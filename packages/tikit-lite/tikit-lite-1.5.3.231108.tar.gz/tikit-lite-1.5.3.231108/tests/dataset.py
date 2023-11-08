# -*- coding=utf-8
import json
import os
import unittest

from tikit.tencentcloud.tione.v20211111 import models
from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tikit.client import Client

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

client = Client(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"), tione_endpoint="tione.test.tencentcloudapi.com")


def output(data):
    print(json.dumps(data, indent=2))


class DatasetTestCase(unittest.TestCase):

    def test_prepare(self):
        client.upload_to_cos("/Users/hqh/Desktop/TiOne/tikit/dataset_ti_images", "ti-251202231", "dataset_ti_images")

    def test_create_text_dataset(self):
        try:
            storage_data_path = "ti-251202231/dataset/"

            storage_label_path = "ti-251202231/dataset-2/"

            result = client.create_text_dataset("tikit-text-01", storage_data_path, storage_label_path)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_table_dataset(self):
        try:
            storage_data_path = "ti-251202231/dataset/"

            storage_label_path = "ti-251202231/dataset-2/"

            schema_info_dict = {
                "初始运维部门ID": "TYPE_INT",
                "初始运维部门": "TYPE_STRING",
                "一级业务ID": "TYPE_INT",
                "一级业务": "TYPE_STRING",
                "二级业务ID": "TYPE_INT",
                "二级业务": "TYPE_STRING",
                "三级业务ID": "TYPE_INT",
                "三级业务": "TYPE_STRING"
            }

            result = client.create_table_dataset("tikit-table-01", storage_data_path, storage_label_path, [],
                                                 True, schema_info_dict)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_image_dataset(self):
        try:
            storage_data_path = "ti-251202231/dataset/"

            storage_label_path = "ti-251202231/dataset-2/"

            result = client.create_image_dataset("tikit-image-01", storage_data_path, storage_label_path,
                                                 with_annotation=False)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_other_dataset(self):
        try:
            storage_data_path = "ti-251202231/dataset/"

            storage_label_path = "ti-251202231/dataset-2/"

            result = client.create_other_dataset("tikit-other-01", storage_data_path, storage_label_path)
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_datasets(self):
        try:
            result = client.describe_datasets()
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_delete_dataset(self):
        try:
            result = client.delete_dataset("365msrh8lw8w")
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_dataset_detail_structured(self):
        try:
            result = client.describe_dataset_detail_structured("36ytwk6e8iyo")
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_dataset_detail_unstructured(self):
        try:
            result = client.describe_dataset_detail_unstructured("37263snevyf4")
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)
