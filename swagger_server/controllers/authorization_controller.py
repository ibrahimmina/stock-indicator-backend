from typing import List
from connexion.exceptions import OAuthProblem
import os

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""


TOKEN_DB = {os.environ.get('api_key'): {"uid": 100}}

def check_ApiKeyAuth(api_key, required_scopes):

    info = TOKEN_DB.get(api_key, None)

    if not info:
        raise OAuthProblem("Invalid token")

    return info


