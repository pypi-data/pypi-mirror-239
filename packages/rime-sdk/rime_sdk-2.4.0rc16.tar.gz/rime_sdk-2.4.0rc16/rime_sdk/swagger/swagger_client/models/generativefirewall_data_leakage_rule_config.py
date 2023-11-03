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

class GenerativefirewallDataLeakageRuleConfig(object):
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
        'sensitive_terms_url': 'str'
    }

    attribute_map = {
        'sensitive_terms_url': 'sensitiveTermsUrl'
    }

    def __init__(self, sensitive_terms_url=None):  # noqa: E501
        """GenerativefirewallDataLeakageRuleConfig - a model defined in Swagger"""  # noqa: E501
        self._sensitive_terms_url = None
        self.discriminator = None
        if sensitive_terms_url is not None:
            self.sensitive_terms_url = sensitive_terms_url

    @property
    def sensitive_terms_url(self):
        """Gets the sensitive_terms_url of this GenerativefirewallDataLeakageRuleConfig.  # noqa: E501

        Sensitive terms URL describes the location of a text file containing the sensitive terms and expressions that should be blocked from the model output. If not provided, the Data Leakage rule will not run.  # noqa: E501

        :return: The sensitive_terms_url of this GenerativefirewallDataLeakageRuleConfig.  # noqa: E501
        :rtype: str
        """
        return self._sensitive_terms_url

    @sensitive_terms_url.setter
    def sensitive_terms_url(self, sensitive_terms_url):
        """Sets the sensitive_terms_url of this GenerativefirewallDataLeakageRuleConfig.

        Sensitive terms URL describes the location of a text file containing the sensitive terms and expressions that should be blocked from the model output. If not provided, the Data Leakage rule will not run.  # noqa: E501

        :param sensitive_terms_url: The sensitive_terms_url of this GenerativefirewallDataLeakageRuleConfig.  # noqa: E501
        :type: str
        """

        self._sensitive_terms_url = sensitive_terms_url

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
        if issubclass(GenerativefirewallDataLeakageRuleConfig, dict):
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
        if not isinstance(other, GenerativefirewallDataLeakageRuleConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
