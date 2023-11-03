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

class SchemadatacollectorPrediction(object):
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
        'datapoint_id': 'RimeUUID',
        'model_id': 'RimeUUID',
        'data_stream_id': 'RimeUUID',
        'prediction': 'str',
        'timestamp': 'datetime'
    }

    attribute_map = {
        'datapoint_id': 'datapointId',
        'model_id': 'modelId',
        'data_stream_id': 'dataStreamId',
        'prediction': 'prediction',
        'timestamp': 'timestamp'
    }

    def __init__(self, datapoint_id=None, model_id=None, data_stream_id=None, prediction=None, timestamp=None):  # noqa: E501
        """SchemadatacollectorPrediction - a model defined in Swagger"""  # noqa: E501
        self._datapoint_id = None
        self._model_id = None
        self._data_stream_id = None
        self._prediction = None
        self._timestamp = None
        self.discriminator = None
        if datapoint_id is not None:
            self.datapoint_id = datapoint_id
        if model_id is not None:
            self.model_id = model_id
        if data_stream_id is not None:
            self.data_stream_id = data_stream_id
        if prediction is not None:
            self.prediction = prediction
        if timestamp is not None:
            self.timestamp = timestamp

    @property
    def datapoint_id(self):
        """Gets the datapoint_id of this SchemadatacollectorPrediction.  # noqa: E501


        :return: The datapoint_id of this SchemadatacollectorPrediction.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._datapoint_id

    @datapoint_id.setter
    def datapoint_id(self, datapoint_id):
        """Sets the datapoint_id of this SchemadatacollectorPrediction.


        :param datapoint_id: The datapoint_id of this SchemadatacollectorPrediction.  # noqa: E501
        :type: RimeUUID
        """

        self._datapoint_id = datapoint_id

    @property
    def model_id(self):
        """Gets the model_id of this SchemadatacollectorPrediction.  # noqa: E501


        :return: The model_id of this SchemadatacollectorPrediction.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this SchemadatacollectorPrediction.


        :param model_id: The model_id of this SchemadatacollectorPrediction.  # noqa: E501
        :type: RimeUUID
        """

        self._model_id = model_id

    @property
    def data_stream_id(self):
        """Gets the data_stream_id of this SchemadatacollectorPrediction.  # noqa: E501


        :return: The data_stream_id of this SchemadatacollectorPrediction.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._data_stream_id

    @data_stream_id.setter
    def data_stream_id(self, data_stream_id):
        """Sets the data_stream_id of this SchemadatacollectorPrediction.


        :param data_stream_id: The data_stream_id of this SchemadatacollectorPrediction.  # noqa: E501
        :type: RimeUUID
        """

        self._data_stream_id = data_stream_id

    @property
    def prediction(self):
        """Gets the prediction of this SchemadatacollectorPrediction.  # noqa: E501


        :return: The prediction of this SchemadatacollectorPrediction.  # noqa: E501
        :rtype: str
        """
        return self._prediction

    @prediction.setter
    def prediction(self, prediction):
        """Sets the prediction of this SchemadatacollectorPrediction.


        :param prediction: The prediction of this SchemadatacollectorPrediction.  # noqa: E501
        :type: str
        """

        self._prediction = prediction

    @property
    def timestamp(self):
        """Gets the timestamp of this SchemadatacollectorPrediction.  # noqa: E501

        The timestamp of the datapoint is stored in the prediction for fast querying.  # noqa: E501

        :return: The timestamp of this SchemadatacollectorPrediction.  # noqa: E501
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this SchemadatacollectorPrediction.

        The timestamp of the datapoint is stored in the prediction for fast querying.  # noqa: E501

        :param timestamp: The timestamp of this SchemadatacollectorPrediction.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp

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
        if issubclass(SchemadatacollectorPrediction, dict):
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
        if not isinstance(other, SchemadatacollectorPrediction):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
