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


class MonitorTestCase(unittest.TestCase):

    def test_push_training_metrics(self):
        try:
            # 在 TI 的训练任务内，自动获取当前任务的ID
            result = client.push_training_metrics(
                int(time.time()),
                {"field1": 20, "field2": 30}
            )
            print(result.to_json_string())
            # 手动填入任务ID
            result = client.push_training_metrics(
                int(time.time()),
                {"field1": 30, "field2": 40},
                "train-51bf1677fc1000",
                3,
                1000,
                68
            )
            print(result.to_json_string())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_push_training_metrics_list(self):
        try:
            metric = models.MetricData()
            metric.Timestamp = int(time.time())
            # metric.TaskId = "task-id-00002"
            metric.Epoch = 3
            metric.Step = 66
            metric.TotalSteps = 1000
            metric.Points = [{"Name": "request3-1", "Value": 51}, {"Name": "request3-2", "Value": 52.01}]
            metric_list = [metric]
            result = client.push_training_metrics_list(metric_list)
            print(result.to_json_string())
            # TODO 若是push一个metrics的时候，参数可以是metric的成员，point使用 map 的方式更加方便。 metrics数组就只能一个参数了。
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_training_metrics(self):
        try:
            result = client.describe_training_metrics("train-51bf1677fc1000")
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)
