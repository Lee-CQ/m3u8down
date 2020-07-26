#!/usr/bin/python3 
# -*- coding: utf-8 -*-
"""
@File Name  : _other_3.py
@Author     : LeeCQ
@Date-Time  : 2020/1/19 12:14

"""
import os
import time
from urllib.parse import urljoin

import m3u8
import requests
from glob import iglob

from natsort import natsorted
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
# pip3 install pycryptodome
# 进入python安装目录，如C:\python37
# 在\Lib\site-packages目录下找到：
# crypto这个目录重命名为: Crypto
from Crypto.Cipher import AES

UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 " \
            "Safari/537.36"


@dataclass
class DownLoadM3U8(object):
    m3u8_url: str
    file_name: str

    def __post_init__(self):
        self.thread_pool = ThreadPoolExecutor(max_workers=10)
        if not self.file_name:
            self.file_name = 'new.mp4'
        self.m3u8_obj = m3u8.load(self.m3u8_url)
        self.cryptor = self.get_key()

    def get_key(self):
        """
        获取key进行解密，这里可以获取method加密方式进行解密
        """
        if self.m3u8_obj.keys and self.m3u8_obj.keys[0]:
            res = requests.get(self.m3u8_obj.keys[0].absolute_uri, headers={'User-Agent': UserAgent})
            # AES 解密
            return AES.new(res.content, AES.MODE_CBC, res.content)
        else:
            return None

    def get_ts_url(self):
        for seg in self.m3u8_obj.segments:
            yield urljoin(self.m3u8_obj.base_uri, seg.uri)

    def download_ts(self, url_info):
        """
        下载ts文件，写入时如果有加密需要解密
        """
        url, ts_name = url_info
        res = requests.get(url, headers={'User-Agent': UserAgent})
        with open(ts_name, 'wb') as fp:
            if self.cryptor is not None:
                fp.write(self.cryptor.decrypt(res.content))
            else:
                fp.write(res.content)

    def download_all_ts(self):
        ts_urls = self.get_ts_url()
        for index, ts_url in enumerate(ts_urls):
            self.thread_pool.submit(self.download_ts, [ts_url, f'{index}.ts'])
        # 此方式可能使视频合并时顺序错乱
        # for file in self.m3u8_obj.files:
        #     url = urljoin(self.m3u8_obj.base_uri, file)
        #     self.thread_pool.submit(self.download_ts, [url, url[url.rfind("/") + 1:]])
        self.thread_pool.shutdown()

    def run(self):
        # 如果是第一层M3U8文件，那么就获取第二层的url
        if self.m3u8_obj.playlists and self.m3u8_obj.data.get("playlists"):
            self.m3u8_url = urljoin(self.m3u8_obj.base_uri, self.m3u8_obj.data.get("playlists")[0]["uri"])
            self.__post_init__()
        if not self.m3u8_obj.segments or not self.m3u8_obj.files:
            raise ValueError("m3u8数据不正确，请检查")
        self.download_all_ts()
        ts_path = '*.ts'
        with open(self.file_name, 'wb') as fn:
            for ts in natsorted(iglob(ts_path)):
                with open(ts, 'rb') as ft:
                    sc_line = ft.read()
                    fn.write(sc_line)
        [os.remove(ts) for ts in iglob(ts_path)]
        if os.path.exists("key.key"):
            os.remove("key.key")


if __name__ == '__main__':
    # aHR0cHM6Ly93d3cuMTAyNHV1LmNjL3ZvZC9saXN0aW5nLTQtMC0wLTAtMC0wLTAtMC0wLTEuaHRtbA==
    m3u8_url = 'https://1400200613.vod2.myqcloud.com/d3af585bvodtranscq1400200613/409d704c5285890805550379503/drm/v.f230.m3u8?t=5f1d3c6f&us=5t9wmjjy&sign=87d3071959ad10baa14770dac55f63a3'
    file_name = 'ts01'
    os.chdir('./sup')

    start = time.time()

    M3U8 = DownLoadM3U8(m3u8_url, file_name)
    M3U8.run()

    end = time.time()
    print('耗时:', end - start)