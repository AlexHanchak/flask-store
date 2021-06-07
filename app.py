from flask import Flask, render_template, request
from dotenv import dotenv_values
from flask_mysqldb import MySQL
import hashlib
import logging

app = Flask(__name__)
app.static_folder = 'static'
config = dotenv_values(".env")

mysql = MySQL(app)

payway = ['EUR', 'USD', 'RUB']
secretKey = 'SecretKey01'


def res(des, cur, payway):
    result = {
        "description": des,
        "payer_currency": int(643),
        "shop_amount": 23.15,
        "shop_currency": 643,
        "shop_id": 112,
        "shop_order_id": 4239,
        "payway": payway
    }
    hexn = [str(result['shop_amount']), str(result['shop_currency']), str(result['shop_id']),
            str(result['shop_order_id'])]
    hexsep = ':'.join(hexn)
    var = hexsep + secretKey
    encoded = var.encode()
    hexsha = hashlib.sha256(encoded)
    print(var)
    sa = hexsha.hexdigest()
    result['sign'] = sa
    return result


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['payway'] == 'EUR':
            s = res(request.form['description'], request.form['currency'], request.form['payway'])
            # Pays
            action = "https://pay.piastrix.com/en/pay"
            return render_template('form.html', amount=s['shop_amount'], currency=s['shop_currency'],
                                   shop_id=s['shop_id'], shop_order_id=s['shop_order_id'], sign=s['sign'],
                                   description=s['description'], action=action)
        if request.form['payway'] == 'USD':
            s = res(request.form['description'], request.form['currency'], request.form['payway'])
            # Bill Piastrix
            action = "https://core.piastrix.com/bill/create"
            return render_template('form.html', amount=s['shop_amount'], currency=s['shop_currency'],
                                   shop_id=s['shop_id'], shop_order_id=s['shop_order_id'], sign=s['sign'],
                                   description=s['description'], payer_currency=s['payer_currency'], action=action)
        if request.form['payway'] == 'RUB':
            # Invoice
            print(request.form)
            return render_template('form.html')
    if request.method == 'GET':
        return render_template('index.html', payway=payway)


if __name__ == "__main__":
    app.run()
