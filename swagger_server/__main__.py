#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_cors import CORS
from swagger_server.config import Config

""" def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Stock Indicator Analysis Open API'}, pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
 """
app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
CORS(app.app)
app.app.config.from_object(Config)

with app.app.app_context():
    app.add_api('swagger.yaml', arguments={'title': 'Stock Indicator Analysis Open API'}, pythonic_params=True)