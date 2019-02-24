# -*- coding: utf-8 -*-
# @File  : main.py.py
# @Author: Cleland
# @Date  : 2019/2/23
# @Desc  :


import sys
import hashlib
import happybase
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

HBASE_INFO = {
    'host': 'header',
    'port': 9090
}

def parse(row):
    row = row.encode('utf-8')
    row.replace('[', '')
    row.replace(']', '')
    data = row.split('\t')
    print u'create_time: {create_time} user_id: {user_id} keyword: {keyword} rank: {rank} click_sort: {click_sort} url: {url} '.format(
        create_time = data[0],
        user_id = data[1],
        keyword = data[2],
        rank = data[3],
        click_sort = data[4],
        url = data[5]
    )


def process(rdd):
    rdd = rdd.map(lambda row: row.encode('utf-8'))
    rdd = rdd.map(lambda row: row.replace('[', '')).map(lambda row: row.replace(']', ''))
    rows = rdd.collect()
    with happybase.ConnectionPool(
            host=HBASE_INFO['host'],
            port=HBASE_INFO['port'],
            size=3).connection() as connection:
            table = connection.table('test1')
            with table.batch() as bat:
                for row in rows:
                   items = row.split('\t')
                   row_key = hashlib.md5('{0}{1}'.format(items[0], items[1])).hexdigest()
                   bat.put(row=row_key, data={
                       'cf:create_time': items[0],
                       'cf:user_id': items[1],
                       'cf:keyword': items[2],
                       'cf:rank': items[3],
                       'cf:click_sort': items[4],
                       'cf:url': items[5]
                   })


def main():
    sc = SparkContext('local[2]', appName="web log collect")
    sc.setLogLevel('WARN')
    ssc = StreamingContext(sc, 10)

    topic = 'weblogs'
    zkQuorum = 'header:2181,worker-1:2181,worker-2:2181'

    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    lines.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
    main()