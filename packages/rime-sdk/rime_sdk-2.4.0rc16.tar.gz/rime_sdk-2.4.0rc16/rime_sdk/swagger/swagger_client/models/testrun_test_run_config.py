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

class TestrunTestRunConfig(object):
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
        'run_name': 'str',
        'model_id': 'RimeUUID',
        'data_info': 'TestrunRefEvalDatasets',
        'run_time_info': 'RuntimeinfoRunTimeInfo',
        'profiling_config': 'TestrunProfilingConfig',
        'test_suite_config': 'TestrunTestSuiteConfig',
        'categories': 'list[TestrunTestCategoryType]'
    }

    attribute_map = {
        'run_name': 'runName',
        'model_id': 'modelId',
        'data_info': 'dataInfo',
        'run_time_info': 'runTimeInfo',
        'profiling_config': 'profilingConfig',
        'test_suite_config': 'testSuiteConfig',
        'categories': 'categories'
    }

    def __init__(self, run_name=None, model_id=None, data_info=None, run_time_info=None, profiling_config=None, test_suite_config=None, categories=None):  # noqa: E501
        """TestrunTestRunConfig - a model defined in Swagger"""  # noqa: E501
        self._run_name = None
        self._model_id = None
        self._data_info = None
        self._run_time_info = None
        self._profiling_config = None
        self._test_suite_config = None
        self._categories = None
        self.discriminator = None
        self.run_name = run_name
        self.model_id = model_id
        self.data_info = data_info
        if run_time_info is not None:
            self.run_time_info = run_time_info
        if profiling_config is not None:
            self.profiling_config = profiling_config
        if test_suite_config is not None:
            self.test_suite_config = test_suite_config
        if categories is not None:
            self.categories = categories

    @property
    def run_name(self):
        """Gets the run_name of this TestrunTestRunConfig.  # noqa: E501

        Name for this Test Run.  # noqa: E501

        :return: The run_name of this TestrunTestRunConfig.  # noqa: E501
        :rtype: str
        """
        return self._run_name

    @run_name.setter
    def run_name(self, run_name):
        """Sets the run_name of this TestrunTestRunConfig.

        Name for this Test Run.  # noqa: E501

        :param run_name: The run_name of this TestrunTestRunConfig.  # noqa: E501
        :type: str
        """
        if run_name is None:
            raise ValueError("Invalid value for `run_name`, must not be `None`")  # noqa: E501

        self._run_name = run_name

    @property
    def model_id(self):
        """Gets the model_id of this TestrunTestRunConfig.  # noqa: E501


        :return: The model_id of this TestrunTestRunConfig.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this TestrunTestRunConfig.


        :param model_id: The model_id of this TestrunTestRunConfig.  # noqa: E501
        :type: RimeUUID
        """
        if model_id is None:
            raise ValueError("Invalid value for `model_id`, must not be `None`")  # noqa: E501

        self._model_id = model_id

    @property
    def data_info(self):
        """Gets the data_info of this TestrunTestRunConfig.  # noqa: E501


        :return: The data_info of this TestrunTestRunConfig.  # noqa: E501
        :rtype: TestrunRefEvalDatasets
        """
        return self._data_info

    @data_info.setter
    def data_info(self, data_info):
        """Sets the data_info of this TestrunTestRunConfig.


        :param data_info: The data_info of this TestrunTestRunConfig.  # noqa: E501
        :type: TestrunRefEvalDatasets
        """
        if data_info is None:
            raise ValueError("Invalid value for `data_info`, must not be `None`")  # noqa: E501

        self._data_info = data_info

    @property
    def run_time_info(self):
        """Gets the run_time_info of this TestrunTestRunConfig.  # noqa: E501


        :return: The run_time_info of this TestrunTestRunConfig.  # noqa: E501
        :rtype: RuntimeinfoRunTimeInfo
        """
        return self._run_time_info

    @run_time_info.setter
    def run_time_info(self, run_time_info):
        """Sets the run_time_info of this TestrunTestRunConfig.


        :param run_time_info: The run_time_info of this TestrunTestRunConfig.  # noqa: E501
        :type: RuntimeinfoRunTimeInfo
        """

        self._run_time_info = run_time_info

    @property
    def profiling_config(self):
        """Gets the profiling_config of this TestrunTestRunConfig.  # noqa: E501


        :return: The profiling_config of this TestrunTestRunConfig.  # noqa: E501
        :rtype: TestrunProfilingConfig
        """
        return self._profiling_config

    @profiling_config.setter
    def profiling_config(self, profiling_config):
        """Sets the profiling_config of this TestrunTestRunConfig.


        :param profiling_config: The profiling_config of this TestrunTestRunConfig.  # noqa: E501
        :type: TestrunProfilingConfig
        """

        self._profiling_config = profiling_config

    @property
    def test_suite_config(self):
        """Gets the test_suite_config of this TestrunTestRunConfig.  # noqa: E501


        :return: The test_suite_config of this TestrunTestRunConfig.  # noqa: E501
        :rtype: TestrunTestSuiteConfig
        """
        return self._test_suite_config

    @test_suite_config.setter
    def test_suite_config(self, test_suite_config):
        """Sets the test_suite_config of this TestrunTestRunConfig.


        :param test_suite_config: The test_suite_config of this TestrunTestRunConfig.  # noqa: E501
        :type: TestrunTestSuiteConfig
        """

        self._test_suite_config = test_suite_config

    @property
    def categories(self):
        """Gets the categories of this TestrunTestRunConfig.  # noqa: E501

        List of test categories to be run.  # noqa: E501

        :return: The categories of this TestrunTestRunConfig.  # noqa: E501
        :rtype: list[TestrunTestCategoryType]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this TestrunTestRunConfig.

        List of test categories to be run.  # noqa: E501

        :param categories: The categories of this TestrunTestRunConfig.  # noqa: E501
        :type: list[TestrunTestCategoryType]
        """

        self._categories = categories

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
        if issubclass(TestrunTestRunConfig, dict):
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
        if not isinstance(other, TestrunTestRunConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
