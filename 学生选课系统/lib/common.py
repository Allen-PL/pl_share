import hashlib
import logging.config
from conf.settings import LOGGING_DIC


def hashlib_md5(password):
    """密码加密"""
    ret = hashlib.md5()
    ret.update(password.encode('utf-8'))
    return ret.hexdigest()


def record_logger():
    """记录日志"""
    logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger()  # 生成一个log实例
    return logger


    
    
    
    