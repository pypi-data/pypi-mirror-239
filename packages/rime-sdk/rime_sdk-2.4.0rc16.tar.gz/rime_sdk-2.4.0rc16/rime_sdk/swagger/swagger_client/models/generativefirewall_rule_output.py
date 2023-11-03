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

class GenerativefirewallRuleOutput(object):
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
        'rule_name': 'str',
        'action': 'GenerativefirewallFirewallAction',
        'risk_category': 'RiskscoreRiskCategoryType'
    }

    attribute_map = {
        'rule_name': 'ruleName',
        'action': 'action',
        'risk_category': 'riskCategory'
    }

    def __init__(self, rule_name=None, action=None, risk_category=None):  # noqa: E501
        """GenerativefirewallRuleOutput - a model defined in Swagger"""  # noqa: E501
        self._rule_name = None
        self._action = None
        self._risk_category = None
        self.discriminator = None
        if rule_name is not None:
            self.rule_name = rule_name
        if action is not None:
            self.action = action
        if risk_category is not None:
            self.risk_category = risk_category

    @property
    def rule_name(self):
        """Gets the rule_name of this GenerativefirewallRuleOutput.  # noqa: E501


        :return: The rule_name of this GenerativefirewallRuleOutput.  # noqa: E501
        :rtype: str
        """
        return self._rule_name

    @rule_name.setter
    def rule_name(self, rule_name):
        """Sets the rule_name of this GenerativefirewallRuleOutput.


        :param rule_name: The rule_name of this GenerativefirewallRuleOutput.  # noqa: E501
        :type: str
        """

        self._rule_name = rule_name

    @property
    def action(self):
        """Gets the action of this GenerativefirewallRuleOutput.  # noqa: E501


        :return: The action of this GenerativefirewallRuleOutput.  # noqa: E501
        :rtype: GenerativefirewallFirewallAction
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this GenerativefirewallRuleOutput.


        :param action: The action of this GenerativefirewallRuleOutput.  # noqa: E501
        :type: GenerativefirewallFirewallAction
        """

        self._action = action

    @property
    def risk_category(self):
        """Gets the risk_category of this GenerativefirewallRuleOutput.  # noqa: E501


        :return: The risk_category of this GenerativefirewallRuleOutput.  # noqa: E501
        :rtype: RiskscoreRiskCategoryType
        """
        return self._risk_category

    @risk_category.setter
    def risk_category(self, risk_category):
        """Sets the risk_category of this GenerativefirewallRuleOutput.


        :param risk_category: The risk_category of this GenerativefirewallRuleOutput.  # noqa: E501
        :type: RiskscoreRiskCategoryType
        """

        self._risk_category = risk_category

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
        if issubclass(GenerativefirewallRuleOutput, dict):
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
        if not isinstance(other, GenerativefirewallRuleOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
