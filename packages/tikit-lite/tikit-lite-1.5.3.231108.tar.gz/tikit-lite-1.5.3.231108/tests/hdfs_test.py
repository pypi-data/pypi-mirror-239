# -*- coding=utf-8
import json
import unittest

import tikit


def output(data):
    print(json.dumps(data, indent=2))


class HdfsTestCase(unittest.TestCase):

    def test_upload_to_hdfs_file(self):
        # 文件 到 不存在的文件：  新建
        # 文件 到 存在的文件：   抛异常
        # 文件 到 存在的目录：   放到目录中
        # 文件 到 不存在的目录：  新建目录
        result = tikit.upload_to_hdfs("dir1/file1", "http://10.0.3.16:4008", "/dir1/file1")
        output(result)
        result = tikit.upload_to_hdfs("dir1/file1", "http://10.0.3.16:4008", "/dir1/file1")
        output(result)
        result = tikit.upload_to_hdfs("dir1/file2", "http://10.0.3.16:4008", "/dir1/")
        output(result)
        result = tikit.upload_to_hdfs("dir1/file2", "http://10.0.3.16:4008", "/dir1/dir3/")
        output(result)

    def test_upload_to_hdfs_dir(self):
        # 目录 到 存在的文件：   报错
        # 目录 到 存在的目录：   文件夹上传成 子目录 !!
        # 目录 到 不存在的目录：  目录到目录
        result = tikit.upload_to_hdfs("dir1", "http://10.0.3.16:4008", "/dir1/file1")
        output(result)
        result = tikit.upload_to_hdfs("dir1", "http://10.0.3.16:4008", "/dir1")
        output(result)
        result = tikit.upload_to_hdfs("dir1", "http://10.0.3.16:4008", "/dir1/dir11")
        output(result)

    def test_download_from_hdfs_file(self):
        # 文件 到 不存在的文件：  新建
        # 文件 到 存在的文件：   抛异常
        # 文件 到 存在的目录：   放到目录中
        # 文件 到 不存在的目录：  当成文件
        result = tikit.download_from_hdfs("http://10.0.3.16:4008", "/dir1/file1", "dir1/file12")
        output(result)
        result = tikit.download_from_hdfs("http://10.0.3.16:4008", "/dir1/file1", "dir1/file12")
        output(result)
        result = tikit.download_from_hdfs("http://10.0.3.16:4008", "/dir1/file1", "dir12/")
        output(result)
        result = tikit.download_from_hdfs("http://10.0.3.16:4008", "/dir1/file1", "dir13/dir13/")
        output(result)

    def test_download_from_hdfs_dir(self):
        # 目录 到 存在的文件：   报错
        # 目录 到 存在的目录：   文件夹下载到 子目录
        # 目录 到 不存在的目录：  目录到目录
        result = tikit.download_from_hdfs("http://10.0.3.16:4008", "/dir1/", "dir1/file1")
        output(result)
        result = tikit.download_from_hdfs("http://10.0.3.16:4008", "/dir1/", "dir1/")
        output(result)
        result = tikit.download_from_hdfs("http://10.0.3.16:4008", "/dir1/", "dir13/dir13/dir13")
        output(result)
