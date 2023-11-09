import json
import os
import unittest

from tikit import models
from tikit.client import Client

client = Client(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"), tione_endpoint="tione.pre.tencentcloudapi.com", region="ap-beijing")

class BatchTaskTestCase(unittest.TestCase):
    def test_create_batch_task(self):
        rcConfig = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
        model_info = models.ModelInfo.new_normal_model("sui-dev-classification-model", "v1")
        ret = client.create_batch_task("batch-test",
                                 1,
                                 rcConfig,
                                "happy-test-sh-1256580188/输出/",
                                 input_config="happy-test-sh-1256580188/notebook-demo-classification-happy/data/val/",
                                 model_info=model_info)
        print(ret)

    def test_create_batch_task_accelerate_model(self):
        rcConfig = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
        model_info = models.ModelInfo.new_accelerate_model("nemo-classify-fp16", "v1-优化1")
        ret = client.create_batch_task("batch-test",
                                       1,
                                       rcConfig,
                                       "happy-test-sh-1256580188/输出/",
                                       input_config="happy-test-sh-1256580188/notebook-demo-classification-happy/data/val/",
                                       model_info=model_info)
        print(ret)

    def test_create_batch_task_custom_image(self):
        rcConfig = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
        image_info = models.FrameworkInfo.new_custom_image("CCR", "ccr.ccs.tencentyun.com/tiemsdev/hellotest:latest")
        ret = client.create_batch_task("batch-test",
                                       1,
                                       rcConfig,
                                       "happy-test-sh-1256580188/输出/",
                                       input_config="happy-test-sh-1256580188/notebook-demo-classification-happy/data/val/",
                                       image_info=image_info)
        print(ret)

    def test_create_batch_task_wedata_hdfs(self):
        rcConfig = models.ResourceConfigInfo.new_postpaid("TI.S.MEDIUM.POST", 1)
        input_datas = [models.TrainingDataConfig.new_mount_wedata_hdfs(914253, "/")]
        # output_datas = [models.TrainingDataConfig.new_mount_wedata_hdfs(914252, "/")]
        output_datas = [models.TrainingDataConfig.new_mount_cos("ali-bj-1257305158/离线跑批输出/", "")]
        model_info = models.ModelInfo.new_normal_model("suix_test_model", "v1")
        ret = client.create_batch_task("batch-test-6",
                                       1,
                                       rcConfig,
                                       output_datas,
                                       input_datas,
                                       start_cmd="sleep 100000",
                                       model_info=model_info,
                                       vpc_id="vpc-1ypowa2u",
                                       subnet_id="subnet-cvrt5pff")
        print(ret)

    def test_describe_batch_task(self):
        print(client.describe_batch_task("Batch-4704mkkbs4cg"))

    def test_describe_batch_tasks(self):
        print(client.describe_batch_tasks())

    def test_stop_batch_task(self):
        print(client.stop_batch_task("Batch-46ffob9olvcw"))

    def test_delete_batch_task(self):
        print(client.delete_batch_task("Batch-46ffob9olvcw"))