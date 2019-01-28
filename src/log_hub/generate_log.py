# -*- coding:utf-8 -*-

"""
读取sample.log, 1s读取100条日志打印到access.log
@author: gantao
@create_date: 2019-01-02
"""

import os
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    in_path = os.path.join(BASE_DIR, 'sougou.log')
    out_path = os.path.join(BASE_DIR, 'access.log')

    with open(in_path, 'r') as in_file:
        for line in in_file:
            with open(out_path, 'w') as out_file:
                out_file.write(line)
                time.sleep(0.001)

if __name__ == '__main__':
    main()
