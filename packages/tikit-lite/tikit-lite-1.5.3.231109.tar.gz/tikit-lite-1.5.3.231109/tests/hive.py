# -*- coding=utf-8
import os
import unittest

from pyhive import hive

import tikit
import time
import jwt

HIVE_PASSWORD = os.getenv("HIVE_PASSWORD")

from tikit.client import Client
from tikit.hive import HiveInitial
client = Client(os.getenv("secret_id"), os.getenv("secret_key"), tione_endpoint="tione.pre.tencentcloudapi.com", region="ap-guangzhou")

class HiveTestCase(unittest.TestCase):

    def test_insert_hdfs_into_hive(self):
        tikit.insert_hdfs_into_hive("/tmp/d1", "10.0.0.54:7001", "t3", username="hadoop", password=HIVE_PASSWORD)

    def test_upload_to_hive_by_hdfs(self):
        # 文件
        # 文件夹
        # 文件夹中有文件夹
        result = tikit.upload_to_hive_by_hdfs("/root/file.csv", "http://10.0.0.54:4008", "10.0.0.54:7001", "t3", username="hadoop", password=HIVE_PASSWORD)
        print(result)
        result = tikit.upload_to_hive_by_hdfs("/root/kinvo/ti", "http://10.0.0.54:4008", "10.0.0.54:7001", "t3", username="hadoop", password=HIVE_PASSWORD)
        print(result)
        result = tikit.upload_to_hive_by_hdfs("/root/kinvo/ti/d2", "http://10.0.0.54:4008", "10.0.0.54:7001", "t3", username="hadoop", password=HIVE_PASSWORD)
        print(result)

    # def test_export_csv_from_hive(self):
    #     # 文件 到 不存在的文件：  新建
    #     # 文件 到 存在的文件：   抛异常
    #     # 文件 到 存在的目录：   放到目录中
    #     # 文件 到 不存在的目录：  当成文件
    #     result = tikit.export_csv_from_hive("/root/kinvo/tixx/aa.csv", "10.0.0.54:7001", "t1", username="hadoop", password=HIVE_PASSWORD)
    #     print(result)
    #     result = tikit.export_csv_from_hive("/root/kinvo/tixx/aa.csv", "10.0.0.54:7001", "t1", username="hadoop", password=HIVE_PASSWORD)
    #     print(result)
    #     result = tikit.export_csv_from_hive("/root/kinvo/ti", "10.0.0.54:7001", "t1", username="hadoop", password=HIVE_PASSWORD)
    #     print(result)
    #     result = tikit.export_csv_from_hive("/root/kinvo/not_existed", "10.0.0.54:7001", "t1", username="hadoop", password=HIVE_PASSWORD)
    #     print(result)

    def test_export_from_hive_by_hdfs(self):
        tikit.export_from_hive_by_hdfs("/root/kinvo/ti", "http://10.0.0.54:4008", "10.0.0.54:7001", "t1", username="hadoop", password=HIVE_PASSWORD)

    def test_get_hive_cursor(self):
        with hive.Connection(host="10.0.0.54", port=7001, database=database,
                             username="hadoop", password=HIVE_PASSWORD, auth="CUSTOM") as conn:
            with conn.cursor() as c:
                c.execute("show databases")
                c.fetchall()
                c.execute("create table t1(a string, b string, c string) row format delimited fields terminated by ','")
                c.execute("load data local inpath '/tmp/file.csv' overwrite into table t3")
                c.execute("select * from t3")
                c.fetchall()
                c.execute("INSERT OVERWRITE LOCAL DIRECTORY '/tmp/file3' row format delimited fields terminated by ',' SELECT * FROM t1")

    def test_hive_initial_wedata(self):
        hive_init = HiveInitial(client)
        hive_init.hive_initial_wedata(4116, "100022374906")

    def test_generate_wedata_jwt_token(self):
        jwt_payload = {
            "user_id": "100022256608",
            "tenant_id": "1257305158",
            "exp": int(time.time() + 3600),
            "owner_user_id": "100006908545",
        }

        jwt_headers = {
            "typ": "JWT",
            "alg": "HS256"
        }
        jwt_token = "Bearer " + jwt.encode(payload=jwt_payload, key="tbds@2022", algorithm='HS256',
                                           headers=jwt_headers)
        print(jwt_token)