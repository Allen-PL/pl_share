import os
import sys

#将整个项目的路径加载到内存
BATH_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BATH_DIR)
from core import src
from core.src import Course
from core.src import Student

#程序启动入口
if __name__ == '__main__':
    src.main()
