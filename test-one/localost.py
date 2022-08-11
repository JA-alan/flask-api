import time

import random
from inset_db import Inset_Sql


def random_phone():
    """随机获取手机号"""
    reu = ""
    reu1 = "1"
    cat_phone = ["32", "58", "31", "71", "55", "33", "47"]
    reu = reu + reu1
    cat_phone = random.choices(cat_phone)[0]
    reu = reu + cat_phone
    for i in range(8):
        num = str(random.randint(1, 9))
        reu += num
    return reu


def random_age():
    """随机获取年龄"""
    age = random.randint(18, 40)
    return age


def print_menu():
    """打印提示菜单信息"""
    print("=" * 25)
    print("\t~新款扣扣~")
    print("\t1: 注册")
    print("\t2: 登录")
    # print("\t2:删除账号")
    # print("\t3:修改学生信息")
    print("\t4:查找账号信息")
    # print("\t5:显示学生信息")

    print("\t0: 退出")
    print("=" * 25)


def VIP_user():
    infos = "1:注册|2:删除|3:修改|4:查找|5:显示|6:退出系统|7：登录|0：清空系统"
    print("1:注册|2:登录|3:修改|4:查找|5:显示|7：删除用户|8:退出系统|0：清空系统")


def login_user():
    """用户登录"""
    try:
        name = input("输入账号：")
        psd = input("输入密码： ")
        Inset_Sql().login_add(name, psd)
        Verification_Code = random.randint(1000, 10000)
        while int(input("请输入验证码\033[1;31;43m %a \033[0m：" % Verification_Code)) == Verification_Code:
            for i in range(0, 101, 2):
                time.sleep(0.1)
                d = i // 2
                if i == 100:
                    print("\r%s%% ☞ [%s]\n" % (i, '▇' * d), end="")
                else:
                    print("\r%s%% ☞ 登录中，请稍等^-^ [%s]" % (i, '▇' * d), end="")
            print("登录成功")
            print("\033[2;32;40m 欢迎%a登录扣扣 \033[0m".center(50, "-") % name)
            print("\033[2;31m 正在开发中，敬请期待！\033[0m".center(45, "-"))
            if Inset_Sql().login_add(name, psd) == "0":
                StudentSys().start()
            elif Inset_Sql().login_add(name, psd) == "1":
                pass
            else:
                StudentSys().start_1()

        else:  # 找到用户名，但密码错了
            print("验证码错误，登录失败")
            return login_user()

    except Exception as e:
        print("登录失败的原因是：%s" % e)


class StudentSys(object):

    # def __init__(self):
    #     # 实例属性
    #     self.infos = "1:注册|2:删除|3:修改|4:查找|5:显示|6:退出系统|7：登录|0：清空系统"

    def Registered_user(self):
        """注册用户"""

        name = input("注册用户名:")
        if len(name) < 6:
            print("用户名长度不能小于6")
            return self.Registered_user()
        phone = input("请添加手机号(不填为随机):")
        if phone == "":
            phone = random_phone()
        elif len(phone) > 11:
            phone = random_phone()
        psd = input("请输入密码:")
        if len(psd) < 6:
            print("密码长度不能小于6位")
            return self.Registered_user()
        elif psd == '123456' or psd == '123123':
            print("密码过于简单，请重新输入")
            return self.Registered_user()
        print("注册成功")
        self.Perfect_data()
        Inset_Sql().insert_user(name, psd, phone)

    def Perfect_data(self):
        """完善资料"""

        print("完善资料页")
        print('*' * 10)
        name = input("输入你的昵称：")
        age = int(input("输入你的年龄："))
        if 200 > age > 0:
            print("ok")
        else:
            print("输入正确的年龄")
            age = input(age)
            # return self.Perfect_data()
        sex = input("输入你的性别(1.男0.女)：")

        if sex == '男' or sex == "1":
            sex = 1
        elif sex == '女' or sex == "0":
            sex = 0
        else:
            print("性别输入错误")
            sex = input(sex)
        character = input("输入你的个性签名:")
        Inset_Sql().insert_news(name, age, sex, character)

    def delete_user(self):
        """删除用户"""
        try:
            print("\n")
            print("删除用户")
            print("~" * 50)
            del_name = input("输入你想删除的账号：")
            del_psd = input("输入该账号密码: ")
            Inset_Sql().data_delete(del_name, del_psd)
            print("用户{}删除成功".format(del_name))
        except Exception as e:
            print("FILL", e)

    def modify_info(self):
        print("\n")
        print("修改用户名")
        print("~" * 50)
        user = input("输入用户名")
        new_user = input("输入你想要修改的用户名")
        new_character = input("请输入想要修改的个性签名")
        Inset_Sql().data_update(new_user, user, new_character)

    def select_user(self):
        print("查找用户名")
        print("~" * 50)

        user = input("输入你要查找的用户名：")
        Inset_Sql().data_select(user)
        print("*操作*:1：修改用户，2：删除用户")
        play = input("输入你的操作: ")
        if play == "2":
            Inset_Sql().vip_delete(user)
        elif play == "1":
            self.modify_info()
        else:
            print("请输入正确的操作:")
            self.select_user()

    def start_1(self):
        print_menu()
        number = int(input("请按照上面的提示输入相应指令1:"))
        # 加载文件中保存的信息,加载到内存中
        print("\n\n")
        print("操作指令")
        print("~" * 50)
        # print(self.infos)
        print("~" * 50)
        # number = input("请按照上面的提示输入相应指令:")

        # 判断是否输入是纯的数字
        if number == 1:
            # 添加信息
            self.Registered_user()
        elif number == 4:  # 修改
            self.select_user()
        elif number == 2:
            # 登录
            login_user()
        elif number == 0:
            quit()
        else:
            print("请输入正确的编号!")
            self.start_1()

    def start(self):
        VIP_user()
        number = int(input("请按照上面的提示输入相应指令1:"))
        # 加载文件中保存的信息,加载到内存中
        while True:
            print("\n\n")
            print("操作指令")
            print("~" * 50)
            # print(self.infos)
            print("~" * 50)
            # number = input("请按照上面的提示输入相应指令:")

            # 判断是否输入是纯的数字
            if number == 1:
                # 添加信息
                self.Registered_user()
            elif number == 2:
                login_user()

            elif number == 3:  # 修改
                self.modify_info()
            elif number == 4:  # 查找
                self.select_user()
            elif number == 5:
                # 显示信息
                pass
            elif number == 7:
                # 登录
                self.delete_user()
            elif number == 8:
                break

            else:
                print("请输入正确的编号!")
                return self.start()


s = StudentSys()
s.start_1()
