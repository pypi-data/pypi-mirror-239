# -*- coding=utf-8
import json
import unittest

import tikit


def output(data):
    print(json.dumps(data, indent=2))


class CosTestCase(unittest.TestCase):

    def test_describe_cos_buckets(self):# help(tikit.describe_cos_buckets)
        buckets = tikit.describe_cos_buckets()
        output(buckets)

    def test_upload_to_cos(self):
        help(tikit.upload_to_cos)
        # upload file.  1. 文件到文件； 2. 文件到目录(有斜杠）
        tikit.upload_to_cos("cos.py", "tai-1300158565", "aaa/bbb")
        tikit.upload_to_cos("cos.py", "tai-1300158565", "aaa/bbb/")

        # upload dir.   1. 目标目录； 2. 目标目录的子目录。 与hdfs、linux保持一致，不需要跟coscmd一样。
        tikit.upload_to_cos("AAA", "tai-1300158565", "not_exist/")
        tikit.upload_to_cos("AAA", "tai-1300158565", "exist/")

    def test_describe_cos_path(self):
        objects = tikit.describe_cos_path("tai-1300158565", "aaa/BBB")
        output(objects)
        objects = tikit.describe_cos_path("tai-1300158565", "aaa/BBB/")
        output(objects)

    def test_delete_cos_path(self):
        # 不带斜杠的，当成文件来删除
        tikit.delete_cos_path("tai-1300158565", "aaa/AAA")
        # 带斜杠的，当成文件夹来删除
        tikit.delete_cos_path("tai-1300158565", "aaa/AAA/")

    def test_download_from_cos(self):
        # ------  get_cos_sub_files
        tikit._default_client.guarantee_valid()
        result = tikit._default_client.get_cos_sub_files("tai-1300158565", "aa/sss/bb/tmp.tif")
        output(result)
        # 文件 到 存在的文件：   覆盖
        # 文件 到 不存在的文件：  新建
        # 文件 到 存在的目录：   直接下载
        # 文件 到 不存在的目录：  新建目录
        tikit.download_from_cos("tai-1300158565", "aa/sss/bb/tmp.tif", "tmp.tif")
        tikit.download_from_cos("tai-1300158565", "aa/sss/bb/tmp.tif", "a/b/tmp.tif")
        tikit.download_from_cos("tai-1300158565", "aa/sss/bb/tmp.tif", "a/b/")
        tikit.download_from_cos("tai-1300158565", "aa/sss/bb/tmp.tif", "a/b/c")
        # 目录 到 不存在的文件：  -
        # 目录 到 存在的文件：   报错
        # 目录 到 存在的目录：   目录到子目录。  与hdfs、linux保持一致，不需要跟coscmd一样。
        # 目录 到 不存在的目录：  目录到目录
        tikit.download_from_cos("tai-1300158565", "aa/sss", "tmp.tif")
        tikit.download_from_cos("tai-1300158565", "aa/sss", "a/b")
        tikit.download_from_cos("tai-1300158565", "aa/sss", "a/c")
        tikit.download_from_cos("tai-1300158565", "aa/sss", "a/c/")
