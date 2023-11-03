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

class GenerativestresstestsProjectIdUuidBody(object):
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
        'project_id': 'object',
        'test_run_config': 'TestrunGenerativeTestRunConfig',
        'agent_id': 'RimeUUID'
    }

    attribute_map = {
        'project_id': 'projectId',
        'test_run_config': 'testRunConfig',
        'agent_id': 'agentId'
    }

    def __init__(self, project_id=None, test_run_config=None, agent_id=None):  # noqa: E501
        """GenerativestresstestsProjectIdUuidBody - a model defined in Swagger"""  # noqa: E501
        self._project_id = None
        self._test_run_config = None
        self._agent_id = None
        self.discriminator = None
        if project_id is not None:
            self.project_id = project_id
        if test_run_config is not None:
            self.test_run_config = test_run_config
        if agent_id is not None:
            self.agent_id = agent_id

    @property
    def project_id(self):
        """Gets the project_id of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501

        Uniquely specifies a Project.  # noqa: E501

        :return: The project_id of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501
        :rtype: object
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this GenerativestresstestsProjectIdUuidBody.

        Uniquely specifies a Project.  # noqa: E501

        :param project_id: The project_id of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501
        :type: object
        """

        self._project_id = project_id

    @property
    def test_run_config(self):
        """Gets the test_run_config of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501


        :return: The test_run_config of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501
        :rtype: TestrunGenerativeTestRunConfig
        """
        return self._test_run_config

    @test_run_config.setter
    def test_run_config(self, test_run_config):
        """Sets the test_run_config of this GenerativestresstestsProjectIdUuidBody.


        :param test_run_config: The test_run_config of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501
        :type: TestrunGenerativeTestRunConfig
        """

        self._test_run_config = test_run_config

    @property
    def agent_id(self):
        """Gets the agent_id of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501


        :return: The agent_id of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._agent_id

    @agent_id.setter
    def agent_id(self, agent_id):
        """Sets the agent_id of this GenerativestresstestsProjectIdUuidBody.


        :param agent_id: The agent_id of this GenerativestresstestsProjectIdUuidBody.  # noqa: E501
        :type: RimeUUID
        """

        self._agent_id = agent_id

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
        if issubclass(GenerativestresstestsProjectIdUuidBody, dict):
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
        if not isinstance(other, GenerativestresstestsProjectIdUuidBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
