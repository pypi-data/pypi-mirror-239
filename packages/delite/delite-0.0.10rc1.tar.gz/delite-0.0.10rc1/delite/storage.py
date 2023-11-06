from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .credentials import Credentials


class Storage:
    def __init__(self, credentials: Credentials, region: str = "us-east-1", bucket: str = None, endpoint: str = None):
        self.region = region
        self.bucket = bucket
        self.endpoint = endpoint
        self.credentials = credentials

        if self.endpoint is None:
            raise Exception("Endpoint is required")

        if self.bucket is None:
            raise Exception("Bucket is required")

        if self.region is None or self.region.strip() == "":
            raise Exception("Region is required")

    def use(self, file_path: str) -> str:
        q_params = ""

        q_params += self.credentials.use()
        q_params += "&s3_bucket={}".format(self.bucket)
        q_params += "&s3_endpoint={}".format(self.endpoint)

        if self.region is not None:
            q_params += "&s3_region={}".format(self.region)

        return "s3://{}/{}?{}".format(
            self.bucket,
            file_path,
            q_params,
        )

    def as_key(self):
        return "{}>{}@{}".format(self.bucket, self.endpoint, self.region)
