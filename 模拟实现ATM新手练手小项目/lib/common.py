#__*__coding:utf-8__*__
"""
时间：2019/8/4
作者：pl
功能：模拟一个ATM系统
"""
from logging import config
from conf.settings import DB_PATH
import os
import logging

def wrapper(f):
	"""
	装饰器，在登录某些功能的时候需要先进行登录操作
	:param f: 执行的功能函数
	:return: 返回功能函数的返回值
	"""
	def inner(login,dic_login_flag):
		#判断传入的标志位是否登录
		if dic_login_flag["login_flag"] == False:
			login()
			#登录自动返回
			if dic_login_flag["login_flag"] == True:
				ret = f()
				return ret
		#没有登录就执行登录
		else:
			ret = f()
			return ret
	return inner



def get_logger(username):
	"""
	功能介绍：这个函数实现的就是日志的记录功能，这个是日志的标准化模板。
	具体的介绍请访问我的blog查看:https://www.chpl.top
	:param username:
	:return:
	"""
	# 定义三种日志输出格式 开始

	# standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
	#                   '[%(levelname)s][%(message)s]' #其中name为getlogger指定的名字

	simple_format = f'{username}在 %(asctime)s %(message)s'

	# id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

	# # log文件的全路径
	# logfile_path = log_path

	# log配置字典
	LOGGING_DIC = {'version': 1, 'disable_existing_loggers': False, 'formatters': {# 'standard': {
		#     'format': standard_format
		# },
		'simple': {'format': simple_format}, }, 'filters': {}, 'handlers': {# 打印到终端的日志
		'stream': {'level': 'INFO', 'class': 'logging.StreamHandler',  # 打印到屏幕
			'formatter': 'simple'}, # 打印到文件的日志,收集info及以上的日志
		'file': {'level': 'INFO', 'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
			'formatter': 'simple', 'filename': None,  # 日志文件
			'maxBytes': 1024 * 1024 * 1024,  # 日志大小 5M
			'backupCount': 5, 'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
		}, }, 'loggers': {# logging.getLogger(__name__)拿到的logger配置
		'': {# 'handlers': ['stream', 'file'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
			'handlers': ['file'], 'level': 'INFO', 'propagate': True,  # 向上（更高level的logger）传递
		}, }, }

	path = os.path.join(DB_PATH, username + '.log')
	LOGGING_DIC['handlers']['file']['filename'] = path
	config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
	logger = logging.getLogger(__name__)  # 生成一个log实例
	return logger






