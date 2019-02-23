# -*- coding: utf-8 -*-
# @File  : main.py.py
# @Author: Cleland
# @Date  : 2019/2/23
# @Desc  :


import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils



def main():
    sc = SparkContext('local[2]', appName="web log collect")
    sc.setLogLevel('WARN')
    ssc = StreamingContext(sc, 10)

    topic = 'weblogs'
    zkQuorum = 'header:2181,worker-1:2181,worker-2:2181'

    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    print lines.collect()

    ssc.start()
    ssc.awaitTermination()

if __name__ = '__main__':
    main()