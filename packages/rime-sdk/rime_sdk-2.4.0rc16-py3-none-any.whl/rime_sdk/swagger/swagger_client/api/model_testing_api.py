# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: dev@robustintelligence.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from rime_sdk.swagger.swagger_client.api_client import ApiClient


class ModelTestingApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def model_testing_get_latest_logs(self, job_id, **kwargs):  # noqa: E501
        """GetLatestLogs  # noqa: E501

        Returns the logs of the latest pod to run the test job with the specified job ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_get_latest_logs(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Uniquely specifies a Job. (required)
        :return: StreamResultOfRimeGetLatestLogsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.model_testing_get_latest_logs_with_http_info(job_id, **kwargs)  # noqa: E501
        else:
            (data) = self.model_testing_get_latest_logs_with_http_info(job_id, **kwargs)  # noqa: E501
            return data

    def model_testing_get_latest_logs_with_http_info(self, job_id, **kwargs):  # noqa: E501
        """GetLatestLogs  # noqa: E501

        Returns the logs of the latest pod to run the test job with the specified job ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_get_latest_logs_with_http_info(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Uniquely specifies a Job. (required)
        :return: StreamResultOfRimeGetLatestLogsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['job_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method model_testing_get_latest_logs" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `model_testing_get_latest_logs`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'job_id' in params:
            path_params['jobId'] = params['job_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['X-Firewall-Api-Key', 'X-Firewall-Auth-Token', 'rime-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1-beta/logs/{jobId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='StreamResultOfRimeGetLatestLogsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def model_testing_start_continuous_test(self, body, firewall_id_uuid, **kwargs):  # noqa: E501
        """StartContinuousTest  # noqa: E501

        Starts a Continuous Test and returns a Job object containing metadata for the Test Run.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_start_continuous_test(body, firewall_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ContinuoustestsFirewallIdUuidBody body: (required)
        :param str firewall_id_uuid: Unique object ID. (required)
        :return: RimeStartContinuousTestResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.model_testing_start_continuous_test_with_http_info(body, firewall_id_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.model_testing_start_continuous_test_with_http_info(body, firewall_id_uuid, **kwargs)  # noqa: E501
            return data

    def model_testing_start_continuous_test_with_http_info(self, body, firewall_id_uuid, **kwargs):  # noqa: E501
        """StartContinuousTest  # noqa: E501

        Starts a Continuous Test and returns a Job object containing metadata for the Test Run.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_start_continuous_test_with_http_info(body, firewall_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ContinuoustestsFirewallIdUuidBody body: (required)
        :param str firewall_id_uuid: Unique object ID. (required)
        :return: RimeStartContinuousTestResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'firewall_id_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method model_testing_start_continuous_test" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `model_testing_start_continuous_test`")  # noqa: E501
        # verify the required parameter 'firewall_id_uuid' is set
        if ('firewall_id_uuid' not in params or
                params['firewall_id_uuid'] is None):
            raise ValueError("Missing the required parameter `firewall_id_uuid` when calling `model_testing_start_continuous_test`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'firewall_id_uuid' in params:
            path_params['firewallId.uuid'] = params['firewall_id_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['X-Firewall-Api-Key', 'X-Firewall-Auth-Token', 'rime-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/continuous-tests/{firewallId.uuid}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeStartContinuousTestResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def model_testing_start_generative_stress_test(self, body, project_id_uuid, **kwargs):  # noqa: E501
        """StartGenerativeStressTest  # noqa: E501

        Starts a Generative Stress Test and returns a Job object containing metadata for the Test Run.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_start_generative_stress_test(body, project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GenerativestresstestsProjectIdUuidBody body: (required)
        :param str project_id_uuid: Unique object ID. (required)
        :return: RimeStartGenerativeStressTestResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.model_testing_start_generative_stress_test_with_http_info(body, project_id_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.model_testing_start_generative_stress_test_with_http_info(body, project_id_uuid, **kwargs)  # noqa: E501
            return data

    def model_testing_start_generative_stress_test_with_http_info(self, body, project_id_uuid, **kwargs):  # noqa: E501
        """StartGenerativeStressTest  # noqa: E501

        Starts a Generative Stress Test and returns a Job object containing metadata for the Test Run.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_start_generative_stress_test_with_http_info(body, project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GenerativestresstestsProjectIdUuidBody body: (required)
        :param str project_id_uuid: Unique object ID. (required)
        :return: RimeStartGenerativeStressTestResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'project_id_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method model_testing_start_generative_stress_test" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `model_testing_start_generative_stress_test`")  # noqa: E501
        # verify the required parameter 'project_id_uuid' is set
        if ('project_id_uuid' not in params or
                params['project_id_uuid'] is None):
            raise ValueError("Missing the required parameter `project_id_uuid` when calling `model_testing_start_generative_stress_test`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_id_uuid' in params:
            path_params['projectId.uuid'] = params['project_id_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['X-Firewall-Api-Key', 'X-Firewall-Auth-Token', 'rime-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1-beta/generative-stress-tests/{projectId.uuid}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeStartGenerativeStressTestResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def model_testing_start_stress_test(self, body, project_id_uuid, **kwargs):  # noqa: E501
        """StartStressTest  # noqa: E501

        Starts a Stress Test and returns a Job object containing metadata for the Test Run.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_start_stress_test(body, project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param StresstestsProjectIdUuidBody body: (required)
        :param str project_id_uuid: Unique object ID. (required)
        :return: RimeStartStressTestResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.model_testing_start_stress_test_with_http_info(body, project_id_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.model_testing_start_stress_test_with_http_info(body, project_id_uuid, **kwargs)  # noqa: E501
            return data

    def model_testing_start_stress_test_with_http_info(self, body, project_id_uuid, **kwargs):  # noqa: E501
        """StartStressTest  # noqa: E501

        Starts a Stress Test and returns a Job object containing metadata for the Test Run.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.model_testing_start_stress_test_with_http_info(body, project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param StresstestsProjectIdUuidBody body: (required)
        :param str project_id_uuid: Unique object ID. (required)
        :return: RimeStartStressTestResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'project_id_uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method model_testing_start_stress_test" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `model_testing_start_stress_test`")  # noqa: E501
        # verify the required parameter 'project_id_uuid' is set
        if ('project_id_uuid' not in params or
                params['project_id_uuid'] is None):
            raise ValueError("Missing the required parameter `project_id_uuid` when calling `model_testing_start_stress_test`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_id_uuid' in params:
            path_params['projectId.uuid'] = params['project_id_uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['X-Firewall-Api-Key', 'X-Firewall-Auth-Token', 'rime-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1/stress-tests/{projectId.uuid}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeStartStressTestResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
