from flask import Flask, render_template

from login_manager import login_manager, auth

from datalog import datalog

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager.init_app(app)

app.register_blueprint(datalog)

app.register_blueprint(auth)

# Rotas
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
