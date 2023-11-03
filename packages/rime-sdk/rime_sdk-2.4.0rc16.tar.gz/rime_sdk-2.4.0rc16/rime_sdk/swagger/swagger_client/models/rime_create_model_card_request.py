# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: dev@robustintelligence.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class RimeCreateModelCardRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'model_card': 'RimeModelCard',
        'project_id': 'RimeUUID'
    }

    attribute_map = {
        'model_card': 'modelCard',
        'project_id': 'projectId'
    }

    def __init__(self, model_card=None, project_id=None):  # noqa: E501
        """RimeCreateModelCardRequest - a model defined in Swagger"""  # noqa: E501
        self._model_card = None
        self._project_id = None
        self.discriminator = None
        if model_card is not None:
            self.model_card = model_card
        if project_id is not None:
            self.project_id = project_id

    @property
    def model_card(self):
        """Gets the model_card of this RimeCreateModelCardRequest.  # noqa: E501


        :return: The model_card of this RimeCreateModelCardRequest.  # noqa: E501
        :rtype: RimeModelCard
        """
        return self._model_card

    @model_card.setter
    def model_card(self, model_card):
        """Sets the model_card of this RimeCreateModelCardRequest.


        :param model_card: The model_card of this RimeCreateModelCardRequest.  # noqa: E501
        :type: RimeModelCard
        """

        self._model_card = model_card

    @property
    def project_id(self):
        """Gets the project_id of this RimeCreateModelCardRequest.  # noqa: E501


        :return: The project_id of this RimeCreateModelCardRequest.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this RimeCreateModelCardRequest.


        :param project_id: The project_id of this RimeCreateModelCardRequest.  # noqa: E501
        :type: RimeUUID
        """

        self._project_id = project_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(RimeCreateModelCardRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RimeCreateModelCardRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
