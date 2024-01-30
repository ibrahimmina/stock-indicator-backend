# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
import re  # noqa: F401,E501
from swagger_server import util


class CmfInner(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: str=None, cmf: float=None):  # noqa: E501
        """CmfInner - a model defined in Swagger

        :param _date: The _date of this CmfInner.  # noqa: E501
        :type _date: str
        :param cmf: The cmf of this CmfInner.  # noqa: E501
        :type cmf: float
        """
        self.swagger_types = {
            '_date': str,
            'cmf': float
        }

        self.attribute_map = {
            '_date': 'Date',
            'cmf': 'cmf'
        }
        self.__date = _date
        self._cmf = cmf

    @classmethod
    def from_dict(cls, dikt) -> 'CmfInner':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The cmf_inner of this CmfInner.  # noqa: E501
        :rtype: CmfInner
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> str:
        """Gets the _date of this CmfInner.


        :return: The _date of this CmfInner.
        :rtype: str
        """
        return self.__date

    @_date.setter
    def _date(self, _date: str):
        """Sets the _date of this CmfInner.


        :param _date: The _date of this CmfInner.
        :type _date: str
        """

        self.__date = _date

    @property
    def cmf(self) -> float:
        """Gets the cmf of this CmfInner.


        :return: The cmf of this CmfInner.
        :rtype: float
        """
        return self._cmf

    @cmf.setter
    def cmf(self, cmf: float):
        """Sets the cmf of this CmfInner.


        :param cmf: The cmf of this CmfInner.
        :type cmf: float
        """

        self._cmf = cmf