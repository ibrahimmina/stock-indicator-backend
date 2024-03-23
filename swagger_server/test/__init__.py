import logging

import connexion
from flask_testing import TestCase
from swagger_server.config import Config

from swagger_server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.app.config.from_object(Config)
        #app.add_api('swagger.yaml')

        with app.app.app_context():
            app.add_api('swagger.yaml', arguments={'title': 'Stock Indicator Analysis Open API'}, pythonic_params=True)

            return app.app
