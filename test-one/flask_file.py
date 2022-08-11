from flask import Flask, render_template
app = Flask(__name__)
app.debug = True


@app.route('/index')
def index():
    return render_template('register.html')


if __name__ == "__main__":
    app.run()
