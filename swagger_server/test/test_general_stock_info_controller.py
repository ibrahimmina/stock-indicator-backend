# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.candlestick import Candlestick  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGeneralStockInfoController(BaseTestCase):
    """GeneralStockInfoController integration test stubs"""

    def test_calculate_candlestick(self):
        """Test case for calculate_candlestick

        The average price over the specified period
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2)]
        response = self.client.open(
            '//candlestick',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
