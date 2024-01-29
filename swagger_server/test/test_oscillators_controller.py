# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.cci import Cci  # noqa: E501
from swagger_server.models.efi import Efi  # noqa: E501
from swagger_server.models.mfi import Mfi  # noqa: E501
from swagger_server.models.obv import Obv  # noqa: E501
from swagger_server.models.roc import Roc  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOscillatorsController(BaseTestCase):
    """OscillatorsController integration test stubs"""

    def test_calculate_cci(self):
        """Test case for calculate_cci

        Used to help determine when an investment vehicle is reaching a condition of being overbought or oversold.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 14),
                        ('cci_scaling_constant', 0.015)]
        response = self.client.open(
            '//cci',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_efi(self):
        """Test case for calculate_efi

        Elder's Force Index measures the power behind a price movement using price and volume as well as potential reversals and price corrections.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 1)]
        response = self.client.open(
            '//efi',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_mfi(self):
        """Test case for calculate_mfi

        The Money Flow Index (MFI) is an oscillator that uses both price and volume to measure buying and selling pressure over a specified period of time.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 1)]
        response = self.client.open(
            '//mfi',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_obv(self):
        """Test case for calculate_obv

        The Money Flow Index (MFI) is an oscillator that uses both price and volume to measure buying and selling pressure over a specified period of time.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2)]
        response = self.client.open(
            '//obv',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_roc(self):
        """Test case for calculate_roc

        Elder's Force Index measures the power behind a price movement using price and volume as well as potential reversals and price corrections.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 100)]
        response = self.client.open(
            '//roc',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
