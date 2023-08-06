import datetime
import os
import re
import tempfile
import threading
import uuid

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.http import StreamingHttpResponse
from django.http.cookie import SimpleCookie
from django.utils import timezone

from wiretap.models import Message, Tap

DEFAULT_MAX_MESSAGE_COUNT = 1000

class WiretapMiddleware(object):
    """
    Wiretap middleware. Saves HTTP requests & responses to the `Message` model.
    """

    def __init__(self):
        """
        Wiretap streams responses to disk, then stores the data in a
        `FileField`.

        This isn't particularly performant, so the middleware will disable
        itself if Django isn't in debug mode.
        """

        if not getattr(settings, 'DEBUG', False):
            raise MiddlewareNotUsed()

        self.thread_local = threading.local()

    def should_tap(self, request):
        matching_tap = False
        for tap in Tap.objects.all():
            if re.search(tap.path_regex, request.path):
                return True
        return False

    def process_request(self, request):
        self.thread_local.message = None

        if not self.should_tap(request):
            return

        req_started_at = timezone.now()

        req_content_type = None
        req_headers = []
        for (key, value) in request.META.iteritems():
            if key.startswith('HTTP_'):
                key = key[5:].title()
                req_headers.append((key, value))
                if key == 'Content-Type':
                    content_type = value

        if not request.body:
            req_body_file = None
        else:
            req_body_file = SimpleUploadedFile(
                name=str(uuid.uuid4()),
                content=request.body,
                content_type=req_content_type
            )

        self.thread_local.message = Message.objects.create(
            started_at=req_started_at,
            ended_at=timezone.now(),
            remote_addr=request.META['REMOTE_ADDR'],
            req_method=request.method,
            req_path=request.path,
            req_headers=req_headers,
            req_body=req_body_file
        )

    def process_response(self, request, response):
        if not self.thread_local.message:
            return response
        else:
            return WiretapHttpResponse(response, self.thread_local.message)

class WiretapHttpResponse(StreamingHttpResponse):
    def __init__(self, response, message):
        super(WiretapHttpResponse, self).__init__()
        self._copy_from_response(response)
        self._response = response
        self._message = message

    def _copy_from_response(self, response):
        """
        Copy data from the original response.
        """

        self.status_code = response.status_code
        self.reason_phrase = response.reason_phrase
        self._headers = {
            key.lower(): (key, value,)
            for (key, value) in response.items()
        }
        self.cookies = SimpleCookie(str(response.cookies))

    def __iter__(self):
        with tempfile.NamedTemporaryFile() as fp:
            for chunk in self._response:
                yield chunk
                fp.write(chunk)

            if fp.tell() == 0:
                res_body_file = None
            else:
                fp.seek(0)
                res_body_file = UploadedFile(
                    file=fp,
                    name=str(uuid.uuid4()),
                    content_type=self._response.get('content-type')
                )

            self._message.res_status_code = self._response.status_code
            self._message.res_reason_phrase = self._response.reason_phrase
            self._message.res_headers = self._response.items()
            self._message.res_body = res_body_file
            self._message.save()

            delete_old_messages()

def delete_old_messages():
    max_message_count = getattr(
        settings,
        'WIRETAP_MAX_MESSAGE_COUNT',
        DEFAULT_MAX_MESSAGE_COUNT
    )
    
    if max_message_count is not None:
        delete_pks = Message.objects\
            .order_by('-started_at')\
            .values_list('pk', flat=True)\
            [max_message_count:]

        Message.objects\
            .filter(id__in=delete_pks)\
            .delete()
