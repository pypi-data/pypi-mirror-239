import os

import requests
from requests.structures import CaseInsensitiveDict


class ReachApiGateway:
    def __init__(self):
        self.environment = os.environ.get("ENV", "Staging")

    @property
    def base_url(self):
        return {
            "Staging": "https://90tin0ndr1.execute-api.us-east-1.amazonaws.com",
            "Prod": "https://101iu6hpaj.execute-api.us-east-1.amazonaws.com",
        }.get(self.environment)

    @property
    def gateway_headers(self):
        common_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        auth_token = {
            "Staging": "Bearer a57a82c0-0493-563b-ba1d-6c63c201ce20",
            "Prod": "Bearer a57a82c0-0493-563b-ba1d-6c63c201ce20",
        }.get(self.environment)

        headers = {**common_headers, "Authorization": auth_token}

        return CaseInsensitiveDict(headers)

    def review_profile_patch_business(self, business_id):
        resp = requests.patch(
            f"{self.base_url}/review-profile/business/{business_id}",
            headers=self.gateway_headers,
        )
        return resp

    def review_profile_post_business(self, business_id):
        resp = requests.post(
            f"{self.base_url}/review-profile/business/{business_id}",
            headers=self.gateway_headers,
        )
        return resp
