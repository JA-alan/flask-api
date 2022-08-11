from pymysql import cursors
import warnings
import pymysql
import setting
import global_setting
warnings.filterwarnings("ignore")


class Del_SQL(object):
    def __init__(self):
        """初始化"""

        self.connect = pymysql.connect(host=setting.host(),
                                       password=setting.psd(),
                                       user=setting.user(),
                                       db=setting.dbname(),
                                       charset='utf8',
                                       cursorclass=cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def data_delete(self, user=None, psd=None):
        """删除数据"""
        try:
            global_setting.dojob()
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
                    print("删除成功1")
                elif user is not values:
                    print("用户不存在")
        except Exception as e:
            print("错误，", e)
        finally:
            self.cursor.close()
            self.connect.close()
