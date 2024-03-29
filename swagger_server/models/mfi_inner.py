# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
import re  # noqa: F401,E501
from swagger_server import util


class MfiInner(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: str=None, mfi: float=None):  # noqa: E501
        """MfiInner - a model defined in Swagger

        :param _date: The _date of this MfiInner.  # noqa: E501
        :type _date: str
        :param mfi: The mfi of this MfiInner.  # noqa: E501
        :type mfi: float
        """
        self.swagger_types = {
            '_date': str,
            'mfi': float
        }

        self.attribute_map = {
            '_date': 'Date',
            'mfi': 'mfi'
        }
        self.__date = _date
        self._mfi = mfi

    @classmethod
    def from_dict(cls, dikt) -> 'MfiInner':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The mfi_inner of this MfiInner.  # noqa: E501
        :rtype: MfiInner
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> str:
        """Gets the _date of this MfiInner.


        :return: The _date of this MfiInner.
        :rtype: str
        """
        return self.__date

    @_date.setter
    def _date(self, _date: str):
        """Sets the _date of this MfiInner.


        :param _date: The _date of this MfiInner.
        :type _date: str
        """

        self.__date = _date

    @property
    def mfi(self) -> float:
        """Gets the mfi of this MfiInner.


        :return: The mfi of this MfiInner.
        :rtype: float
        """
        return self._mfi

    @mfi.setter
    def mfi(self, mfi: float):
        """Sets the mfi of this MfiInner.


        :param mfi: The mfi of this MfiInner.
        :type mfi: float
        """

        self._mfi = mfi
