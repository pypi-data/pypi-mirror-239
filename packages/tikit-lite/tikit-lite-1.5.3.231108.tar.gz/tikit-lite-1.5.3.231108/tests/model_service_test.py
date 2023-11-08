# -*- coding=utf-8
import json
import os
import unittest

from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tikit import models
from tikit.client import Client
from tikit.tencentcloud.tione.v20211111 import models as MM


client = Client(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"), "ap-shanghai", tione_endpoint="tione.pre.tencentcloudapi.com")


def output(data):
    print(json.dumps(data, indent=2))


class ModelServiceTestCase(unittest.TestCase):

    def test_create_model_service(self):
        try:
            framework = models.FrameworkInfo.new_custom("", "PRESET",
                                                        "ccr.ccs.tencentyun.com/qcloud-ti-platform/"
                                                        "ti-cloud-infer-pytorch-cpu:py38-torch1.9.0-cpu-1.0.0")
            worker_resource = models.ModelServiceResurceConfigInfo.new_postpaid("TI.S.MEDIUM.POST")
            cos_path_info = MM.CosPathInfo()
            cos_path_info.Paths = [
                "m-558585918986294016/mv-v1-558585918986294017/"
            ]
            cos_path_info.Uin = "100005348929"
            cos_path_info.SubUin = "100026210598"
            cos_path_info.Bucket = "hayescao-sh-1256580188"
            cos_path_info.Region = "ap-shanghai"
            model_config_info = models.ModelConfigInfo.new_model_reference(model_id="m-558585918986294016",
                                                                           model_name="ziquan_det_1",
                                                                           model_version_id="mv-v1-558585918986294017",
                                                                           model_version="v1", model_source="COS",
                                                                           cos_path_info=cos_path_info,
                                                                           model_type="NORMAL")
            result = client.create_model_service(service_group_name="ziquan_test_2",
                                                 worker_resource=worker_resource,
                                                 framework=framework,
                                                 model_config_info=model_config_info)
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_model_service_version(self):
        try:
            framework = models.FrameworkInfo.new_custom("", "CCR", "ccr.ccs.tencentyun.com/tiemsdev/hellotest",
                                                        "ap-guangzhou", "")
            worker_resource = models.ModelServiceResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST")

            result = client.create_model_service_version(service_group_id="ms-dff7gm9s",
                                                         worker_resource=worker_resource,
                                                         framework=framework,
                                                         scale_mode="MANUAL",
                                                         replicas=1,
                                                         authorization_enable=False)
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_modify_model_service(self):
        try:
            framework = models.FrameworkInfo.new_custom("", "PRESET",
                                                        "ccr.ccs.tencentyun.com/qcloud-ti-platform/"
                                                        "ti-cloud-infer-pytorch-cpu:py38-torch1.9.0-cpu-1.0.0")
            worker_resource = models.ModelServiceResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST")
            cos_path_info = MM.CosPathInfo()
            cos_path_info.Paths = [
                "m-558585918986294016/mv-v1-558585918986294017/"
            ]
            cos_path_info.Uin = "100005348929"
            cos_path_info.SubUin = "100026210598"
            cos_path_info.Bucket = "hayescao-sh-1256580188"
            cos_path_info.Region = "ap-shanghai"
            model_config_info = models.ModelConfigInfo.new_model_reference(model_id="m-558585918986294016",
                                                                           model_name="ziquan_det_1",
                                                                           model_version_id="mv-v1-558585918986294017",
                                                                           model_version="v1", model_source="COS",
                                                                           cos_path_info=cos_path_info,
                                                                           model_type="NORMAL")
            result = client.modify_model_service(service_id="ms-dff7gm9s-1",
                                                 model_config_info=model_config_info,
                                                 framework=framework,
                                                 worker_resource=worker_resource,
                                                 service_description="更新test1")
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)
    
    def test_describe_model_service_groups(self):
        try:
            result = client.describe_model_service_groups()
            if len(result.ServiceGroups) == 0:
                print('0 group found:', result._serialize())
                return
            model_service_group = result.ServiceGroups[0]
            result = client.describe_model_service_group(model_service_group.ServiceGroupId)
            if result.ServiceGroup is None or len(result.ServiceGroup.Services) == 0:
                print('model service group is none:', result._serialize())
                return

            result = client.describe_model_services()
            if len(result.Services) == 0:
                print('0 services found:', result._serialize())
                return
            model_service = result.Services[0]
            result = client.describe_model_service(service_id=model_service.ServiceId)
            print("the first model:", result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)





