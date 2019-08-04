#__*__coding:utf-8__*__
"""
时间：2019/8/4
作者：pl
功能：模拟一个ATM系统
"""
import os
import tabulate
import hashlib
import json

from conf.settings import JSON_PATH
from conf import settings
from conf.settings import DB_PATH
from lib.common import wrapper,get_logger

#定义的一个全局的字典，login_flag记录登录的状态，username记录的是登录成功的用户名
dic_login_flag = {"login_flag":False,
                  "username":None,
                  }

def login():
	"""
	登录功能
	:return:
	"""
	count = 1
	list_db_userinfo = os.listdir(DB_PATH)
	flag = True
	#控制循环，进入登录，成功或者失败3次就退出循环
	while flag:
		#3次失败，退出登录系统回到ATM主界面
		if count > 3:
			print ("您已经3次登录失败，自动退出系统！")
			flag = False
			return False
		#进入登录系统
		print ("*****欢迎进入ATM登录系统界面*****")
		log_username = input("username:")
		#判断该用户名是否存在
		if log_username+'.json' in list_db_userinfo:
			db_userinnfo = os.path.join(DB_PATH,log_username+'.json')
			dic_info = {}
			with open(db_userinnfo,'r',encoding='utf-8') as fp:
				dic_info = json.load(fp)
			log_password = input("password:")
			md5 = hashlib.md5()
			md5.update(log_password.encode('utf-8'))
			#判断用户名和密码是否正确
			if log_username == dic_info["username"] and md5.hexdigest() == dic_info["password"]:
				print (f"欢迎{log_username}登录成功！")
				dic_login_flag["login_flag"] = True
				dic_login_flag["username"] = log_username
				flag = False
			else:
				print ("密码错误！")
				count += 1
		else:
			print ("该用户不存在。")
			count += 1

def register():
	"""
	注册用户
	:return:
	"""
	#查看文件夹下所有的文件名
	list_db_userinfo = os.listdir(DB_PATH)
	while True:
		print("*****欢迎进入ATM注册系统界面*****")
		print ("温馨提示：用户名只能含有字母数字不能含有特殊字符，密码长度在6与14个字符之间。")
		reg_username = input("username:")
		reg_password = input("password:")
		#判断输入的用户名是否存在
		if reg_username+'.json' not in list_db_userinfo:
			if reg_username.isalnum() == True  and 5 < reg_password.__len__() <15:
				md5 = hashlib.md5()
				md5.update(reg_password.encode('utf-8'))
				dic_userinfo = {"username":reg_username,"password":md5.hexdigest(),"money":0}
				userinfo_path = os.path.join(DB_PATH,reg_username+'.json')
				#将序列化数据写进db下对应自己用户名文件里面
				with open(userinfo_path,'w',encoding='utf-8') as fp:
					json.dump(dic_userinfo,fp)
				print ("注册成功!")
				break
			else:
				print("您输入的用户名或密码不规范，请按照提示注册。")
		else:
			print ("该用户已经存在，请重新注册。")

@wrapper
def see_balane():
	"""
	查看余额
	:return:
	"""
	username_path = os.path.join(DB_PATH,dic_login_flag["username"]+".json")
	with open(username_path,'r',encoding='utf-8') as fp:
		dic_info = json.load(fp)
	print ("*******************")
	print (f"你的用户余额为:\n{dic_info['money']}")
	print("*******************")
	#把查看的日志写进log下的日志文件夹，但是我写进了db里面。
	logger = get_logger(dic_login_flag["username"])
	logger.info('查看账户余额')  # 记录该文件的运行状态

@wrapper
def save_money():
	"""
	存钱
	:return:
	"""
	dic_info = os.path.join(DB_PATH,dic_login_flag["username"]+'.json')
	money = input("请输入你存入的金额：")
	if money.isdecimal():
		with open(dic_info,'r',encoding='utf-8') as fp:
			dic = json.load(fp)
		dic["money"] = int(money) +int(dic["money"])
		with open(dic_info,'w',encoding='utf-8') as f:
			json.dump(dic,f)
		print ("存钱成功！")
		logger = get_logger(dic_login_flag["username"])
		logger.info(f'存入账户{money}￥')  # 记录该文件的运行状态


@wrapper
def transfer_accounts():
	"""
	转账
	:return:
	"""
	passive_user = input("请输入被转账方的用户名：")
	print("*******************")
	list_json = os.listdir(DB_PATH)
	own_json = os.path.join(DB_PATH,dic_login_flag["username"]+'.json')
	#被转账的用户是否存在，同时被转账的用户不应该自己
	if passive_user+'.json' in list_json and passive_user != dic_login_flag["username"]:
		passive_path = os.path.join(DB_PATH,passive_user+'.json')
		with open(own_json,'r',encoding='utf-8') as fp:
			dic = json.load(fp)
		while True:
			turn_money = input("输入转账金额：")
			if turn_money.isdecimal():
				#自己的前是否够
				if int(turn_money) <= int(dic["money"]):
					count_money = 0
					#把钱加到对方账户同时减少自己账户的钱
					with open(passive_path,'r',encoding='utf-8') as f:
						passive_dic = json.load(f)
						count_money = int(passive_dic["money"]) +int(turn_money)
						passive_dic["money"] = count_money
					with open(passive_path, 'w', encoding='utf-8') as f1:
						json.dump(passive_dic,f1)
					with open(own_json,'w',encoding='utf-8') as f2:
						dic["money"] = int(dic["money"]) - int(turn_money)
						# print (dic)
						json.dump(dic,f2)
					print("转账成功。")
					#记录日志
					logger = get_logger(dic_login_flag["username"])
					logger.info(f'向{passive_user}成功转入{turn_money}￥')  # 记录该文件的运行状态
					break
				else:
					print ("金额不足。")
			else:
				print ("输入的字符未识别。")
	else:
		print ("被转账的用户不存在！")

@wrapper
def pipeline_record():
	"""
	查看用户流水
	:return:
	"""
	log_path = os.path.join(DB_PATH,dic_login_flag["username"]+'.log')
	f =  open(log_path,'r',encoding='utf-8')
	print (f"*****{dic_login_flag['username']}的日志记录*****")
	for i in f:
		print (i)
	print ("********************")


def logout():
	"""
	退出
	:return:
	"""
	return False

def menu():
	menu_bar = [[1, '登录'], [2, '注册'], [3, '查看余额'], [4, '存钱'], [5, '转账'], [6, '查看账户流水'], [7, '退出']]
	print("--------欢迎进入ATM机主界面-------")
	print(format(tabulate.tabulate(menu_bar, headers=["id", "功能"], tablefmt="grid")))
	print("****************************")

def run():
	"""
	主逻辑函数
	:return:
	"""
	#功能映射，将函数名和数字之间做映射封装到字典中
	dic_func = dict(enumerate([login,register,see_balane, save_money, transfer_accounts, pipeline_record, logout], 1))
	#进入循环，也就是进入ATM的页面选择系统
	while True:
		menu()
		user_select = input("请输入你的选项(id)：")
		if user_select.isdecimal():
			if int(user_select) in dic_func.keys():
				if int(user_select) in [1,2,7]:
					# re接收执行的函数的返回值
					re = dic_func[int(user_select)]()
				#登录成功才能进入以下的几个函数实现的功能
				else:
					#re接收执行的函数的返回值
					re = dic_func[int(user_select)](login,dic_login_flag)
					#如果返回False就退出循环，也就是退出程序
				if re == False:
					break
			else:
				print ("您输入的id有误，请重新输入。")
		else:
			print ("您输入的id有误，请重新输入。")























