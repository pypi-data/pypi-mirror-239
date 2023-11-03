import json
from datetime import datetime, timedelta, timezone

from google.cloud import tasks_v2
from google.cloud.tasks_v2 import Task
from google.protobuf import timestamp_pb2

from .base import BaseService


class CloudTasksService(BaseService):

    def __init__(
        self,
        cloud_tasks_client: tasks_v2.CloudTasksClient,
        project: str,
        location: str,
        base_url: str,
        service_account_email: str
    ) -> None:
        self.cloud_tasks_client = cloud_tasks_client
        self.project = project
        self.location = location
        self.base_url = base_url
        self.service_account_email = service_account_email
        super().__init__(log_name='cloud_tasks.service')

    def enqueue(
        self,
        queue: str,
        handler_uri: str,
        payload: dict = None,
        in_seconds: int = None
    ) -> Task:
        parent = self.cloud_tasks_client.queue_path(self.project, self.location, queue)

        # Construct the request body.
        base_url = self.base_url.strip('/')
        handler_uri = handler_uri.strip('/')
        url = handler_uri if handler_uri.startswith('https://') else f"{base_url}/{handler_uri}"
        self.logger.log_text(f"Enqueueing task on {url}", severity='DEBUG')
        task = {
            'http_request': {  # Specify the type of request.
                'http_method': tasks_v2.HttpMethod.POST,
                'url': url,  # The full url path that the task will be sent to.
                'oidc_token': {
                    'service_account_email': self.service_account_email,
                    'audience': self.base_url
                },
            }
        }

        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = json.dumps(payload).encode()

            # Add the payload to the request.
            task['http_request']['body'] = converted_payload

        if in_seconds is not None:
            # Convert "seconds from now" into a rfc3339 datetime string.
            d = datetime.now(tz=timezone.utc) + timedelta(
                seconds=in_seconds
            )
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)

            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp

        return self.cloud_tasks_client.create_task(request={'parent': parent, 'task': task})
