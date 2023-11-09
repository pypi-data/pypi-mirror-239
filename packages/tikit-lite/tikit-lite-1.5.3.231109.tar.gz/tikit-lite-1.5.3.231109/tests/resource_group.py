# -*- coding=utf-8
import json
import os
import unittest
import time

from tikit.tencentcloud.common import credential
from tikit.tencentcloud.common.profile.client_profile import ClientProfile
from tikit.tencentcloud.common.profile.http_profile import HttpProfile
from tikit.tencentcloud.tione.v20211111 import tione_client, models
from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

import tikit

from tikit.client import Client


client = Client(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"), tione_endpoint="tione.test.tencentcloudapi.com")


def output(data):
    print(json.dumps(data, indent=2))


class ResourceGroupTestCase(unittest.TestCase):

    def test_describe_train_resource_groups(self):
        try:
            result = client.describe_train_resource_groups(limit=10, search_word="train")
            print(result)
            print(result._repr_html_())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_inference_resource_groups(self):
        try:
            result = client.describe_inference_resource_groups(limit=10)
            print(result)
            print(result._repr_html_())
            print(result.to_json_string())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)
