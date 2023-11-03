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

class RuntimeinfoRunTimeInfo(object):
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
        'custom_image': 'RuntimeinfoCustomImageType',
        'resource_request': 'RuntimeinfoResourceRequest',
        'explicit_errors': 'bool',
        'random_seed': 'str'
    }

    attribute_map = {
        'custom_image': 'customImage',
        'resource_request': 'resourceRequest',
        'explicit_errors': 'explicitErrors',
        'random_seed': 'randomSeed'
    }

    def __init__(self, custom_image=None, resource_request=None, explicit_errors=None, random_seed=None):  # noqa: E501
        """RuntimeinfoRunTimeInfo - a model defined in Swagger"""  # noqa: E501
        self._custom_image = None
        self._resource_request = None
        self._explicit_errors = None
        self._random_seed = None
        self.discriminator = None
        if custom_image is not None:
            self.custom_image = custom_image
        if resource_request is not None:
            self.resource_request = resource_request
        if explicit_errors is not None:
            self.explicit_errors = explicit_errors
        if random_seed is not None:
            self.random_seed = random_seed

    @property
    def custom_image(self):
        """Gets the custom_image of this RuntimeinfoRunTimeInfo.  # noqa: E501


        :return: The custom_image of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :rtype: RuntimeinfoCustomImageType
        """
        return self._custom_image

    @custom_image.setter
    def custom_image(self, custom_image):
        """Sets the custom_image of this RuntimeinfoRunTimeInfo.


        :param custom_image: The custom_image of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :type: RuntimeinfoCustomImageType
        """

        self._custom_image = custom_image

    @property
    def resource_request(self):
        """Gets the resource_request of this RuntimeinfoRunTimeInfo.  # noqa: E501


        :return: The resource_request of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :rtype: RuntimeinfoResourceRequest
        """
        return self._resource_request

    @resource_request.setter
    def resource_request(self, resource_request):
        """Sets the resource_request of this RuntimeinfoRunTimeInfo.


        :param resource_request: The resource_request of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :type: RuntimeinfoResourceRequest
        """

        self._resource_request = resource_request

    @property
    def explicit_errors(self):
        """Gets the explicit_errors of this RuntimeinfoRunTimeInfo.  # noqa: E501

        Specifies whether the job will return silent errors. By default, this is set to false, and silent errors are not returned.  # noqa: E501

        :return: The explicit_errors of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :rtype: bool
        """
        return self._explicit_errors

    @explicit_errors.setter
    def explicit_errors(self, explicit_errors):
        """Sets the explicit_errors of this RuntimeinfoRunTimeInfo.

        Specifies whether the job will return silent errors. By default, this is set to false, and silent errors are not returned.  # noqa: E501

        :param explicit_errors: The explicit_errors of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :type: bool
        """

        self._explicit_errors = explicit_errors

    @property
    def random_seed(self):
        """Gets the random_seed of this RuntimeinfoRunTimeInfo.  # noqa: E501

        Random seed to use for the Job, so that Test Job result will be deterministic.  # noqa: E501

        :return: The random_seed of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :rtype: str
        """
        return self._random_seed

    @random_seed.setter
    def random_seed(self, random_seed):
        """Sets the random_seed of this RuntimeinfoRunTimeInfo.

        Random seed to use for the Job, so that Test Job result will be deterministic.  # noqa: E501

        :param random_seed: The random_seed of this RuntimeinfoRunTimeInfo.  # noqa: E501
        :type: str
        """

        self._random_seed = random_seed

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
        if issubclass(RuntimeinfoRunTimeInfo, dict):
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
        if not isinstance(other, RuntimeinfoRunTimeInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
