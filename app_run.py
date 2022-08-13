from flask import Flask
from flask_test import bp
from global_setting import initialization_token, token_del
from setting import BASE_URL_test
from log.der_log import init_logging
app = Flask(__name__)
app.register_blueprint(bp)
app.debug = True
app.config['JSON_SORT_KEYS'] = False
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
app.config["JSON_AS_ASCII"] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"


if __name__ == '__main__':
    # init_logging()
    token_del()
    app.run(host=BASE_URL_test, port=6000)
