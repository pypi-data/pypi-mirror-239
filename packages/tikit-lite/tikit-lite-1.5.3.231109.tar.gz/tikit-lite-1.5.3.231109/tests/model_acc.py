# -*- coding=utf-8
import json
import os
import unittest

from tikit.tencentcloud.tione.v20211111 import models as MM
from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tikit.client import Client
from tikit import models

client = Client(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"), region="ap-shanghai", tione_endpoint="tione.test.tencentcloudapi.com")


class ModelTiACCTestCase(unittest.TestCase):

    def test_describe_model_accelerate_tasks(self):
        try:
            result = client.describe_model_accelerate_tasks()
            print(result)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_model_accelerate_task(self):
        try:
            model_input = models.CosPathInfo("scott-test-sh-1256580188","ti-acc/torchscript/inceptionv3.pt","ap-shanghai")
            model_output = models.CosPathInfo("scott-test-sh-1256580188","ti-acc/output/","ap-shanghai")
            ret = client.create_model_accelerate_task("tikit-tiacc-task",
                                        "COS","TORCH_SCRIPT",
                                        "scott_test_130","v2",
                                        model_input, model_output,
                                        ["input_0:float(1*3*640*640)"])
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_model_accelerate_task(self):
        try:
            ret = client.describe_model_accelerate_task("acc-xxxx")
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_stop_model_accelerate_task(self):
        try:
            ret = client.stop_model_accelerate_task("acc-xxxx")
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_delete_model_accelerate_task(self):
        try:
            ret = client.delete_model_accelerate_task("acc-xxxx")
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_restart_model_accelerate_task(self):
        try:
            model_input = models.CosPathInfo("scott-test-sh-1256580188","ti-acc/torchscript/inceptionv3.pt","ap-shanghai")
            model_output = models.CosPathInfo("scott-test-sh-1256580188","ti-acc/output/","ap-shanghai")
            ret = client.restart_model_accelerate_task("acc-xxxx",
                                        "COS","TORCH_SCRIPT",
                                        "scott_test_130","v2",
                                        model_input, model_output,
                                        ["input_0:float(1*3*640*640)"])
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)


    def test_create_optimized_model(self):
        try:
            ret = client.create_optimized_model("acc-xxxx")
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)


    def test_describe_model_acc_engine_versions(self):
        try:
            ret = client.describe_model_acc_engine_versions()
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    
    def test_create_batch_model_acc_tasks(self):
        try:
            model_output = models.CosPathInfo("scott-test-sh-1256580188","ti-acc/output/","ap-shanghai")
            batch_tasks = []
            batch_task = MM.BatchModelAccTask()
            batch_task.ModelName = "scott_test_130"
            batch_task.ModelVersion = "v2"

            model_input = MM.CosPathInfo()
            model_input.Bucket = "scott-test-sh-1256580188"
            model_input.Paths = ["ti-acc/torchscript/inceptionv3.pt"]
            model_input.Region = "ap-shanghai"
            batch_task.ModelInputPath = model_input

            batch_task.ModelFormat = "TORCH_SCRIPT"
            batch_task.ModelSource = "COS"
            batch_task.TensorInfos = ["input_0:float(1*3*640*640)"]
            batch_tasks.append(batch_task)

            ret = client.create_batch_model_acc_tasks("tikit-tiacc-task",
                                                batch_tasks,model_output)
            print(ret)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)