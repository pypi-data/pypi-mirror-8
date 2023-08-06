#!/usr/bin/python3

import requests
from .parser import *
from .exceptions import is_error, ExceptionFactory
from pprint import pprint

#disabling warnings about unverified SSL certificates
#as urllib3 is embedded, we don't have to worry about
#urllib3 being missing.
requests.packages.urllib3.disable_warnings()

def index(board, page=1):
  res = requests.get("https://api.archive.moe/index",
          stream=False, verify=False,
          params = {"board": board, "page": int(page)}).json()
  if is_error(res):
    raise ExceptionFactory.generateException(res)
  for thread_num in res:
    res[thread_num] = IndexResult(res[thread_num])
  return res 

def search(**kwargs):
  url = "https://api.archive.moe/search"
  #print("[api.search] url", url)
  #kwargs["board"]=board
  res = requests.get(url, stream=False, verify=False, params=kwargs).json()
  if is_error(res):
    raise ExceptionFactory.generateException(res)
  res = res[0]
  return [Post(post_obj) for post_obj in res["posts"]]

def thread(board, thread_num, latest_doc_id=-1, last_limit=-1):
  url = "https://api.archive.moe/thread"
  payload = {"board": board, "num": thread_num}
  if(latest_doc_id != -1):
    payload["latest_doc_id"] = (int(latest_doc_id))
  if(last_limit != -1):
    payload["last_limit"] = (int(last_limit))
  res = requests.get(url, stream=False, verify=False, params=payload).json()
  if is_error(res):
    raise ExceptionFactory.generateException(res)
  return Thread(res)

def post(board, post_num):
  res = requests.get("https://api.archive.moe/post", verify=False,  stream=False,
                  params={"board":board, "num":post_num}).json()
  if is_error(res):
    raise ExceptionFactory.generateException(res)
  return Post(res)
