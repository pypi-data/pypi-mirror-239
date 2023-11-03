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

class ManagedImagePipRequirement(object):
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
        'name': 'str',
        'version_specifier': 'str'
    }

    attribute_map = {
        'name': 'name',
        'version_specifier': 'versionSpecifier'
    }

    def __init__(self, name=None, version_specifier=None):  # noqa: E501
        """ManagedImagePipRequirement - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._version_specifier = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if version_specifier is not None:
            self.version_specifier = version_specifier

    @property
    def name(self):
        """Gets the name of this ManagedImagePipRequirement.  # noqa: E501

        Name of the library.  # noqa: E501

        :return: The name of this ManagedImagePipRequirement.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ManagedImagePipRequirement.

        Name of the library.  # noqa: E501

        :param name: The name of this ManagedImagePipRequirement.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def version_specifier(self):
        """Gets the version_specifier of this ManagedImagePipRequirement.  # noqa: E501

        Specifier for a version of the library, see: https://www.python.org/dev/peps/pep-0440/#version-specifiers or https://peps.python.org/pep-0440/ for reference.  # noqa: E501

        :return: The version_specifier of this ManagedImagePipRequirement.  # noqa: E501
        :rtype: str
        """
        return self._version_specifier

    @version_specifier.setter
    def version_specifier(self, version_specifier):
        """Sets the version_specifier of this ManagedImagePipRequirement.

        Specifier for a version of the library, see: https://www.python.org/dev/peps/pep-0440/#version-specifiers or https://peps.python.org/pep-0440/ for reference.  # noqa: E501

        :param version_specifier: The version_specifier of this ManagedImagePipRequirement.  # noqa: E501
        :type: str
        """

        self._version_specifier = version_specifier

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
        if issubclass(ManagedImagePipRequirement, dict):
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
        if not isinstance(other, ManagedImagePipRequirement):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
