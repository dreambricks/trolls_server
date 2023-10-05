from flask import Flask, render_template, send_file, request

from login_manager import login_manager, auth

from datalog import datalog

from udp_sender import UDPSender

import qrcode
import io
import parameters as pm

udp_sender1 = UDPSender()

app = Flask(__name__)
app.config.from_pyfile('config.py')

login_manager.init_app(app)

app.register_blueprint(datalog)

app.register_blueprint(auth)


# Rotas
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/term-accept')
def terms_accept():
    udp_sender1.send("yes")
    return render_template('terms-answer.html')


@app.route('/term-notaccept')
def terms_notaccept():
    udp_sender1.send("no")
    return render_template('terms-answer.html')


@app.route('/qrcode')
def gerar_qrcode():
    # Obtenha o link do parâmetro da consulta na URL.
    link = pm.BASE_URL

    # Crie um objeto QRCode com o link fornecido.
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Crie uma imagem do QRCode.
    img = qr.make_image(fill_color="black", back_color="white")

    # Salve a imagem em um objeto de bytes.
    img_bytes = io.BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)

    return send_file(img_bytes, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
