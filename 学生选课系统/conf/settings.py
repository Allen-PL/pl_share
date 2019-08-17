import os
import logging.config
#各种文件的路径
BATH_DIR = os.path.dirname(os.path.dirname(__file__))
USERINFO_PATH = os.path.join(BATH_DIR, 'db', 'user_info')
COURSE_PATH = os.path.join(BATH_DIR, 'db', 'Course')
STUDENT_PATH = os.path.join(BATH_DIR, 'db', 'Student')
LOGGING_PATH = os.path.join(BATH_DIR, 'log', 'admin.log')
SIMPLE_FORMAT = '[%(asctime)s] %(message)s'

#配置日志的字典信息
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        
        'simple': {
            'format': SIMPLE_FORMAT,
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'simple',
            'filename': LOGGING_PATH,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['stream', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}





