# -*- coding=utf-8
import json
import os
import unittest

from tikit.tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tikit import models
from tikit.client import Client


client = Client(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"),
            tione_endpoint="tione.pre.tencentcloudapi.com", region=os.getenv("REGION"))

def output(data):
    print(json.dumps(data, indent=2))


class TrainingTaskTestCase(unittest.TestCase):
    def test_download_from_cos(self):
        client.download_from_cos("ofs-ifenghadoop-1300722751", "/user/recom/ningxr/code/", "/home/tione/notebook/")

    def test_parse_cos_info(self):
        output(client.parse_cos_info("aaa/bbb/")._serialize())
        # client.parse_coc_str("aaa/bbb")

    def test_describe_training_frameworks(self):
        try:
            result = client.describe_training_frameworks()
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_postpaid_training_price(self):
        try:
            # result = client.describe_billing_specs([{"SpecName": "TI.S.4XLARGE32.POST", "SpecCount": 1},
            #                                         {"SpecName": "HDD云硬盘10G", "SpecCount": 1}])
            result = client.describe_postpaid_training_price()
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_prepaid(self):
        try:
            # 预付费，dataset存储数据挂载，PS_WORKER
            framework = models.FrameworkInfo.new_system_framework("TENSORFLOW", "1.15-py3.6-cpu", "PS_WORKER")
            worker_resource = models.ResourceConfigInfo.new_prepaid(1, 2, 0)
            ps_resource = models.ResourceConfigInfo.new_prepaid(1, 2.2, 0)
            input_datas = [models.TrainingDataConfig.new_dataset_mount("ds-rsp2tctp", "/opt/ml/input/data/1"),
                           models.TrainingDataConfig.new_dataset_mount("ds-rsp2tctp", "/opt/ml/input/data/2")]
            result = client.create_training_task("tikit-prepaid-dataset-2",
                                                 framework,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 worker_resource,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 ps_resource,
                                                 input_data_config=input_datas,
                                                 resource_group_id="trsg-7fmj9d42",
                                                 worker_start_cmd="sleep 1000",
                                                 ps_start_cmd="sleep 1000")
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_rdma(self):
        try:
            # 预付费，dataset存储数据挂载，PS_WORKER
            framework = models.FrameworkInfo.new_system_framework("TENSORFLOW", "tf1.15-py3.7-cpu", "PS_WORKER")
            worker_resource = models.ResourceConfigInfo.new_prepaid(1, 2, 0)
            ps_resource = models.ResourceConfigInfo.new_prepaid(1, 2.2, 0)
            result = client.create_training_task("tikit-rdma-006",
                                                 framework,
                                                 "kiten2-1256580188/",
                                                 worker_resource,
                                                 "kiten2-1256580188/",
                                                 ps_resource,
                                                 resource_group_id="trsg-bvmtk8wf",
                                                 enable_rdma=True)
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_taiji_hy_task(self):
        try:
            worker_resource = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
            template_name = "ti_gpt_7b_sft_lora_small_template"
            tuning_parameters_dict = {}
            tuning_parameters_dict["WARMUP_TOKENS"] = "375000000"
            tuning_parameters_dict["epoch_num"] = "10"
            input_datas = [models.TrainingDataConfig.new_mount_cos("kiten-1256580188/", "/opt/ml/input/data/1")]
            result = client.create_taiji_hy_training_task("tikit-taiji-hy-task-16",
                                                          worker_resource,
                                                          template_name,
                                                          input_data_config=input_datas,
                                                          tuning_parameters_dict=tuning_parameters_dict)
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_postpaid(self):
        try:
            # 后付费，cos存储数据挂载
            framework = models.FrameworkInfo.new_system_framework("TENSORFLOW", "tf1.15-py3.7-cpu", "MPI")
            worker_resource = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
            input_datas = [models.TrainingDataConfig.new_mount_cos("hhh-gz-1256580188/dir-1/", "/opt/ml/input/data/1"),
                           models.TrainingDataConfig.new_mount_cos("hhh-gz-1256580188/dir-1/dir-1-1/", "/opt/ml/input/data/2")]
            result = client.create_training_task("tikit-post_paid-cos-0318-3",
                                                 framework,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 worker_resource,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 input_data_config=input_datas,
                                                 worker_start_cmd="sleep 1000")
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_cfs(self):
        try:
            framework = models.FrameworkInfo.new_system_framework("TI_ACC", "1.0.0-torch1.7.1-py3.6-cuda10.1-gpu", "DDP")
            worker_resource = models.ResourceConfigInfo.new_prepaid(1, 2, 0)
            input_datas = [models.TrainingDataConfig.new_mount_cfs("cfs-526h2lnb", "/", "/opt/ml/input/data/1"),
                           models.TrainingDataConfig.new_mount_cfs("cfs-526h2lnb", "/hhh", "/opt/ml/input/data/2")]
            result = client.create_training_task("tikit-cfs-0317-5",
                                                 framework,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 worker_resource,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 input_data_config=input_datas,
                                                 resource_group_id="trsg-7fmj9d42",
                                                 worker_start_cmd="sleep 1000",
                                                 vpc_id="vpc-3slyyrbf",
                                                 sub_net_id="subnet-q9dg58fq")
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_hdfs(self):
        try:
            framework = models.FrameworkInfo.new_system_framework("TI_ACC", "1.0.0-torch1.7.1-py3.6-cuda10.1-gpu", "DDP")
            worker_resource = models.ResourceConfigInfo.new_prepaid(1, 2, 0)
            input_datas = [models.TrainingDataConfig.new_mount_hdfs("emr-kjgjcdvv", "/", "/opt/ml/input/data/1"),
                           models.TrainingDataConfig.new_mount_hdfs("emr-kjgjcdvv", "/emr/", "/opt/ml/input/data/2"),
                           models.TrainingDataConfig.new_mount_hdfs("emr-kjgjcdvv", "/emr/dir-1", "/opt/ml/input/data/3")]
            result = client.create_training_task("tikit-hdfs-0318-5",
                                                 framework,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 worker_resource,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 input_data_config=input_datas,
                                                 resource_group_id="trsg-7fmj9d42",
                                                 worker_start_cmd="sleep 1000",
                                                 vpc_id="vpc-qus24ksr",
                                                 sub_net_id="subnet-15h02et6")
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_wedata_hdfs(self):
        try:
            framework = models.FrameworkInfo.new_system_framework("PYTORCH", "torch1.9-py3.8-cuda11.1-gpu", "DDP")
            worker_resource = models.ResourceConfigInfo.new_postpaid("TI.S.2XLARGE16.POST", 1)
            input_datas = [models.TrainingDataConfig.new_mount_wedata_hdfs(914253, "/", "/opt/ml/input/data/wedata1")]
            result = client.create_training_task("suix_tikit_wedata_hdfs_test",
                                                 framework,
                                                 "wedata-fusion-test1-1257305158/",
                                                 worker_resource,
                                                 "wedata-fusion-test1-1257305158/",
                                                 input_data_config=input_datas,
                                                 worker_start_cmd="sleep 30000",
                                                 vpc_id="vpc-1ypowa2u",
                                                 sub_net_id="subnet-cvrt5pff")
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_ai_market_algo(self):
        try:
            framework = models.FrameworkInfo.new_system_framework("PYTORCH", "torch1.9-py3.8-cuda11.1-gpu", "DDP")
            worker_resource = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
            input_datas = [models.TrainingDataConfig.new_ai_market_algo("hunyuan_bert_base_chinese_short_text_matching-v1", "/opt/ml/input/data/aimarket_pretrain_model")]
            result = client.create_training_task("kiten_tikit_ai_market_algo_test",
                                                 framework,
                                                 "kiten2-1256580188/",
                                                 worker_resource,
                                                 "kiten2-1256580188/",
                                                 input_data_config=input_datas,
                                                 worker_start_cmd="ls /opt/ml/input/data/aimarket_pretrain_model && sleep 60")
                                                 #vpc_id="vpc-1ypowa2u",
                                                 #sub_net_id="subnet-cvrt5pff")
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_create_training_task_postpaid_deprecated(self):
        try:
            # 后付费，cos存储数据挂载
            framework = models.FrameworkInfo.new_system_framework("TI_ACC", "1.0.0-torch1.7.1-py3.6-cuda10.1-gpu", "DDP")
            worker_resource = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
            input_data = models.TrainingDataConfig.new_cos_data({"hhh-gz-1256580188/": "/opt/ml/input/data/1",
                                                                 "hhh-gz-1256580188/dir-1/": "/opt/ml/input/data/2"})
            result = client.create_training_task("tikit-post_paid-deprecated-02",
                                                 framework,
                                                 "hhh-gz-1256580188/dir-1/",
                                                 worker_resource,
                                                 code_package_path="hhh-gz-1256580188/dir-1/",
                                                 worker_start_cmd="sleep 1000",
                                                 input_data_config=input_data)
            print(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_training_tasks(self):
        try:
            result = client.describe_training_tasks()
            print(result)
            # output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_training_task(self):
        try:
            # client._tione_client.profile.language = "zh-CN"
            result = client.describe_training_task("train-23510266138202112")
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_stop_training_task(self):
        try:
            result = client.stop_training_task("train-848325581826295680")
            print(result.to_json_string())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_delete_training_task(self):
        try:
            result = client.delete_training_task("train-848505140425199744")
            print(result.to_json_string())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_training_task_pods(self):
        try:
            result = client.describe_training_task_pods("train-51cd6bf7ec1000")
            output(result._serialize())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_logs(self):
        try:
            import datetime
            now_time = datetime.datetime.now(datetime.timezone.utc)
            now_time_str = now_time.isoformat()
            result = client.describe_train_logs("train-51d6dbedfc1000*",
                                                "2021-12-10T09:32:03.823509+00:00",
                                                now_time_str,
                                                limit=30)
            print(result)

            # 这种用起来更方便，但如果
            print(result.next())
            print(result)
            print(result.next())
            print(result.next())
        except TencentCloudSDKException as err:
            print("error:")
            print(err)
            
    def test_describe_taiji_template(self):
        template_id = "ti_gpt_7b_sft_lora_small_template"
        try:
            result = client.describe_taiji_template(template_id)
            print(result)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)

    def test_describe_taiji_template_list(self):
        try:
            result = client.describe_taiji_template_list()
            print(result)
        except TencentCloudSDKException as err:
            print("error:")
            print(err)