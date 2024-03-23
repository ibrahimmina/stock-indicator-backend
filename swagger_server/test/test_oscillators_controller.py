# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.cci import Cci  # noqa: E501
from swagger_server.models.cmf import Cmf  # noqa: E501
from swagger_server.models.efi import Efi  # noqa: E501
from swagger_server.models.macd import Macd  # noqa: E501
from swagger_server.models.mfi import Mfi  # noqa: E501
from swagger_server.models.obv import Obv  # noqa: E501
from swagger_server.models.ppo import Ppo  # noqa: E501
from swagger_server.models.psar import Psar  # noqa: E501
from swagger_server.models.pvo import Pvo  # noqa: E501
from swagger_server.models.roc import Roc  # noqa: E501
from swagger_server.models.rsi import Rsi  # noqa: E501
from swagger_server.models.stoch import Stoch  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOscillatorsController(BaseTestCase):
    """OscillatorsController integration test stubs"""

    def test_calculate_cci(self):
        """Test case for calculate_cci

        Used to help determine when an investment vehicle is reaching a condition of being overbought or oversold.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('length', 14),
                        ('cci_scaling_constant', 0.015)]
        response = self.client.open(
            '//cci',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_cmf(self):
        """Test case for calculate_cmf

        Chailin Money Flow measures the amount of money flow volume over a specific period in conjunction with Accumulation/Distribution.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('length', 20)]
        response = self.client.open(
            '//cmf',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_efi(self):
        """Test case for calculate_efi

        Elder's Force Index measures the power behind a price movement using price and volume as well as potential reversals and price corrections.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('length', 13),
                        ('drift', 1)]
        response = self.client.open(
            '//efi',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_macd(self):
        """Test case for calculate_macd

        The MACD is a popular indicator to that is used to identify a security's trend. While APO and MACD are the same calculation, MACD also returns two more series called Signal and Histogram. The Signal is an EMA of MACD and the Histogram is the difference of MACD and Signal.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('fast', 12),
                        ('slow', 26),
                        ('signal', 9)]
        response = self.client.open(
            '//macd',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_mfi(self):
        """Test case for calculate_mfi

        The Money Flow Index (MFI) is an oscillator that uses both price and volume to measure buying and selling pressure over a specified period of time.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('length', 14),
                        ('drift', 1)]
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
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile')]
        response = self.client.open(
            '//obv',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_ppo(self):
        """Test case for calculate_ppo

        The Percentage Price Oscillator is similar to MACD in measuring momentum.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('fast', 12),
                        ('slow', 26),
                        ('signal', 9),
                        ('scalar', 100)]
        response = self.client.open(
            '//ppo',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_psar(self):
        """Test case for calculate_psar

        An oscillator meaning that it operates between or within a set range of numbers or parameters..
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('initial_acceleration', 0.02),
                        ('acceleration', 0.02),
                        ('max_acceleration', 0.2)]
        response = self.client.open(
            '//psar',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_pvo(self):
        """Test case for calculate_pvo

        Percentage Volume Oscillator is a Momentum Oscillator for Volume.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('fast', 12),
                        ('slow', 26),
                        ('signal', 9),
                        ('scalar', 100)]
        response = self.client.open(
            '//pvo',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_roc(self):
        """Test case for calculate_roc

        Elder's Force Index measures the power behind a price movement using price and volume as well as potential reversals and price corrections.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('length', 1),
                        ('scalar', 100)]
        response = self.client.open(
            '//roc',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_rsi(self):
        """Test case for calculate_rsi

        The Relative Strength Index is popular momentum oscillator used to measure the velocity as well as the magnitude of directional price movements.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('length', 14),
                        ('scalar', 100),
                        ('drift', 1)]
        response = self.client.open(
            '//rsi',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calculate_stoch(self):
        """Test case for calculate_stoch

        The Stochastic Oscillator (STOCH) was developed by George Lane in the 1950's. He believed this indicator was a good way to measure momentum because changes in momentum precede changes in price.
        """
        query_string = [('symbol', 'symbol_example'),
                        ('period', 'period_example'),
                        ('multiplier', 1),
                        ('frontend', 'Mobile'),
                        ('fast', 14),
                        ('slow', 3),
                        ('smooth_k', 3)]
        response = self.client.open(
            '//stoch',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
