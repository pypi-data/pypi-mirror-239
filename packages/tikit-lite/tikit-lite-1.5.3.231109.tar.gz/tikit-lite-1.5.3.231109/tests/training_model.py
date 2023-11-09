# -*- coding=utf-8
import json
import os
import unittest

from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tikit.client import Client
from tikit import models


client = Client(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"), tione_endpoint="tione.test.tencentcloudapi.com")


def output(data):
    print(json.dumps(data, indent=2))


class DatasetTestCase(unittest.TestCase):

    def test_describe_system_reasoning_images(self):
        try:
            result = client.describe_system_reasoning_images()
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_model_by_task(self):
        try:
            reasoning_env = models.ReasoningEnvironment.new_custom_environment("CCR", "ccr.com/my/image:v1")
            a = models.CosPathInfo("demo-1256580188", "output/model-test/", "ap-guangzhou")
            result = client.create_model_by_task("tikit-model-task-122711",
                                                 "train-538458931842563968",
                                                 reasoning_env,
                                                 a,
                                                 "PYTORCH",)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_model_by_cos(self):
        try:
            model_cos_path = "ti-251202231/dataset/"
            reasoning_env = models.ReasoningEnvironment.new_system_environment("tf2.4-py38-cpu")
            a = models.CosPathInfo("demo-1256580188", "output/model-test/", "ap-guangzhou")
            result = client.create_model_by_cos("tikit-model-cos-1227",
                                                "TENSORFLOW",
                                                model_cos_path,
                                                "aa=11,bb=22",
                                                reasoning_env,
                                                a,
                                                "PYTORCH",)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_model_version_by_task(self):
        try:
            reasoning_env = models.ReasoningEnvironment.new_custom_environment("TCR", "ccr.com/my-company/image:v1",
                                                                               "ap-guangzhou", "hhhhh")
            result = client.create_model_version_by_task("m-23036973226987520",
                                                         "train-51b98b6df91000",
                                                         reasoning_env)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_model_version_by_cos(self):
        try:
            reasoning_env = models.ReasoningEnvironment.new_system_environment("pmml-py36")
            result = client.create_model_version_by_cos("m-23054253294030848",
                                                        "TENSORFLOW",
                                                        "ti-251202231/dataset-2/",
                                                        "aa=11,bb=22",
                                                        reasoning_env)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_training_models(self):
        try:
            result = client.describe_training_models()
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_training_model_versions(self):
        try:
            result = client.describe_training_model_versions("m-23036973226987520")
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_training_model_version(self):
        try:
            result = client.describe_training_model_version("22997374388948992")
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_delete_training_model(self):
        try:
            result = client.delete_training_model("22996893500641280")
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_delete_training_model_version(self):
        try:
            result = client.delete_training_model_version("22996893501640704")
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)
