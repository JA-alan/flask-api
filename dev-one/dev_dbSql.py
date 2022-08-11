import json
import random
from pymysql import cursors
import warnings
import pymysql
import pandas as pd

global cur_data
import hashlib

warnings.filterwarnings("ignore")


def inset_user():
    """造数据"""
    import random
    user = ''
    user1 = ['周', '赵', '钱', '孙', '李', '朱', '吴', '郑', '王', '张', '谢', '麦', '冯', '刘', '汤', '熊']
    user2 = ['春', '兰', '怀', '雅', '琪', '安', '子', '发', '若', '正', '耀', '让', '俊', '要', '梓', '浩']
    user3 = ['玉', '建', '嚄', '宇', '玲', '满', '曼', '末', '旺', '卫', '才', '伟', '从', '峰', '费', '坤']
    user1 = random.choice(user1)[0]
    user += user1
    user2 = random.choice(user2)[0]
    user += user2
    user3 = random.choice(user3)[0]
    user += user3
    sex = [1, 0]
    age = random.randint(18, 40)
    c = random.choice(sex)
    DB_SQL().insert_news(user, c, age)


class DB_SQL(object):
    def __init__(self):
        """初始化"""
        self.host = "43.138.182.131"
        self.username = "test-root"
        self.password = "asd123456"
        self.db_name = "test-root"

        self.connect = pymysql.connect(host=self.host,
                                       password=self.password,
                                       user=self.username,
                                       db=self.db_name,
                                       charset='utf8',
                                       cursorclass=cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def start_sql(self):
        self.cursor.execute(
            "CREATE TABLE test_time(CreateTime datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT 创建时间;)"
        )
        self.connect.commit()

    def insert_user(self, user, psd, phone):
        """注册user表"""
        try:
            insert_sql = """
            insert into users(user,password,phone,md5password,user_type,uid)
                values(%s,%s,%s,%s,%s,%s)
            """
            m = hashlib.md5()
            b = psd.encode(encoding='utf-8')
            m.update(b)
            md5_psd = m.hexdigest()
            user_type = '2'

            self.cursor.execute("select user from users where user = %s", user)
            result = self.cursor.fetchall()
            result1 = result[0]
            if user == result1:
                return "账号相同"

            else:
                self.cursor.execute("select uid from users ORDER BY uid desc")
                cur_data = self.cursor.fetchall()
                sql_data = cur_data[0]
                values = sql_data["uid"]
                values = values + 1

                self.cursor.execute(insert_sql, (user, psd, phone, md5_psd, user_type, values))
                self.connect.commit()
                print("添加成功")

        except Exception as e:
            return "插入失败"
        finally:
            self.cursor.close()
            self.connect.close()

    def insert_news(self, name=None, age=18, sex=1, character=None):
        """注册news表"""
        try:
            insert_sql = """
            insert into news(name,age,sex,`character`,money)
                values(%s,%s,%s,%s,%s)
            """
            if character is None:
                character = "此人很无聊,没有个性签名"
            money1 = random.uniform(1, 100)
            money = round(money1, 2)
            # name = '张三'
            self.cursor.execute(insert_sql, (name, age, sex, character, money))
            self.connect.commit()
            print("添加成功")

        except Exception as e:
            print("插入失败", e)
        finally:
            self.cursor.close()
            self.connect.close()

    def data_select(self, name=None):
        """查询数据"""
        try:
            if name == '' or name is None:

                # self.cursor.execute("select uid,user,phone from users;")
                self.cursor.execute("select users.uid 用户编号,users.user 用户名,news.name,"
                                    "用户名称, news.age年龄,news.sex 性别,""news.character 个性签名,"
                                    "news.money 余额," "users.phone 手机号,users.user_type 用户类型,")
                result = self.cursor.fetchall()

                print("查询全部成功")
                cols = self.cursor.description
                col = []
                for i in cols:
                    col.append(i[0])
                Msql = pd.DataFrame(result, columns=col)
                return result
            elif name == name:
                self.cursor.execute(
                    "select news.name 名字, users.phone 手机,news.age 年龄,news.sex 性别, news.character 个性签名 "
                    "from users INNER JOIN news  on user = %s where users.uid = news.uid",
                    name)

                print("单独查询成功")
                result = self.cursor.fetchall()

                cols = self.cursor.description
                col = []
                for i in cols:
                    col.append(i[0])
                Msql = pd.DataFrame(result, columns=col)
                print(Msql)

        except Exception as e:
            print("查询失败", e)
        finally:
            self.cursor.close()
            self.connect.close()

    def api_select(self, user, psd):
        """登录"""
        m = hashlib.md5()
        b = psd.encode(encoding='utf-8')
        m.update(b)
        md5_psd = m.hexdigest()
        self.cursor.execute(
            "select * from users where user = '{}' and md5password = '{}'".format(user, md5_psd))
        cur_data = self.cursor.fetchall()
        if len(cur_data) == 0:
            return {"code": 402, "result": "账号或密码错误"}

        if cur_data is not None:
            sql_data = cur_data[0]
            values = sql_data["user"]
            values1 = sql_data["md5password"]
            if user == values and md5_psd == values1:
                self.cursor.execute(
                    "select news.name,users.uid, users.phone,news.age,news.sex, news.character "
                    "from users INNER JOIN news  on users.user = %s where users.uid = news.uid",
                    user)
                relust = self.cursor.fetchall()
                relust = relust[0]
                return relust
            else:
                return {"code": "402", "result": "账号或密码错误"}

    def scp_select(self, name, key=None, expect=None):
        """校验用户名"""
        global cur_data
        try:
            if name is not None:
                cur = self.cursor
                cur.execute("select users.uid, news.name , users.phone ,news.age ,news.sex , news.character  "
                            "from users INNER JOIN news  on users.user = %s where users.uid = news.uid", (name))
                cur_data = cur.fetchall()
                return cur_data

        except Exception as e:
            print("FILL", e)
        finally:
            self.cursor.close()
            self.connect.close()

        if key is not None:  # 如果key不为空
            mysql_data = cur_data[0].get(key)
            self.data_delete(name)
            assert mysql_data == expect

    def select_all(self):
        """获取所有用户信息"""
        try:
            self.cursor.execute("select users.uid, news.name , users.phone ,news.age ,news.sex , news.character"
                                " from users INNER JOIN news  where users.uid = news.uid")
            result = self.cursor.fetchall()
            return result
        finally:
            self.cursor.close()
            self.connect.close()

    def login_add(self, user, psd):
        """登录"""
        try:
            m = hashlib.md5()
            b = psd.encode(encoding='utf-8')
            m.update(b)
            md5_psd = m.hexdigest()
            self.cursor.execute(
                "select * from users where user = '{}' and md5password = '{}';".format(user, md5_psd))
            cur_data = self.cursor.fetchall()
            if cur_data is not None:
                sql_data = cur_data[0]
                values = sql_data["user"]
                values1 = sql_data["md5password"]
                values2 = sql_data["user_type"]
                if user == values and md5_psd == values1:
                    print("校验成功")
                    return values2

                elif user != values or md5_psd != values1:
                    print("账号密码错误")

                else:
                    print("请求错误")
        except Exception as e:
            print("loginFILL", e)
            quit()

        finally:
            self.cursor.close()
            self.connect.close()

    def data_delete(self, user=None, psd=None):
        """删除数据"""

        try:
            self.cursor.execute("select * from users where user={} and password ={}".format(user, psd))
            sql_data = self.cursor.fetchall()
            if sql_data is not None:
                ept_data = sql_data[0]
                values = ept_data["user"]
                values1 = ept_data["password"]
                if user == values and psd == values1:
                    delete = "delete  from users WHERE user = %s;"
                    self.cursor.execute(delete, user)
                    self.connect.commit()
                    print("删除成功")
                elif user is not values:
                    print("用户不存在")
        except Exception as e:
            print("错误，", e)
        finally:
            self.cursor.close()
            self.connect.close()

    def data_update(self, token, name=None, age=None, character=None):
        """修改数据"""
        if character == '' or character is None:
            self.cursor.execute("update users set user ='{}' where user ='{}'".format(name, age))
            self.connect.commit()
            print("修改成功")
        else:
            self.cursor.execute("update users inner join news on users.uid = news.uid set news.name = %s,"
                                "news.`character` = %s,news.age = %s where users.token = %s",
                                (name, character, age, token))
            self.connect.commit()
            return {"code": 200}

        self.cursor.close()
        self.connect.close()

    def check_uid(self, uid):
        """退出登录"""
        try:
            self.cursor.execute("select uid from users where uid = %s", uid)
            data = self.cursor.fetchall()
            if len(data) == 0:
                return {"code": 200, "result": "no check"}
            result = data[0]
            result1 = result["uid"]
            if uid == result1:

                return {"code": 200, "result": "check"}
            elif uid != result1:
                return {"code": 200, "result": "no check"}

        except Exception as e:
            return e

        finally:
            self.cursor.close()
            self.connect.close()

    def token_data(self, token, user):
        """储存token"""
        try:
            self.cursor.execute("update users inner join news on users.uid = news.uid "
                                "set users.token = %s,news.token = %s where user = %s ", (token, token, user))
            self.connect.commit()
        except Exception as e:
            return e

        finally:
            self.cursor.close()
            self.connect.close()

    def check_users_token(self, token, user):
        """校验token"""
        try:
            self.cursor.execute("select token from users where user = %s", user)
            self.connect.commit()
            relues = self.cursor.fetchall()
            if len(relues) == 0:
                return json.dumps({'return_code': '400', 'return_info': '用户未登录'})
            result = relues[0]
            if token != result['token']:
                return {'result': '!='}

            else:
                return {'return_code': '200'}
        except Exception as e:
            return {'return_code': '400', 'return_info': '用户未登录', "data": e}

        finally:
            self.cursor.close()
            self.connect.close()

    def check_news_token(self, token):
        """校验token"""
        try:
            self.cursor.execute("select token from news where token = %s", token)
            self.connect.commit()
            relues = self.cursor.fetchall()
            if len(relues) == 0:
                return {'return_code': '400', 'return_info': '用户未登录'}
            result = relues[0]
            if token != result['token']:
                print("错误")
                quit()
            elif token == result['token']:
                return {'return_code': '200'}
        except Exception as e:
            return {'return_code': '400', 'return_info': '用户未登录', "data": e}

        finally:
            self.cursor.close()
            self.connect.close()

    def logout_del_token(self, user):
        """退出登录清除token"""
        try:
            self.cursor.execute("update users inner join news on users.uid = news.uid "
                                "set users.token = '',news.token = '' where users.user = %s ", user)
            self.connect.commit()
        except Exception as e:
            return e

        finally:
            self.cursor.close()
            self.connect.close()


a = DB_SQL
# a().check_uid("10012")
# a().check_users_token('611967828d75bc22ee8fd5784ef7df4e','jiangan')a().select_all()
# a().api_select('jiangan', 'asd1234')
# a().login_add('jiangan2', 'asd123')
# a().data_update("anan1", 'anan2')
# a().data_delete(2)
# a().data_select(4)
# aa = '1314520'  # 预期结果
# a().scp_select(1314520, key='user', expect=aa)

# #
# if __name__ == "__main__":
#     db = DB_SQL()
#     for re in range(40):
#         inset_user()
