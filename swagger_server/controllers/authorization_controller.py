from typing import List
from connexion.exceptions import OAuthProblem
from flask import current_app
from polygon import exceptions as polygon_exceptions
from swagger_server.exceptions import CustomException

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""


TOKEN_DB = {current_app.config['API_KEY']: {"uid": 100}}

def check_ApiKeyAuth(api_key, required_scopes):

    info = TOKEN_DB.get(api_key, None)

    if not info:
        raise OAuthProblem("Invalid token")

    return info