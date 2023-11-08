# -*- coding=utf-8
import json
import os
import unittest

from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tikit import models
from tikit.client import Client
from tikit.tencentcloud.tione.v20211111 import models as MM

id = os.getenv("SECRET_ID")
key = os.getenv("SECRET_KEY")

client = Client(id, key, "ap-shanghai", tione_endpoint="tione.pre.tencentcloudapi.com")


def output(data):
    print(json.dumps(data, indent=2))


class ModelServiceTestCase(unittest.TestCase):

    def test_create_model_service(self):
        try:
            framework = models.FrameworkInfo.new_custom("", "CCR",
                                                        "ccr.ccs.tencentyun.com/qcloud-ti-platform/"
                                                        "hellotest")
            worker_resource = models.ModelServiceResourceConfigInfo.new_prepaid(1, 1, 0)

            volume_mount = MM.VolumeMount()
            cfs = MM.CFSConfig()
            cfs.Id = "cfs-xxxxx"
            cfs.Path = "/"
            cfs.Protocol = "TURBO"
            cfs.MountType = "SOURCE"
            volume_mount.CFSConfig = cfs

            result = client.create_model_service(service_group_name="turbofs-test",
                                                 worker_resource=worker_resource,
                                                 framework=framework,
                                                 volume_mount=volume_mount,
                                                 resource_group_id="ersg-6hg977dh",
                                                 )
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)
