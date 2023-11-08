# -*- coding=utf-8
import json
import unittest

from tikit.tencentcloud.common import credential
from tikit.tencentcloud.common.profile.client_profile import ClientProfile
from tikit.tencentcloud.common.profile.http_profile import HttpProfile
from tikit.tencentcloud.tione.v20211111 import tione_client, models
from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

import tikit


def output(data):
    print(json.dumps(data, indent=2))


class TrainingTaskTestCase(unittest.TestCase):

    def test_create_training_job(self):
        try:
            tikit.create_training_job()
        except TencentCloudSDKException as err:
            print("error:")
            print(err)