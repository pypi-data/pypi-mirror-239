# coding: utf-8
# -*- coding: utf-8 -*-
import base64

def encode_base64(string):
    byte = string.encode('utf-8')
    b64 = base64.b64encode(byte)
    result = b64.decode('utf-8')
    return result


def decode_base64(string):
    byte = string.encode('utf-8')
    b64 = base64.b64decode(byte)
    result = b64.decode('utf-8')
    return result

def love(how):
    if how == "limeng":
        print("""
          李猛李猛               李猛李猛
         李猛李猛李猛           李猛李猛李猛
       李猛李猛李猛李猛        李猛李猛李猛李猛
      李猛李猛李猛李猛李猛     李猛李猛李猛李猛李猛
     李猛李猛李猛李猛李猛李猛 李猛李猛李猛李猛李猛李猛
    李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛
      李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛
       李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛
        李猛李猛李猛李猛李猛李猛李猛李猛李猛李猛
         李猛李猛李猛李猛李猛李猛李猛李猛李猛
          李猛李猛李猛李猛李猛李猛李猛李猛
           李猛李猛李猛李猛李猛李猛李猛
            李猛李猛李猛李猛李猛李猛
             李猛李猛李猛李猛李猛
              李猛李猛李猛李猛
               李猛李猛李猛
                李猛李猛
                 李猛
        """)

def 输出(内容):
    print(内容)

def 输入(内容):
    input(内容)