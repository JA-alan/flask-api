import datetime
import json
import logging
from flask import request, jsonify, make_response, Response, Blueprint
from global_setting import inset_token
from update_db import Update_Sql
from sel_db import Select_Sql
from inset_db import Inset_Sql

bp = Blueprint("user", __name__, url_prefix="/auth")
bp.debug = True


@bp.route('/index', methods=['GET', 'POST'])  # 首页
def index():
    asd = {"code": 200}
    logging.info(asd)
    return jsonify({'return_code': '200', 'return_result': '操作成功', 'data': '欢迎来到这里'})


@bp.route('/logon/register', methods=['POST'])
def register():  # 注册
    user = request.form.get('user')
    password = request.form.get('password')
    name = request.form.get('name')
    if len(request.form) == 0:
        return not_request_parameters()
    elif len(request.form) < 3:
        return lack_request_parameters()
    elif len(request.form) > 3:
        return lack_request_parameters()
    result = Inset_Sql().insert_user(user, password)
    if result == {"msg": "账号相同"}:
        return {'return_code': '405', 'return_info': '账号%s已被注册' % user}

    elif result == {"msg": "手机号相同"}:
        return {'return_code': '405', 'return_info': '手机号%s已被注册' % name}

    elif result == {"msg": "插入失败"}:
        return Server_error()

    elif user is None:
        return jsonify({'return_code': '400', 'return_info': '用户名不能为空'})

    elif name is None:
        return jsonify({'return_code': '400', 'return_info': '昵称不能为空'})

    elif password is None:
        return jsonify({'return_code': '400', 'return_info': '手机号不能为空'})

    elif result == {"code": "500"}:
        return jsonify({"code": 500, "msg": "服务器错误"})

    elif result == {"code": 200}:
        Inset_Sql().insert_news(name)
        return_dict = {'return_code': '200', 'return_info': '注册成功', 'name': user}
        return jsonify(return_dict)
    else:
        return Server_error()


@bp.route('/login', methods=['GET', 'POST'])
def login():  # 登录

    if request.method == 'POST':
        name = request.form.get('user')
        password = request.form.get('password')
        return_dict = {}
        if len(request.form) == 0:
            return_dict['return_code'] = '5004'
            return_dict['return_info'] = '参数请求为空'
            return jsonify(return_dict)

        elif len(request.form) > 2:
            return_dict['return_code'] = '403'
            return_dict['return_info'] = '请求参数错误'
            return jsonify(return_dict)

        elif name is None:
            return_dict['return_code'] = '404'
            return_dict['return_info'] = '请求错误'
            return jsonify(return_dict)
        elif password is None:
            return_dict['return_code'] = '404'
            return_dict['return_info'] = '请求错误'
            return jsonify(return_dict)
        elif len(request.form) == 2:
            return_dict = {
                'return_code': '200',
                'return_info': '操作成功',
                'result': "用户 %s 登录成功" % name,
                "login_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "token": inset_token(),
                "data": Select_Sql().api_select(name, password)
            }
            now_token = return_dict["token"]
            Inset_Sql().token_data(now_token, name)
            #  initialization_token(name)  # TODO 定时清空TOKEN
            #  Del_SQL().data_delete(name)
            if return_dict["data"] == {"code": 402, "result": "账号或密码错误"}:
                return {"code": 402, "result": "账号或密码错误"}

            return Response(json.dumps(return_dict, default=str), mimetype='application/json')

        else:
            return Server_error()

    elif request.method == 'GET':
        get_data = request.args.to_dict()
        name = get_data.get('user')
        password = get_data.get('password')
        return_dict = {}
        if name is None:
            return_dict['return_code'] = '404'
            return_dict['return_info'] = '请求错误'
            return jsonify(return_dict)
        elif password is None:
            return_dict['return_code'] = '404'
            return_dict['return_info'] = '请求错误'
            return jsonify(return_dict)
        elif len(request.args) == 0:
            return_dict['return_code'] = '403'
            return_dict['return_info'] = '参数请求为空'
            return jsonify(return_dict)

        elif len(request.args) > 2:
            return_dict['return_code'] = '404'
            return_dict['return_info'] = '请求错误'
            return jsonify(return_dict)
        if len(request.args) == 2:
            return_dict = {
                'return_code': '200',
                'return_info': '操作成功',
                'result': "用户 %s 登录成功" % name,
                "login_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "token": inset_token(),
                "data": Select_Sql().api_select(name, password)
            }
            now_token = return_dict["token"]
            Inset_Sql().token_data(now_token, name)
            #  initialization_token(name)  # TODO 定时清空TOKEN
            #  Del_SQL().data_delete(name)
            if return_dict["data"] == {'code': '402', 'result': '账号或密码错误'}:
                return {"code": 402, "result": "账号或密码错误"}
            return jsonify(return_dict)

        else:
            return Server_error()


@bp.route('/logout', methods=['GET'])
def logout():  # 退出登录
    if request.method == 'GET':
        get_data = request.args.to_dict()
        user = get_data.get('user')
        token = get_data.get('token')
        if len(request.args) == 0:
            return not_request_parameters()
        elif len(request.args) < 2:
            return lack_request_parameters()
        elif len(request.args) > 2:
            return lack_request_parameters()
        if len(request.args) == 2:
            result = Select_Sql().check_users_token(user, token)
            if result == {'return_code': '200'}:
                Update_Sql().logout_del_token(user)
                return jsonify({'result': '%s成功退出登录' % user})
            elif result == {'return_code': '403'}:
                return User_not_login()
            elif result == {'result': '!='}:
                return User_not_login()
            elif result == {'return_code': '500'}:
                return Server_error()
        elif len(request.args) > 2:
            return lack_request_parameters()
        elif len(request.args) < 2:
            return lack_request_parameters()
        else:
            return Server_error()


@bp.route('/user/update', methods=['POST'])
def update_user_profile():  # 修改个人信息
    name = request.form.get('name')
    age = request.form.get('age')
    character = request.form.get('character')
    Token = request.form.get('token')
    if len(request.form) == 0:
        return not_request_parameters()
    elif len(request.form) < 4:
        return lack_request_parameters()
    elif len(request.form) > 4:
        return lack_request_parameters()
    result = Select_Sql().check_news_token(Token)
    if result == {'msg': "no_login"}:
        return User_not_login()
    elif result == {"msg": "err_token"}:
        return User_not_login()
    elif result == {"code": "500"}:
        return Server_error()
    elif result == {'return_code': '200'}:
        result = Update_Sql().data_update(Token, name, age, character)
        return_dict = {'return_code': '200', 'return_info': '修改成功'}
        if result == {"msg": "no_token"}:
            return User_not_login()
        return jsonify(return_dict)


@bp.route('/user/all/list', methods=['get'])  # 查询所有用户信息
def all_user_list():
    get_data = request.args.to_dict()
    uid = get_data.get('code')
    # file = request.files['file']  # 传递文件
    if len(request.args) == 0:
        return not_request_parameters()
    elif len(request.args) < 1:
        return lack_request_parameters()
    elif len(request.args) > 1:
        return lack_request_parameters()
    elif len(get_data) == 1:
        result = Select_Sql().check_uid(uid)
        if result == {"code": 200, "result": "check"}:
            result1 = {"return_code": 200, "return_result": "操作成功", "data": Select_Sql().select_all()}
            return Response(json.dumps(result1), mimetype='application/json')
            # return jsonify(result1)
        elif result == {"code": 200, "result": "no check"}:
            return jsonify({"return_code": "402", "return_info": "没有权限"})
        elif result == {"mes": "err"}:
            return Server_error()


@bp.route('/submit_message', methods=['POST'])  # 发布留言
def submit_message():
    user = request.form.get('user')
    msg = request.form.get('msg')
    token = request.form.get('token')
    if len(request.form) == 0:
        return not_request_parameters()
    elif len(request.form) < 3:
        return lack_request_parameters()
    elif len(request.form) > 3:
        return lack_request_parameters()
    elif len(request.form) == 3:
        result = Inset_Sql().save_message(user, msg, token)
        if result == {"code": 200}:
            return jsonify({"return_code": 200, "return_result": "操作成功"})
        elif result == {"msg": "重复"}:
            return jsonify({"return_code": 403, "return_result": "5分钟内不能重复"})
        elif result == {'result': 'err_token'}:
            return Server_error()
        elif result == {'msg': '系统错误'}:
            return Server_error()
    else:
        return Server_error()


@bp.route('/user/check/message', methods=['GET'])  # 查看留言
def check_user_message():
    get_data = request.args
    token = get_data.get('token')
    message_id = get_data.get('message_id')
    if len(request.args) == 0:
        return not_request_parameters()
    elif len(request.args) < 2:
        return lack_request_parameters()
    elif len(request.args) > 2:
        return lack_request_parameters()
    elif token is None:
        return User_not_login()
    elif message_id is None:
        return lack_request_parameters()
    else:
        result = Select_Sql().check_token(token)
        if result == {"code": 200}:
            result1 = Select_Sql().select_user_message(message_id)
            result_dict = {"return_code": 200, "return_result": "操作成功", "data": result1}
            if result1 == {"code": 400}:
                return lack_request_parameters()
            elif result1 == {"code": 500}:
                return Server_error()
            else:
                # return json.dumps(result_dict, default=str, ensure_ascii=False)
                return Response(json.dumps(result_dict, default=str), mimetype='application/json')
        elif result == {"code": 404}:
            return Server_error()
        elif result == {"code": 405}:
            return Server_error()
        else:
            return Server_error()


@bp.route('/user/article/save', methods=['POST'])  # 发布文章
def article_save():
    user = request.form.get('user')
    token = request.form.get('token')
    article_head = request.form.get('article_head')
    article_msg = request.form.get('article_msg')
    if len(request.form) == 0:
        return not_request_parameters()
    elif len(request.form) < 4:
        return lack_request_parameters()
    elif len(request.form) > 4:
        return lack_request_parameters()
    elif len(request.form) == 4:
        result = Select_Sql().check_users_token(user, token)
        if result == {'return_code': '200'}:
            result = Inset_Sql().save_article(user, token, article_head, article_msg)
            if result == {"code": 200}:
                return jsonify({"return_code": 200, "return_result": "操作成功"})
            elif result == {"msg": "重复"}:
                return jsonify({"return_code": 402, "return_result": "5分钟内不能重复"})
            elif result == {"msg": "系统错误"}:
                return Server_error()
            else:
                return Server_error()
        elif result == {'return_code': '403'}:
            return jsonify({"return_code": 403, "return_result": "用户不存在"})
        elif result == {'result': '!='}:
            return jsonify({"return_code": 400, "return_result": "用户未登录"})


@bp.route('/user/check/article', methods=['GET'])  # 查看文章详情
def select_article():
    get_data = request.args.to_dict()
    article_id = get_data.get("article_id")
    token = get_data.get("token")
    if len(request.args) == 0:
        return not_request_parameters()
    elif len(request.args) < 2:
        return lack_request_parameters()
    elif len(request.args) > 2:
        return lack_request_parameters()
    elif token is None:
        return User_not_login()
    elif article_id is None:
        return lack_request_parameters()
    elif len(request.args) == 2:
        result1 = Select_Sql().check_token(token)
        if result1 == {'code': 200}:
            result = Select_Sql().check_article(article_id)
            if result == {"code": 415}:
                return lack_request_parameters()
            elif result == {"code": 500}:
                return Server_error()
            else:
                return_dict = {"return_code": 200, "return_result": "操作成功",
                               "data": result}
                return Response(json.dumps(return_dict, default=str), mimetype='bplication/json')
                # return json.dumps(return_dict, default=str, ensure_ascii=False)
        elif result1 == {"code": 404}:
            return User_not_login()
        elif result1 == {"code": 405}:
            return User_not_login()
        else:
            return Server_error()
    else:
        return Server_error()


@bp.route("get/user/all", methods=["post"])
def get_user_all():
    user = request.form.get("user")
    token = request.form.get("token")
    if len(request.form) == 0:
        return not_request_parameters()
    elif len(request.form) < 2:
        return lack_request_parameters()
    elif len(request.form) > 2:
        return lack_request_parameters()
    elif len(request.form) == 2:
        result = Select_Sql().check_users_token(user, token)
        if result == {'return_code': '200'}:
            # return jsonify({"return_code": 200, "return_result": "操作成功","msg":Select_Sql().select_user_all(user)})
            redre_dict = {"return_code": 200, "return_result": "操作成功", "msg": Select_Sql().select_user_all(user)}
            return Response(json.dumps(redre_dict, default=str), mimetype='application/json')
        elif result == {"code": 200}:
            return jsonify({"return_code": 200, "return_result": "操作成功"})
        elif result == {"msg": "重复"}:
            return jsonify({"return_code": 402, "return_result": "5分钟内不能重复"})
        elif result == {"msg": "系统错误"}:
            return Server_error()
        elif result == {'return_code': '403'}:
            return jsonify({"return_code": 403, "return_result": "用户不存在"})
        elif result == {'result': '!='}:
            return jsonify({"return_code": 400, "return_result": "用户未登录"})


@bp.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


def lack_request_parameters():
    return jsonify({"return_code": 415, "return_result": "请求参数错误"})


def not_request_parameters():
    return jsonify({"return_code": 400, "return_result": "请求参数为空"})


def Server_error():
    return jsonify({"return_code": 500, "return_result": "服务器错误"})


def User_not_login():
    return jsonify({'return_code': '401', 'return_info': '用户未登录'})
