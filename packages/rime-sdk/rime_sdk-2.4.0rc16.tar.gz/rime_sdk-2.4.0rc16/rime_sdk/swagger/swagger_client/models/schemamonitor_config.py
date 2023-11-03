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

class SchemamonitorConfig(object):
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
        'degradation': 'MonitorMetricDegradationConfig',
        'anomaly': 'MonitorAnomalyConfig'
    }

    attribute_map = {
        'degradation': 'degradation',
        'anomaly': 'anomaly'
    }

    def __init__(self, degradation=None, anomaly=None):  # noqa: E501
        """SchemamonitorConfig - a model defined in Swagger"""  # noqa: E501
        self._degradation = None
        self._anomaly = None
        self.discriminator = None
        if degradation is not None:
            self.degradation = degradation
        if anomaly is not None:
            self.anomaly = anomaly

    @property
    def degradation(self):
        """Gets the degradation of this SchemamonitorConfig.  # noqa: E501


        :return: The degradation of this SchemamonitorConfig.  # noqa: E501
        :rtype: MonitorMetricDegradationConfig
        """
        return self._degradation

    @degradation.setter
    def degradation(self, degradation):
        """Sets the degradation of this SchemamonitorConfig.


        :param degradation: The degradation of this SchemamonitorConfig.  # noqa: E501
        :type: MonitorMetricDegradationConfig
        """

        self._degradation = degradation

    @property
    def anomaly(self):
        """Gets the anomaly of this SchemamonitorConfig.  # noqa: E501


        :return: The anomaly of this SchemamonitorConfig.  # noqa: E501
        :rtype: MonitorAnomalyConfig
        """
        return self._anomaly

    @anomaly.setter
    def anomaly(self, anomaly):
        """Sets the anomaly of this SchemamonitorConfig.


        :param anomaly: The anomaly of this SchemamonitorConfig.  # noqa: E501
        :type: MonitorAnomalyConfig
        """

        self._anomaly = anomaly

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
        if issubclass(SchemamonitorConfig, dict):
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
        if not isinstance(other, SchemamonitorConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
