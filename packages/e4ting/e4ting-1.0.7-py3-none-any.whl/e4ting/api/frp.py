#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :cdj test@qq.com 2023-07-26 23:23:00
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent

from jinja2 import Template

from e4ting.cache           import UUIDCache,FrpCache
from e4ting.cluster         import Cloud

class FRP():
    def __init__(self, uuid):
        self.uuid = uuid
        self.token = os.environ.get("FRP_TOKEN")

    def create(self):
        template = open("/code/etc/frpc_temp.ini").read()
        return Template(template).render(etc=self, frp=FrpCache(self.uuid))

    def push(self):
        if not FrpCache(self.uuid).exists():
            return True
        cloud = Cloud(remote="consul.e4ting.cn")
        @cloud.push(kv="{self.uuid}/etc/frpc.ini".format(self=self))
        def frp_etc():
            return self.create()
        return frp_etc()


