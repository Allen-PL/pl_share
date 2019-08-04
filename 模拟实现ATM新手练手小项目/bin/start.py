#__*__coding:utf-8__*__
"""
时间：2019/8/4
作者：pl
功能：模拟一个ATM系统
"""
import os
import sys

#这两行代码就是把当前目录上两级的目录加载到内存，不然我们就不能在平行文件之间调用py文件了。
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

#这个就是启动文件，启动只指向了core.src文件下的run()函数
from core.src import run
if __name__ == '__main__':
   run()












