from flask import Flask, send_file

app = Flask(__name__)


@app.route('/get_data')
def get_data():
    return send_file('data/data.xlsx')


app.run(host='0.0.0.0', port=5000)
