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

class RegistryDataLoadingInfo(object):
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
        'path': 'str',
        'load_func_name': 'str',
        'loader_kwargs_json': 'str',
        'data_endpoint_integration_id': 'RimeUUID'
    }

    attribute_map = {
        'path': 'path',
        'load_func_name': 'loadFuncName',
        'loader_kwargs_json': 'loaderKwargsJson',
        'data_endpoint_integration_id': 'dataEndpointIntegrationId'
    }

    def __init__(self, path=None, load_func_name=None, loader_kwargs_json=None, data_endpoint_integration_id=None):  # noqa: E501
        """RegistryDataLoadingInfo - a model defined in Swagger"""  # noqa: E501
        self._path = None
        self._load_func_name = None
        self._loader_kwargs_json = None
        self._data_endpoint_integration_id = None
        self.discriminator = None
        self.path = path
        self.load_func_name = load_func_name
        if loader_kwargs_json is not None:
            self.loader_kwargs_json = loader_kwargs_json
        if data_endpoint_integration_id is not None:
            self.data_endpoint_integration_id = data_endpoint_integration_id

    @property
    def path(self):
        """Gets the path of this RegistryDataLoadingInfo.  # noqa: E501

        The path to the python file containing the data loading function.  # noqa: E501

        :return: The path of this RegistryDataLoadingInfo.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this RegistryDataLoadingInfo.

        The path to the python file containing the data loading function.  # noqa: E501

        :param path: The path of this RegistryDataLoadingInfo.  # noqa: E501
        :type: str
        """
        if path is None:
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501

        self._path = path

    @property
    def load_func_name(self):
        """Gets the load_func_name of this RegistryDataLoadingInfo.  # noqa: E501

        The name of the function that loads the data.  # noqa: E501

        :return: The load_func_name of this RegistryDataLoadingInfo.  # noqa: E501
        :rtype: str
        """
        return self._load_func_name

    @load_func_name.setter
    def load_func_name(self, load_func_name):
        """Sets the load_func_name of this RegistryDataLoadingInfo.

        The name of the function that loads the data.  # noqa: E501

        :param load_func_name: The load_func_name of this RegistryDataLoadingInfo.  # noqa: E501
        :type: str
        """
        if load_func_name is None:
            raise ValueError("Invalid value for `load_func_name`, must not be `None`")  # noqa: E501

        self._load_func_name = load_func_name

    @property
    def loader_kwargs_json(self):
        """Gets the loader_kwargs_json of this RegistryDataLoadingInfo.  # noqa: E501

        This is a JSON-serialized string from a map.  # noqa: E501

        :return: The loader_kwargs_json of this RegistryDataLoadingInfo.  # noqa: E501
        :rtype: str
        """
        return self._loader_kwargs_json

    @loader_kwargs_json.setter
    def loader_kwargs_json(self, loader_kwargs_json):
        """Sets the loader_kwargs_json of this RegistryDataLoadingInfo.

        This is a JSON-serialized string from a map.  # noqa: E501

        :param loader_kwargs_json: The loader_kwargs_json of this RegistryDataLoadingInfo.  # noqa: E501
        :type: str
        """

        self._loader_kwargs_json = loader_kwargs_json

    @property
    def data_endpoint_integration_id(self):
        """Gets the data_endpoint_integration_id of this RegistryDataLoadingInfo.  # noqa: E501


        :return: The data_endpoint_integration_id of this RegistryDataLoadingInfo.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._data_endpoint_integration_id

    @data_endpoint_integration_id.setter
    def data_endpoint_integration_id(self, data_endpoint_integration_id):
        """Sets the data_endpoint_integration_id of this RegistryDataLoadingInfo.


        :param data_endpoint_integration_id: The data_endpoint_integration_id of this RegistryDataLoadingInfo.  # noqa: E501
        :type: RimeUUID
        """

        self._data_endpoint_integration_id = data_endpoint_integration_id

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
        if issubclass(RegistryDataLoadingInfo, dict):
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
        if not isinstance(other, RegistryDataLoadingInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
