import logging
from pymysql import cursors
import warnings
import pymysql
import setting
import global_setting

warnings.filterwarnings("ignore")


class Select_Sql(object):
    def __init__(self):
        """初始化"""

        self.connect = pymysql.connect(host=setting.host(),
                                       password=setting.psd(),
                                       user=setting.user(),
                                       db=setting.dbname(),
                                       charset='utf8',
                                       cursorclass=cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def api_select(self, user, psd):
        """登录"""
        try:
            md5_psd = global_setting.inset_md5(psd)
            self.cursor.execute(
                "select * from `users` where user = %s and md5password = %s", (user, md5_psd))
            cur_data = self.cursor.fetchall()
            if len(cur_data) == 0:
                return {"code": 402, "result": "账号或密码错误"}

            if cur_data is not None:
                sql_data = cur_data[0]
                values = sql_data["user"]
                values1 = sql_data["md5password"]

                if user == values and md5_psd == values1:
                    self.cursor.execute(
                        "select name_news.name,users.uid, users.phone,name_news.age,name_news.sex, name_news.character "
                        "from users INNER JOIN name_news  on users.user = %s where users.uid = name_news.uid",
                        user)
                    relust = self.cursor.fetchall()[0]
                    return relust
                else:
                    return {"code": "402", "result": "账号或密码错误"}
            else:
                return {"code": "402", "result": "账号或密码错误"}
        except Exception as e:
            logging.info(e)
            return {"code": "402", "result": "账号或密码错误"}
        finally:
            self.cursor.close()
            self.connect.close()

    def select_all(self):
        """获取所有用户信息"""
        try:
            self.cursor.execute(
                "select users.uid, name_news.name , users.phone ,name_news.age ,name_news.sex , name_news.character"
                " from users INNER JOIN name_news  where users.uid = name_news.uid")
            result = self.cursor.fetchall()
            self.cursor.execute("select count(*) as number from users")
            number = self.cursor.fetchall()[0]["number"]
            count = {"count": number}

            return result, count
        finally:
            self.cursor.close()
            self.connect.close()

    def check_uid(self, uid):
        """校验uid"""
        try:

            self.cursor.execute("select uid from users where uid = %s", uid)
            data = self.cursor.fetchall()
            if len(data) == 0:
                return {"code": 200, "result": "no check"}
            result = data[0]
            result1 = result["uid"]
            if int(uid) == int(result1):
                return {"code": 200, "result": "check"}
            elif uid != result1:
                return {"code": 200, "result": "no check"}

        except Exception as e:
            logging.info(e)
            return {"mes": "err"}

        finally:
            self.cursor.close()
            self.connect.close()

    def check_user(self, user):
        """校验用户名"""
        try:
            self.cursor.execute("select user from users where user = %s", user)
            data = self.cursor.fetchall()[0]
            result = data["user"]
            if user == result:
                return {"code": 200}
        except Exception as e:
            logging.info(e)
            return {"mes": "err"}
        finally:
            self.cursor.close()
            self.connect.close()

    def check_token(self, token):
        """校验token"""
        try:
            self.cursor.execute("select token from users where token = %s", token)
            result = self.cursor.fetchall()
            if result is None:
                return {"code": 404}
            elif len(result) == 1:
                return {"code": 200}
            elif len(result) < 1:
                return {"code": 405}
            elif len(result) == 0:
                return {"code": 406}
        except Exception as e:
            logging.info(e)
            return {"code": 500}
        finally:
            self.cursor.close()
            self.connect.close()

    def check_users_token(self, user, token):
        """users校验token"""
        try:
            self.cursor.execute("select token from users where user = %s", user)
            result = self.cursor.fetchall()
            if len(result) == 0:
                return {'return_code': '403'}
            result = result[0]
            if token != result['token']:
                return {'result': '!='}
            else:
                return {'return_code': '200'}
        except Exception as e:
            logging.info(e)
            return {'return_code': '500'}

        finally:
            self.cursor.close()
            self.connect.close()

    def check_news_token(self, token):
        """name_news校验token"""
        try:
            self.cursor.execute("select token from name_news where token = %s", token)
            relues = self.cursor.fetchall()
            if len(relues) == 0:
                return {'msg': "no_login"}
            result = relues[0]
            if token != result['token']:
                return {"msg": "err_token"}
            elif token == result['token']:
                return {'return_code': '200'}
        except Exception as e:
            logging.info(e)
            return {"code": "500"}

        finally:
            self.cursor.close()
            self.connect.close()

    def check_article(self, article_id=None):
        """查看文章/详情"""
        try:
            self.cursor.execute("select * from user_article where look_type = 1")
            result1 = self.cursor.fetchall()
            self.cursor.execute("select count(*) as look from user_article where look_type = 1")
            number = self.cursor.fetchall()[0]["look"]
            look_type = {"count": number}
            if article_id is None:
                return result1, look_type
            elif len(article_id) == 0:
                return result1, look_type
            else:
                self.cursor.execute("select * from user_article where article_id = %s", article_id)
                result = self.cursor.fetchall()
                if result is None:
                    return {"code": 415}
                elif len(result) == 0:
                    return result
                else:
                    self.cursor.execute("select browse_number from user_article where article_id = %s", article_id)
                    data = self.cursor.fetchall()[0]
                    data1 = data['browse_number']
                    num = 1
                    if data1 is None:
                        self.cursor.execute("update user_article set browse_number = %s where article_id = %s",
                                            (num, article_id))
                        self.connect.commit()
                    elif data1 == 0:
                        self.cursor.execute("update user_article set browse_number = %s where article_id = %s",
                                            (num, article_id))
                        self.connect.commit()
                    elif data1 > 0:
                        num = data1 + 1
                        self.cursor.execute("update user_article set browse_number = %s where article_id = %s",
                                            (num, article_id))
                        self.connect.commit()
                        return result
        except Exception as e:
            logging.info(e)
            return {"code": 500}
        finally:
            self.cursor.close()
            self.connect.close()

    def select_user_message(self, msg_id=None):
        """查看留言/详情"""
        try:
            self.cursor.execute("select * from user_message where look_type = 1")
            result = self.cursor.fetchall()
            self.cursor.execute("select count(*) as look from user_message where look_type = 1")
            number = self.cursor.fetchall()[0]["look"]
            look_type = {"count": number}
            if msg_id is None:
                return result, look_type
            elif len(msg_id) == 0:
                return result, look_type
            elif msg_id is not None:
                self.cursor.execute("select * from user_message where msg_id = %s", msg_id)
                result = self.cursor.fetchall()
                return result
            else:
                return {"code": 400}
        except Exception as e:
            logging.info(e)
            return {"code": 500}
        finally:
            self.cursor.close()
            self.connect.close()

    def select_user_all(self, user):
        """查询用户所有信息"""
        try:
            self.cursor.execute(
                "select name_news.name,users.uid, users.phone,name_news.age,name_news.sex, name_news.character,"
                "users.CreateTime "
                "from users INNER JOIN name_news on users.user = %s where users.uid = name_news.uid", user)
            user_data = self.cursor.fetchall()[0]
            user_uid = user_data["uid"]

            self.cursor.execute(
                "select article_id,look_type,article_head,article_msg,label_id,"
                "browse_number,likes_number,collection_number,Photo,create_time "
                "from `test-root`.user_article where uid = %s", user_uid)
            user_article = self.cursor.fetchall()

            self.cursor.execute("select msg_id,look_type,Photo,message,create_time "
                                "from `test-root`.user_message where uid = %s", user_uid)
            user_msg = self.cursor.fetchall()

            user_dict = [user_data, user_article, user_msg]
            return user_dict
        except Exception as error:
            return error

        finally:
            self.cursor.close()
            self.connect.close()
