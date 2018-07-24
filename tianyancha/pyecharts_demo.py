# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: pyecharts_demo.py
 Time: 7/24/18
"""
import logging
import sys
import os
import requests

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
from pyecharts import Geo

data =[
    ('汕头市', 50), ('汕尾市', 60), ('揭阳市', 35),
    ('阳江市', 44), ('肇庆市', 72)
]
geo = Geo("广东城市空气质量", "data from pm2.5", title_color="#fff",
          title_pos="center", width=1200,
          height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value, maptype='广东', type="effectScatter",
        is_random=True, effect_scale=5, is_legend_show=False)
geo.render()