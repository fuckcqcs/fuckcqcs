# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Since : 3.6
 Author: zhangjian
 Site: https://iliangqunru.bitcron.com/
 File: f_cccs_structure_gen
 Time: 2018/7/24
 
 Add New Functional f_cccs_structure_gen
"""
import json
import os
import sys

PY3 = False

if sys.version > '3':
    PY3 = True


# 结构化后json数据文件

TARGET_JSON = "structure_data.json"


def generate_data_for_echarts():
    if not os.path.exists('structure_data.json'):
        return
    cc_data = []
    with open(TARGET_JSON, mode='r+', encoding='utf-8') as f_target_file:
        json_map = json.load(fp=f_target_file)
        for item in json_map:
            if not item.get('county') == '':
                location_name = item.get('county')
            else:
                if not item.get('city') == '':
                    location_name = item.get('city')
                else:
                    location_name = item.get('province')
            single_way = [{'name': '长春市'},
                          {'name': location_name},
                          {'name': item.get('title')},
                          {'name': item.get('publish_time')},
                          {'name': item.get('title_link')},
                          {'name': item.get('raw_link')},
                          {'name': item.get('location')}]
            cc_data.append(single_way)
    print(cc_data)


if __name__ == '__main__':
    generate_data_for_echarts()