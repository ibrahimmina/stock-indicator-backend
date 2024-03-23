# coding: utf-8

from __future__ import absolute_import

from flask import current_app, json
from six import BytesIO

from swagger_server.models.candlestick import Candlestick  # noqa: E501
from swagger_server.test import BaseTestCase
import os


class TestGeneralStockInfoController(BaseTestCase):
    """GeneralStockInfoController integration test stubs"""

    def test_calculate_candlestick_updated(self):
        """Test case for calculate_candlestick_updated

        The average price over the specified period
        """
        print(os.environ.get('api_key'))
        query_string = [('symbol', 'AAPL'),
                        ('period', 'minute'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile')]

        headers = {
            "X-API-KEY": "test",
            "Content-Type": "application/json",  # Add content type if needed
        }
        

        response = self.client.open(
            current_app.config['LOCALHOST']+'candlesticknew',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
