# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
import re  # noqa: F401,E501
from swagger_server import util


class MacdInner(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: str=None, macd: float=None, hist: float=None, sig: float=None):  # noqa: E501
        """MacdInner - a model defined in Swagger

        :param _date: The _date of this MacdInner.  # noqa: E501
        :type _date: str
        :param macd: The macd of this MacdInner.  # noqa: E501
        :type macd: float
        :param hist: The hist of this MacdInner.  # noqa: E501
        :type hist: float
        :param sig: The sig of this MacdInner.  # noqa: E501
        :type sig: float
        """
        self.swagger_types = {
            '_date': str,
            'macd': float,
            'hist': float,
            'sig': float
        }

        self.attribute_map = {
            '_date': 'Date',
            'macd': 'MACD',
            'hist': 'HIST',
            'sig': 'SIG'
        }
        self.__date = _date
        self._macd = macd
        self._hist = hist
        self._sig = sig

    @classmethod
    def from_dict(cls, dikt) -> 'MacdInner':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The macd_inner of this MacdInner.  # noqa: E501
        :rtype: MacdInner
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> str:
        """Gets the _date of this MacdInner.


        :return: The _date of this MacdInner.
        :rtype: str
        """
        return self.__date

    @_date.setter
    def _date(self, _date: str):
        """Sets the _date of this MacdInner.


        :param _date: The _date of this MacdInner.
        :type _date: str
        """

        self.__date = _date

    @property
    def macd(self) -> float:
        """Gets the macd of this MacdInner.


        :return: The macd of this MacdInner.
        :rtype: float
        """
        return self._macd

    @macd.setter
    def macd(self, macd: float):
        """Sets the macd of this MacdInner.


        :param macd: The macd of this MacdInner.
        :type macd: float
        """

        self._macd = macd

    @property
    def hist(self) -> float:
        """Gets the hist of this MacdInner.


        :return: The hist of this MacdInner.
        :rtype: float
        """
        return self._hist

    @hist.setter
    def hist(self, hist: float):
        """Sets the hist of this MacdInner.


        :param hist: The hist of this MacdInner.
        :type hist: float
        """

        self._hist = hist

    @property
    def sig(self) -> float:
        """Gets the sig of this MacdInner.


        :return: The sig of this MacdInner.
        :rtype: float
        """
        return self._sig

    @sig.setter
    def sig(self, sig: float):
        """Sets the sig of this MacdInner.


        :param sig: The sig of this MacdInner.
        :type sig: float
        """

        self._sig = sig
