import sys
import os
import pickle
from lib import common
from conf import settings


class Base:
    
    def show_courses(self):
        with open(settings.COURSE_PATH, mode='rb') as f:
            num = 0
            while 1:
                try:
                    num += 1
                    obj = pickle.load(f)
                    print(f'{num}: {obj.name} {obj.price} {obj.period}')
                except EOFError:
                    break
    
    def exit(self):
        sys.exit(f'\033[0;32m感谢{self.name}使用选课系统！\033[0m')


class Student(Base):
    """
    学生类
    """
    operate_lst = [('查看可选课程', 'show_courses'),
                   ('选择课程', 'select_course'),
                   ('查看所选课程', 'show_selected_course'),
                   ('退出', 'exit')]
    
    def __init__(self, name):
        self.name = name
        self.courses = []
    
    def select_course(self):
        """选择课程"""
        self.show_courses()
        try:
            choice_num = input('\033[0;32m请输入要选择的课程序号：\033[0m').strip()
            with open(settings.COURSE_PATH, mode='rb') as f:
                for i in range(int(choice_num)):  # 根据输入的序号确定循环次数最终锁定选择的课程对象
                    obj = pickle.load(f)
                self.courses.append(obj)
            print(f'\033[0;32m您已经成功添加了{obj.name}课程\033[0m')
        
        except Exception:
            print('输入有误....')
    
    def show_selected_course(self):
        """查看所选课程"""
        print(f'\033[0;32m您已报名如下课程\033[0m')
        for obj_course in self.courses:
            print(f'\033[0;32m课程名：{obj_course.name}，课程价格：{obj_course.price} 课程周期：{obj_course.period}\033[0m')
    
    def exit(self):
        """退出之前要将学生选择的课程添加上"""
        with open(settings.STUDENT_PATH, mode='rb') as f1, \
                open(f'{settings.STUDENT_PATH}_bak', mode='wb') as f2:
            while 1:
                try:
                    obj = pickle.load(f1)
                    pickle.dump(self if obj.name == self.name else obj, f2)
                except EOFError:
                    break
        os.remove(settings.STUDENT_PATH)
        os.rename(f'{settings.STUDENT_PATH}_bak', settings.STUDENT_PATH)
        super().exit()
    
    @classmethod
    def get_obj(cls, username):
        """此方法是区别学生与管理员登录，学生登录就会去文件中取对象，管理员登录则直接userinfo获取管理员用户名密码"""
        with open(settings.STUDENT_PATH, mode='rb') as f1:
            while 1:
                try:
                    obj = pickle.load(f1)
                    if username == obj.name:
                        return obj
                except EOFError:
                    break


class Manager(Base):
    """
    管理员类
    """
    operate_lst = [('创建课程', 'create_course'),
                   ('创建学生', 'create_student'),
                   ('查看可选课程', 'show_courses'),
                   ('查看所有学生', 'show_students'),
                   ('查看所有学生选课情况', 'show_students_courses'),
                   ('退出', 'exit')]
    
    def __init__(self, name):
        self.name = name
    
    def create_course(self):
        """创建课程"""
        course = getattr(sys.modules[__name__], 'Course')
        name, price, period = input('请依次输入课程名，价格以及课程周期，以|分割').strip().split('|')
        obj = course(name, price, period)
        with open(settings.COURSE_PATH, mode='ab') as f1:
            pickle.dump(obj, f1)
        logger = common.record_logger()
        logger.info(f'成功创建{name}课程')
    
    def create_student(self):
        """创建学生"""
        student_username = input('\033[0;32m 请输入学生姓名：\033[0m').strip()
        student_password = input('\033[0;32m 请输入学生密码：\033[0m').strip()
        student_pwd_md5 = common.hashlib_md5(student_password)
        with open(settings.USERINFO_PATH, encoding='utf-8', mode='a') as f1:
            f1.write(f'\n{student_username}|{student_pwd_md5}|Student')
        with open(settings.STUDENT_PATH, mode='ab') as f:
            obj = getattr(sys.modules[__name__], 'Student')(student_username)
            pickle.dump(obj, f)
        logger = common.record_logger()
        logger.info(f'成功您已成功创建学生账号：{student_username},初始密码：{student_password}')
    
    def show_students(self):
        """查看所有学生"""
        with open(settings.STUDENT_PATH, mode='rb') as f1:
            while 1:
                try:
                    obj = pickle.load(f1)
                    print(obj.name)
                except EOFError:
                    break
    
    def show_students_courses(self):
        """查看所有学生选课情况"""
        with open(settings.STUDENT_PATH, mode='rb') as f1:
            while 1:
                try:
                    obj = pickle.load(f1)
                    print(f'\033[0;32m学生:{obj.name},所选课程：\
                    {["%s-%s-%s" %(course.name,course.price,course.period) for course in obj.courses]}\033[0m')
                except EOFError:
                    break
    
    def exit(self):
        """退出"""
        super().exit()
    
    @classmethod
    def get_obj(cls, username):
        return Manager(username)


class Course:
    def __init__(self, name, price, period):
        self.name = name
        self.price = price
        self.period = period
        self.teacher = None


def login():
    """登陆逻辑,此处是用了单次登陆验证，你也可以根据自己的需求改成三次登陆失败才返回False"""
    count = 1
    #只有三次的输入机会
    while count < 4:
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        pwd_md5 = common.hashlib_md5(password)
        with open(settings.USERINFO_PATH, encoding='utf-8') as f1:
            for line in f1:
                if not line.strip(): continue
                user, pwd, identify = line.strip().split('|')
                if user == username and pwd == pwd_md5:
                    return {'username': user, 'identify': identify, 'auth': True}
            else:
                print('用户名或者密码错误，请重新输入')
        count += 1
    return {'username': username, 'identify': None, 'auth': False}


def main():
    print('\033[0;32m欢迎访问选课系统，请先登录\033[0m')
    dict_auth = login()
    print(f"\033[0;32m登陆成功，欢迎{dict_auth['username']}，您的身份是{dict_auth['identify']}\033[0m")
    if dict_auth['auth']:
        '''根据不同的身份，进行相应的操作，利用反射'''
        if hasattr(sys.modules[__name__], dict_auth['identify']):
            cls = getattr(sys.modules[__name__], dict_auth['identify'])
        obj = cls.get_obj(dict_auth['username'])  # 管理员与学生都定义了此方法，鸭子类型。
        while 1:
            for num, option in enumerate(cls.operate_lst, 0):
                print(f'{num+1}: {option[0]}')
            choice_num = int(input('\033[0;32m 请输入选项：\033[0m').strip())
            getattr(obj, cls.operate_lst[choice_num - 1][1])()
    
    else:
        print('三次验证失败，系统自动退出')
        return False
