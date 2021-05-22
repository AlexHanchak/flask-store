from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import hashlib


app = Flask(__name__)
app.static_folder = 'static'
app.config['MYSQl_HOST'] = 'localhost'
app.config['MYSQl_USER'] = 'lex'
app.config['MYSQl_PASSWORD'] = 'h4t8j6b2f5'
app.config['MYSQl_DB'] = 'web_store'

mysql = MySQL(app)

payway = ['EUR', 'USD', 'RUB']
secretKey = 'SecretKey01'


def res(des, cur, payway):
    result = {
                    "description": des,
                    "payer_currency": cur,
                    "shop_amount": "23.15",
                    "shop_currency": cur,
                    "shop_id": "112",
                    "shop_order_id": 4239,
                    "payway": payway
                }
    hexn = [str(result['shop_amount']), str(result['payer_currency']), str(result['payway']), str(result['shop_id']), str(result['shop_order_id'])]
    hexsep = ':'.join(hexn)
    var = hexsep + secretKey
    s = str(var)
    encoded = s.encode()
    hexsha = hashlib.sha256(encoded)
    sa = hexsha.hexdigest()
    result['sign'] = sa
    return result


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['payway'] == 'EUR':
            s = res(request.form['description'], request.form['currency'], request.form['payway'])
            # Pay
            # print(s)

            return render_template('index.html')
        if request.form['payway'] == 'USD':
            # Bill Piastrix
            print(request.form)
        if request.form['payway'] == 'RUB':
            # Invoice
            print(request.form)
            return render_template('form.html')
    if request.method == 'GET':
        return render_template('index.html', payway=payway)


if __name__ == "__main__":
    app.run()
