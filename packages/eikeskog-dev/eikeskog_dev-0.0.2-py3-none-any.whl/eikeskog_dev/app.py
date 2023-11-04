#!/usr/bin/env python3

import os
from flask import Flask


########################################################################################################################


app = Flask(__name__)

@app.route('/', methods=['GET'])
def eikeskog():
    out = "eikeskog_dev"
    return out


########################################################################################################################


if __name__ == '__main__':
    FLASK_PORT = os.getenv("FLASK_PORT", 5555)
    app.run(host='0.0.0.0', port=FLASK_PORT)
