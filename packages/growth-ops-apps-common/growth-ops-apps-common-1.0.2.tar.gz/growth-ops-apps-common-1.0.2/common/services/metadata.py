import os
from functools import cached_property

import requests
from google.cloud import run_v2

from ..core.utils import timed_lru_cache


class MetadataService:
    def __init__(self, project: str = None, region: str = None):
        self._project = project
        self._region = region
        self.headers = {
            "Metadata-Flavor": "Google"
        }
        self.run_client = run_v2.ServicesClient()

    @cached_property
    def project_id(self):
        if self._project:
            return self._project
        return requests.get(
            url="http://metadata.google.internal/computeMetadata/v1/project/project-id",
            headers=self.headers
        ).content.decode()

    @cached_property
    def region(self):
        if self._region:
            return self._region
        return requests.get(
            url="http://metadata.google.internal/computeMetadata/v1/instance/region",
            headers=self.headers
        ).content.decode().split('/')[3]

    @cached_property
    def service_account(self):
        return requests.get(
            url="http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email",
            headers=self.headers
        ).content.decode()

    @cached_property
    def service_name(self):
        return os.environ.get('K_SERVICE')

    @cached_property
    def token(self):
        return requests.get(
            url="http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
            headers=self.headers
        ).json()['access_token']

    @cached_property
    def public_url(self):
        project_id = self.project_id
        region = self.region
        service_name = os.environ.get('K_SERVICE')
        token = self.token
        base_url = f"https://{region}-run.googleapis.com"
        return requests.get(
            url=f"{base_url}/apis/serving.knative.dev/v1/namespaces/{project_id}/services/{service_name}",
            headers={
                'Authorization': f"Bearer {token}"
            }
        ).json()['status']['url']

    @cached_property
    def list_services(self):
        project = self.project_id if not self._project else self._project
        location = self.region if not self._region else self._region
        # noinspection PyTypeChecker
        request = run_v2.ListServicesRequest(
            parent=f"projects/{project}/locations/{location}"
        )
        return self.run_client.list_services(request=request)

    @timed_lru_cache(seconds=3600)
    def get_public_url_for_service(
        self,
        service_name: str
    ):
        return {service.name.split('/')[-1]: service.uri for service in self.list_services}[service_name]
