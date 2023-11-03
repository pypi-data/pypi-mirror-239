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


class JobReaderApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def job_reader_cancel_job(self, job_id, **kwargs):  # noqa: E501
        """CancelJob  # noqa: E501

        Cancels the job with the specified ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_cancel_job(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID of job to be cancelled. (required)
        :return: RimeCancelJobResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.job_reader_cancel_job_with_http_info(job_id, **kwargs)  # noqa: E501
        else:
            (data) = self.job_reader_cancel_job_with_http_info(job_id, **kwargs)  # noqa: E501
            return data

    def job_reader_cancel_job_with_http_info(self, job_id, **kwargs):  # noqa: E501
        """CancelJob  # noqa: E501

        Cancels the job with the specified ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_cancel_job_with_http_info(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID of job to be cancelled. (required)
        :return: RimeCancelJobResponse
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
                    " to method job_reader_cancel_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `job_reader_cancel_job`")  # noqa: E501

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
            '/v1/jobs/cancel/{jobId}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeCancelJobResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def job_reader_get_job(self, job_id, **kwargs):  # noqa: E501
        """GetJob  # noqa: E501

        Get a single job by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_get_job(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID (required)
        :param str view: Specifies how much information about the job to retrieve. The default behavior is the Basic view.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view.
        :return: RimeGetJobResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.job_reader_get_job_with_http_info(job_id, **kwargs)  # noqa: E501
        else:
            (data) = self.job_reader_get_job_with_http_info(job_id, **kwargs)  # noqa: E501
            return data

    def job_reader_get_job_with_http_info(self, job_id, **kwargs):  # noqa: E501
        """GetJob  # noqa: E501

        Get a single job by ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_get_job_with_http_info(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID (required)
        :param str view: Specifies how much information about the job to retrieve. The default behavior is the Basic view.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view.
        :return: RimeGetJobResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['job_id', 'view']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method job_reader_get_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `job_reader_get_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'job_id' in params:
            path_params['jobId'] = params['job_id']  # noqa: E501

        query_params = []
        if 'view' in params:
            query_params.append(('view', params['view']))  # noqa: E501

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
            '/v1/jobs/{jobId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeGetJobResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def job_reader_get_project_id(self, job_id, **kwargs):  # noqa: E501
        """GetProjectID  # noqa: E501

        Returns the project ID of the project running the job with the specified job ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_get_project_id(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID belonging to the project. (required)
        :return: RimeGetProjectIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.job_reader_get_project_id_with_http_info(job_id, **kwargs)  # noqa: E501
        else:
            (data) = self.job_reader_get_project_id_with_http_info(job_id, **kwargs)  # noqa: E501
            return data

    def job_reader_get_project_id_with_http_info(self, job_id, **kwargs):  # noqa: E501
        """GetProjectID  # noqa: E501

        Returns the project ID of the project running the job with the specified job ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_get_project_id_with_http_info(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID belonging to the project. (required)
        :return: RimeGetProjectIDResponse
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
                    " to method job_reader_get_project_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `job_reader_get_project_id`")  # noqa: E501

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
            '/v1/jobs/{jobId}/project-id', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeGetProjectIDResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def job_reader_get_test_run_id(self, job_id, **kwargs):  # noqa: E501
        """GetTestRunID  # noqa: E501

        Returns a test run ID based on a specified job ID. The job ID must be for a completed stress test job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_get_test_run_id(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID associated with the test run. (required)
        :return: RimeGetTestRunIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.job_reader_get_test_run_id_with_http_info(job_id, **kwargs)  # noqa: E501
        else:
            (data) = self.job_reader_get_test_run_id_with_http_info(job_id, **kwargs)  # noqa: E501
            return data

    def job_reader_get_test_run_id_with_http_info(self, job_id, **kwargs):  # noqa: E501
        """GetTestRunID  # noqa: E501

        Returns a test run ID based on a specified job ID. The job ID must be for a completed stress test job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_get_test_run_id_with_http_info(job_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str job_id: Unique job ID associated with the test run. (required)
        :return: RimeGetTestRunIDResponse
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
                    " to method job_reader_get_test_run_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'job_id' is set
        if ('job_id' not in params or
                params['job_id'] is None):
            raise ValueError("Missing the required parameter `job_id` when calling `job_reader_get_test_run_id`")  # noqa: E501

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
            '/v1/jobs/{jobId}/test-run-id', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeGetTestRunIDResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def job_reader_list_jobs_for_project(self, project_id_uuid, **kwargs):  # noqa: E501
        """ListJobsForProject  # noqa: E501

        Returns a paginated list of jobs for a given project. The list can be filtered by job type and status.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_list_jobs_for_project(project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id_uuid: Unique object ID. (required)
        :param list[str] first_page_query_selected_statuses: Specifies a set of statuses. The query only returns results with a status in the specified set. Specify no statuses to return all results.   - JOB_STATUS_PENDING: Resources have been created for the job but the job has not started yet.  - JOB_STATUS_FAILED: Blanket status for user or system-related job failure.  - JOB_STATUS_REQUESTED: The job descriptor exists but has no resources allocated. Jobs that remain in this status without moving to the PENDING status are at risk of entering the FAILED status.  - JOB_STATUS_CANCELLED: Job has been cancelled. Cancelled jobs cannot be recovered.
        :param list[str] first_page_query_selected_types: Specifies a set of types. The query only returns jobs with types in the specified set. Specify no types to return all results. Job types not tied to projects will not be returned.
        :param bool first_page_query_internal_created: If true, the query only returns jobs created by internal workers. Otherwise, all jobs are returned.
        :param str page_token: The ListJobs query returns a pageToken after the first request.
        :param str page_size: The maximum number of Job objects to return in a single page.
        :param str view: Specifies how much information about each job to retrieve.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view.
        :return: RimeListJobsForProjectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.job_reader_list_jobs_for_project_with_http_info(project_id_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.job_reader_list_jobs_for_project_with_http_info(project_id_uuid, **kwargs)  # noqa: E501
            return data

    def job_reader_list_jobs_for_project_with_http_info(self, project_id_uuid, **kwargs):  # noqa: E501
        """ListJobsForProject  # noqa: E501

        Returns a paginated list of jobs for a given project. The list can be filtered by job type and status.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.job_reader_list_jobs_for_project_with_http_info(project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id_uuid: Unique object ID. (required)
        :param list[str] first_page_query_selected_statuses: Specifies a set of statuses. The query only returns results with a status in the specified set. Specify no statuses to return all results.   - JOB_STATUS_PENDING: Resources have been created for the job but the job has not started yet.  - JOB_STATUS_FAILED: Blanket status for user or system-related job failure.  - JOB_STATUS_REQUESTED: The job descriptor exists but has no resources allocated. Jobs that remain in this status without moving to the PENDING status are at risk of entering the FAILED status.  - JOB_STATUS_CANCELLED: Job has been cancelled. Cancelled jobs cannot be recovered.
        :param list[str] first_page_query_selected_types: Specifies a set of types. The query only returns jobs with types in the specified set. Specify no types to return all results. Job types not tied to projects will not be returned.
        :param bool first_page_query_internal_created: If true, the query only returns jobs created by internal workers. Otherwise, all jobs are returned.
        :param str page_token: The ListJobs query returns a pageToken after the first request.
        :param str page_size: The maximum number of Job objects to return in a single page.
        :param str view: Specifies how much information about each job to retrieve.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view.
        :return: RimeListJobsForProjectResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_id_uuid', 'first_page_query_selected_statuses', 'first_page_query_selected_types', 'first_page_query_internal_created', 'page_token', 'page_size', 'view']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method job_reader_list_jobs_for_project" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_id_uuid' is set
        if ('project_id_uuid' not in params or
                params['project_id_uuid'] is None):
            raise ValueError("Missing the required parameter `project_id_uuid` when calling `job_reader_list_jobs_for_project`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_id_uuid' in params:
            path_params['projectId.uuid'] = params['project_id_uuid']  # noqa: E501

        query_params = []
        if 'first_page_query_selected_statuses' in params:
            query_params.append(('firstPageQuery.selectedStatuses', params['first_page_query_selected_statuses']))  # noqa: E501
            collection_formats['firstPageQuery.selectedStatuses'] = 'multi'  # noqa: E501
        if 'first_page_query_selected_types' in params:
            query_params.append(('firstPageQuery.selectedTypes', params['first_page_query_selected_types']))  # noqa: E501
            collection_formats['firstPageQuery.selectedTypes'] = 'multi'  # noqa: E501
        if 'first_page_query_internal_created' in params:
            query_params.append(('firstPageQuery.internalCreated', params['first_page_query_internal_created']))  # noqa: E501
        if 'page_token' in params:
            query_params.append(('pageToken', params['page_token']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501
        if 'view' in params:
            query_params.append(('view', params['view']))  # noqa: E501

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
            '/v1/jobs/project/{projectId.uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeListJobsForProjectResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
