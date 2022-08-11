import logging
import random
from pymysql import cursors
import warnings
import pymysql
import setting
from sel_db import Select_Sql
from global_setting import inset_token
import global_setting

warnings.filterwarnings("ignore")


class Inset_Sql(object):
    def __init__(self):
        """初始化"""
        self.connect = pymysql.connect(host=setting.host(),
                                       password=setting.psd(),
                                       user=setting.user(),
                                       db=setting.dbname(),
                                       charset='utf8',
                                       cursorclass=cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def insert_user(self, user, psd):
        """注册users表"""
        try:
            insert_sql = """
            insert into users(user,password,md5password,user_type,uid)
                values(%s,%s,%s,%s,%s)
            """

            user_info = '2'
            if user is None:
                return {"msg": "用户名为空"}
            # elif phone is None:
            #     return {"msg": "name为空"}
            self.cursor.execute("select user from users where user = %s", user)
            data = self.cursor.fetchall()
            # self.cursor.execute("select phone from users where phone = %s", phone)
            # data1 = self.cursor.fetchall()

            if len(data) > 0:
                return {"msg": "账号相同"}
            # elif len(data1) > 0:
            #     return {"msg": "手机号相同"}

            else:
                self.cursor.execute("select uid from users ORDER BY uid desc")
                cur_data = self.cursor.fetchall()
                sql_data = cur_data[0]
                values = sql_data["uid"]
                values = values + 1
                inset_md5 = global_setting.inset_md5(psd)
                self.cursor.execute(insert_sql, (user, psd, inset_md5, user_info, values))
                self.connect.commit()
                return {"code": 200}

        except Exception as e:
            logging.info(e)
            return {"msg": "插入失败"}
        finally:
            self.cursor.close()
            self.connect.close()

    def insert_news(self, name, age=18, sex=1, character=None):
        """注册news表"""
        try:
            insert_sql = """
            insert into name_news(name,age,sex,`character`,money,uid)
                values(%s,%s,%s,%s,%s,%s)
            """
            if character is None:
                character = "此人很无聊,没有个性签名"
            money1 = random.uniform(1, 100)
            money = round(money1, 2)
            # name = '张三'
            self.cursor.execute("select uid from name_news ORDER BY uid desc")
            cur_data = self.cursor.fetchall()
            sql_data = cur_data[0]
            values = sql_data["uid"]
            values = values + 1
            self.cursor.execute(insert_sql, (name, age, sex, character, money, values))
            self.connect.commit()

        except Exception as e:
            return {"code": "500"}
        finally:
            self.cursor.close()
            self.connect.close()

    def token_data(self, token, user):
        """储存token"""
        try:
            self.cursor.execute("update users inner join name_news on users.uid = name_news.uid "
                                "set users.token = %s,name_news.token = %s where user = %s ", (token, token, user))
            self.connect.commit()
        except Exception as e:
            return e

        finally:
            self.cursor.close()
            self.connect.close()

    def save_message(self, user, msg, token):
        """存消息"""
        try:
            data = Select_Sql().check_users_token(user, token)

            self.cursor.execute(
                "SELECT * FROM user_message WHERE create_time > DATE_SUB(NOW(),INTERVAL  5 MINUTE)"
                " and user = %s ORDER BY Create_Time DESC",
                user)
            result = self.cursor.fetchall()
            if data == {'return_code': '200'}:
                insert_sql = """
                            insert into user_message(uid, user,msg_id,name,message)
                                values(%s,%s,%s,%s,%s)
                            """
                self.cursor.execute("select uid from users where user = %s", user)
                cur_data = self.cursor.fetchall()[0]
                sql_data = cur_data["uid"]

                self.cursor.execute("select name from name_news where token = %s", token)
                cur_data1 = self.cursor.fetchall()[0]
                sql_data1 = cur_data1["name"]
                MSG= "MSG"
                MSG = MSG + inset_token().upper()
                msg_id = MSG
                if result is None:
                    self.cursor.execute(insert_sql, (sql_data, user, msg_id, sql_data1, msg))
                    self.connect.commit()
                    return {"code": 200}
                elif len(result) == 0:
                    self.cursor.execute(insert_sql, (sql_data, user, msg_id, sql_data1, msg))
                    self.connect.commit()
                    return {"code": 200}
                else:
                    return {"msg": "重复"}
            elif data == {'result': '!='}:
                return {'result': 'err_token'}
        except Exception as e:
            logging.info(e)
            return {"msg": "系统错误"}
        finally:
            self.cursor.close()
            self.connect.close()

    def save_article(self, user, token, head, msg):
        """存文章"""
        try:
            self.cursor.execute(
                "SELECT * FROM user_article WHERE create_time > DATE_SUB(NOW(),INTERVAL  5 MINUTE)"
                " and user = %s ORDER BY Create_Time DESC",
                user)
            result = self.cursor.fetchall()

            insert_sql = """
                        insert into user_article(uid, user,name,article_id,article_head,article_msg,label_id,look_type)
                            values(%s,%s,%s,%s,%s,%s,%s,%s)
                        """
            self.cursor.execute("select uid from users where user = %s", user)
            cur_data = self.cursor.fetchall()[0]
            sql_data = cur_data["uid"]

            self.cursor.execute("select name from name_news where token = %s", token)
            cur_data1 = self.cursor.fetchall()[0]
            sql_data1 = cur_data1["name"]
            ATL = "ATL"
            ATL = ATL + inset_token().upper()
            article_id = ATL
            look_type = 1
            label_id = None
            if result is None:
                self.cursor.execute(insert_sql, (sql_data, user, sql_data1, article_id, head, msg, label_id, look_type))
                self.connect.commit()
                return {"code": 200}
            elif len(result) == 0:
                self.cursor.execute(insert_sql, (sql_data, user, sql_data1, article_id, head, msg, label_id, look_type))
                self.connect.commit()
                return {"code": 200}
            else:
                return {"msg": "重复"}

        except Exception as e:
            logging.info(e)
            return {"msg": "系统错误"}
        finally:
            self.cursor.close()
            self.connect.close()
