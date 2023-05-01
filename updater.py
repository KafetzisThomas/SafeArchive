#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os, requests

with requests.get("https://raw.githubusercontent.com/KafetzisThomas/SafeArchive/main/main.py") as rq:
  with open('main.py', 'wb') as file:
    file.write(rq.content)
    file.close()

os.startfile("main.py")
