from flask import Flask, render_template

from login_manager import login_manager, auth

from datalog import datalog

from udp_sender import UDPSender

udp_sender1 = UDPSender()

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager.init_app(app)

app.register_blueprint(datalog)

app.register_blueprint(auth)

# Rotas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/term-accept')
def terms_accept():
    udp_sender1.send("yes")

@app.route('/term-notaccept')
def terms_notaccept():
    udp_sender1.send("no")


if __name__ == '__main__':
    app.run()
