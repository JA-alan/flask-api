from pymysql import cursors
import warnings
import pymysql
import setting

warnings.filterwarnings("ignore")


class Update_Sql(object):
    def __init__(self):
        """初始化"""

        self.connect = pymysql.connect(host=setting.host(),
                                       password=setting.psd(),
                                       user=setting.user(),
                                       db=setting.dbname(),
                                       charset='utf8',
                                       cursorclass=cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def data_update(self, token, name=None, age=None, character=None):
        """修改数据"""
        if character == '' or character is None:
            self.cursor.execute("update users set user ='{}' where user ='{}'".format(name, age))
            self.connect.commit()
            print("修改成功")
        elif token is None:
            return {"msg": "no_token"}
        else:
            self.cursor.execute(
                "update users inner join name_news on users.uid = name_news.uid set name_news.name = %s,"
                "name_news.`character` = %s,name_news.age = %s where users.token = %s",
                (name, character, age, token))
            self.connect.commit()
            return {"code": 200}

        self.cursor.close()
        self.connect.close()

    def logout_del_token(self, user):
        """退出登录清除token"""
        try:
            self.cursor.execute("update users inner join name_news on users.uid = name_news.uid "
                                "set users.token = '',name_news.token = '' where users.user = %s ", user)
            self.connect.commit()
        except Exception as e:
            return e

        finally:
            self.cursor.close()
            self.connect.close()

    def time_del_token(self):
        """定时清除token"""
        try:
            self.cursor.execute("update users inner join name_news on users.uid = name_news.uid "
                                "set users.token = '',name_news.token = '' "
                                "where DATE_SUB(NOW(),INTERVAL  10 MINUTE) > users.UpdateTime")
            self.connect.commit()
            print("ok")

        except Exception as error:
            return {"result": error}

        finally:
            self.cursor.close()
            self.connect.close()
