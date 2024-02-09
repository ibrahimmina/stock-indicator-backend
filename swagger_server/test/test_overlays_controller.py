# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.adl import Adl  # noqa: E501
from swagger_server.models.adx import Adx  # noqa: E501
from swagger_server.models.bollinger import Bollinger  # noqa: E501
from swagger_server.models.ema import Ema  # noqa: E501
from swagger_server.models.sma import Sma  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOverlaysController(BaseTestCase):
    """OverlaysController integration test stubs"""

    def test_calculate_adl(self):
        """Test case for calculate_adl

        Accumulation/Distribution indicator utilizes the relative position of the close to it's High-Low range with volume.  Then it is cumulated.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2)]
        response = self.client.open(
            '//adl',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_adx(self):
        """Test case for calculate_adx

        Average Directional Movement is meant to quantify trend strength by measuring the amount of movement in a single direction.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 14),
                        ('scalar', 100),
                        ('drift', 1),
                        ('lensig', 14)]
        response = self.client.open(
            '//adx',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_bollinger_bands(self):
        """Test case for calculate_bollinger_bands

        An oscillator meaning that it operates between or within a set range of numbers or parameters..
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 5),
                        ('standard_deviation', 2)]
        response = self.client.open(
            '//bollinger',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_ema(self):
        """Test case for calculate_ema

        The average price over the specified period
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 5)]
        response = self.client.open(
            '//ema',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_sma(self):
        """Test case for calculate_sma

        The average price over the specified period
        """
        query_string = [('symbol', 'symbol_example'),
                        ('start_date', 'start_date_example'),
                        ('period', 2),
                        ('length', 5)]
        response = self.client.open(
            '//sma',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
