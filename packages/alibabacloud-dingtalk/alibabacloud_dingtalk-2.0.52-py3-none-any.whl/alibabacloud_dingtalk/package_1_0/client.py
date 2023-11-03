# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.core import TeaCore

from alibabacloud_gateway_spi.client import Client as SPIClient
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_gateway_dingtalk.client import Client as GatewayClientClient
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dingtalk.package_1_0 import models as dingtalkpackage__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    _client: SPIClient = None

    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._client = GatewayClientClient()
        self._spi = self._client
        self._endpoint_rule = ''
        if UtilClient.empty(self._endpoint):
            self._endpoint = 'api.dingtalk.com'

    def close_hpackage_with_options(
        self,
        request: dingtalkpackage__1__0_models.CloseHPackageRequest,
        headers: dingtalkpackage__1__0_models.CloseHPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.CloseHPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CloseHPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/microApps/close',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.CloseHPackageResponse(),
            self.execute(params, req, runtime)
        )

    async def close_hpackage_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.CloseHPackageRequest,
        headers: dingtalkpackage__1__0_models.CloseHPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.CloseHPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CloseHPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/microApps/close',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.CloseHPackageResponse(),
            await self.execute_async(params, req, runtime)
        )

    def close_hpackage(
        self,
        request: dingtalkpackage__1__0_models.CloseHPackageRequest,
    ) -> dingtalkpackage__1__0_models.CloseHPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.CloseHPackageHeaders()
        return self.close_hpackage_with_options(request, headers, runtime)

    async def close_hpackage_async(
        self,
        request: dingtalkpackage__1__0_models.CloseHPackageRequest,
    ) -> dingtalkpackage__1__0_models.CloseHPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.CloseHPackageHeaders()
        return await self.close_hpackage_with_options_async(request, headers, runtime)

    def get_upload_token_with_options(
        self,
        request: dingtalkpackage__1__0_models.GetUploadTokenRequest,
        headers: dingtalkpackage__1__0_models.GetUploadTokenHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.GetUploadTokenResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUploadToken',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/uploadTokens',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.GetUploadTokenResponse(),
            self.execute(params, req, runtime)
        )

    async def get_upload_token_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.GetUploadTokenRequest,
        headers: dingtalkpackage__1__0_models.GetUploadTokenHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.GetUploadTokenResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GetUploadToken',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/uploadTokens',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.GetUploadTokenResponse(),
            await self.execute_async(params, req, runtime)
        )

    def get_upload_token(
        self,
        request: dingtalkpackage__1__0_models.GetUploadTokenRequest,
    ) -> dingtalkpackage__1__0_models.GetUploadTokenResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.GetUploadTokenHeaders()
        return self.get_upload_token_with_options(request, headers, runtime)

    async def get_upload_token_async(
        self,
        request: dingtalkpackage__1__0_models.GetUploadTokenRequest,
    ) -> dingtalkpackage__1__0_models.GetUploadTokenResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.GetUploadTokenHeaders()
        return await self.get_upload_token_with_options_async(request, headers, runtime)

    def h_package_list_get_with_options(
        self,
        request: dingtalkpackage__1__0_models.HPackageListGetRequest,
        headers: dingtalkpackage__1__0_models.HPackageListGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HPackageListGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HPackageListGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HPackageListGetResponse(),
            self.execute(params, req, runtime)
        )

    async def h_package_list_get_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.HPackageListGetRequest,
        headers: dingtalkpackage__1__0_models.HPackageListGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HPackageListGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.page_number):
            query['pageNumber'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['pageSize'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HPackageListGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/versions',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HPackageListGetResponse(),
            await self.execute_async(params, req, runtime)
        )

    def h_package_list_get(
        self,
        request: dingtalkpackage__1__0_models.HPackageListGetRequest,
    ) -> dingtalkpackage__1__0_models.HPackageListGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HPackageListGetHeaders()
        return self.h_package_list_get_with_options(request, headers, runtime)

    async def h_package_list_get_async(
        self,
        request: dingtalkpackage__1__0_models.HPackageListGetRequest,
    ) -> dingtalkpackage__1__0_models.HPackageListGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HPackageListGetHeaders()
        return await self.h_package_list_get_with_options_async(request, headers, runtime)

    def h_publish_package_with_options(
        self,
        request: dingtalkpackage__1__0_models.HPublishPackageRequest,
        headers: dingtalkpackage__1__0_models.HPublishPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HPublishPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HPublishPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/publish',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HPublishPackageResponse(),
            self.execute(params, req, runtime)
        )

    async def h_publish_package_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.HPublishPackageRequest,
        headers: dingtalkpackage__1__0_models.HPublishPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HPublishPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HPublishPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/publish',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HPublishPackageResponse(),
            await self.execute_async(params, req, runtime)
        )

    def h_publish_package(
        self,
        request: dingtalkpackage__1__0_models.HPublishPackageRequest,
    ) -> dingtalkpackage__1__0_models.HPublishPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HPublishPackageHeaders()
        return self.h_publish_package_with_options(request, headers, runtime)

    async def h_publish_package_async(
        self,
        request: dingtalkpackage__1__0_models.HPublishPackageRequest,
    ) -> dingtalkpackage__1__0_models.HPublishPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HPublishPackageHeaders()
        return await self.h_publish_package_with_options_async(request, headers, runtime)

    def h_upload_package_with_options(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageRequest,
        headers: dingtalkpackage__1__0_models.HUploadPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HUploadPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.oss_object_key):
            body['ossObjectKey'] = request.oss_object_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HUploadPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/asyncUpload',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HUploadPackageResponse(),
            self.execute(params, req, runtime)
        )

    async def h_upload_package_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageRequest,
        headers: dingtalkpackage__1__0_models.HUploadPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HUploadPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.oss_object_key):
            body['ossObjectKey'] = request.oss_object_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HUploadPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/asyncUpload',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HUploadPackageResponse(),
            await self.execute_async(params, req, runtime)
        )

    def h_upload_package(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageRequest,
    ) -> dingtalkpackage__1__0_models.HUploadPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HUploadPackageHeaders()
        return self.h_upload_package_with_options(request, headers, runtime)

    async def h_upload_package_async(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageRequest,
    ) -> dingtalkpackage__1__0_models.HUploadPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HUploadPackageHeaders()
        return await self.h_upload_package_with_options_async(request, headers, runtime)

    def h_upload_package_status_with_options(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageStatusRequest,
        headers: dingtalkpackage__1__0_models.HUploadPackageStatusHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HUploadPackageStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.task_id):
            query['taskId'] = request.task_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HUploadPackageStatus',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/uploadStatus',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HUploadPackageStatusResponse(),
            self.execute(params, req, runtime)
        )

    async def h_upload_package_status_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageStatusRequest,
        headers: dingtalkpackage__1__0_models.HUploadPackageStatusHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.HUploadPackageStatusResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.task_id):
            query['taskId'] = request.task_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HUploadPackageStatus',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/uploadStatus',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.HUploadPackageStatusResponse(),
            await self.execute_async(params, req, runtime)
        )

    def h_upload_package_status(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageStatusRequest,
    ) -> dingtalkpackage__1__0_models.HUploadPackageStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HUploadPackageStatusHeaders()
        return self.h_upload_package_status_with_options(request, headers, runtime)

    async def h_upload_package_status_async(
        self,
        request: dingtalkpackage__1__0_models.HUploadPackageStatusRequest,
    ) -> dingtalkpackage__1__0_models.HUploadPackageStatusResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.HUploadPackageStatusHeaders()
        return await self.h_upload_package_status_with_options_async(request, headers, runtime)

    def open_micro_app_package_with_options(
        self,
        request: dingtalkpackage__1__0_models.OpenMicroAppPackageRequest,
        headers: dingtalkpackage__1__0_models.OpenMicroAppPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.OpenMicroAppPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.agent_id):
            body['agentId'] = request.agent_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='OpenMicroAppPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/microApps/open',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.OpenMicroAppPackageResponse(),
            self.execute(params, req, runtime)
        )

    async def open_micro_app_package_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.OpenMicroAppPackageRequest,
        headers: dingtalkpackage__1__0_models.OpenMicroAppPackageHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.OpenMicroAppPackageResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.agent_id):
            body['agentId'] = request.agent_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='OpenMicroAppPackage',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/h5/microApps/open',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.OpenMicroAppPackageResponse(),
            await self.execute_async(params, req, runtime)
        )

    def open_micro_app_package(
        self,
        request: dingtalkpackage__1__0_models.OpenMicroAppPackageRequest,
    ) -> dingtalkpackage__1__0_models.OpenMicroAppPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.OpenMicroAppPackageHeaders()
        return self.open_micro_app_package_with_options(request, headers, runtime)

    async def open_micro_app_package_async(
        self,
        request: dingtalkpackage__1__0_models.OpenMicroAppPackageRequest,
    ) -> dingtalkpackage__1__0_models.OpenMicroAppPackageResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.OpenMicroAppPackageHeaders()
        return await self.open_micro_app_package_with_options_async(request, headers, runtime)

    def release_gray_deploy_with_options(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayDeployRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayDeployHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayDeployResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayDeploy',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/deploy',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayDeployResponse(),
            self.execute(params, req, runtime)
        )

    async def release_gray_deploy_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayDeployRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayDeployHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayDeployResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayDeploy',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/deploy',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayDeployResponse(),
            await self.execute_async(params, req, runtime)
        )

    def release_gray_deploy(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayDeployRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayDeployResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayDeployHeaders()
        return self.release_gray_deploy_with_options(request, headers, runtime)

    async def release_gray_deploy_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayDeployRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayDeployResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayDeployHeaders()
        return await self.release_gray_deploy_with_options_async(request, headers, runtime)

    def release_gray_exit_with_options(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayExitRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayExitHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayExitResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayExit',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/exit',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayExitResponse(),
            self.execute(params, req, runtime)
        )

    async def release_gray_exit_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayExitRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayExitHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayExitResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayExit',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/exit',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayExitResponse(),
            await self.execute_async(params, req, runtime)
        )

    def release_gray_exit(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayExitRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayExitResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayExitHeaders()
        return self.release_gray_exit_with_options(request, headers, runtime)

    async def release_gray_exit_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayExitRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayExitResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayExitHeaders()
        return await self.release_gray_exit_with_options_async(request, headers, runtime)

    def release_gray_org_get_with_options(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgGetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayOrgGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseGrayOrgGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/organizations',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayOrgGetResponse(),
            self.execute(params, req, runtime)
        )

    async def release_gray_org_get_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgGetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayOrgGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseGrayOrgGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/organizations',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayOrgGetResponse(),
            await self.execute_async(params, req, runtime)
        )

    def release_gray_org_get(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgGetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayOrgGetHeaders()
        return self.release_gray_org_get_with_options(request, headers, runtime)

    async def release_gray_org_get_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgGetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayOrgGetHeaders()
        return await self.release_gray_org_get_with_options_async(request, headers, runtime)

    def release_gray_org_set_with_options(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgSetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayOrgSetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgSetResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.value):
            body['value'] = request.value
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayOrgSet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/organizations/release',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayOrgSetResponse(),
            self.execute(params, req, runtime)
        )

    async def release_gray_org_set_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgSetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayOrgSetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgSetResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.value):
            body['value'] = request.value
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayOrgSet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/organizations/release',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayOrgSetResponse(),
            await self.execute_async(params, req, runtime)
        )

    def release_gray_org_set(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgSetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgSetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayOrgSetHeaders()
        return self.release_gray_org_set_with_options(request, headers, runtime)

    async def release_gray_org_set_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayOrgSetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayOrgSetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayOrgSetHeaders()
        return await self.release_gray_org_set_with_options_async(request, headers, runtime)

    def release_gray_percent_get_with_options(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentGetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayPercentGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseGrayPercentGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/users/percents',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayPercentGetResponse(),
            self.execute(params, req, runtime)
        )

    async def release_gray_percent_get_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentGetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayPercentGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseGrayPercentGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/users/percents',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayPercentGetResponse(),
            await self.execute_async(params, req, runtime)
        )

    def release_gray_percent_get(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentGetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayPercentGetHeaders()
        return self.release_gray_percent_get_with_options(request, headers, runtime)

    async def release_gray_percent_get_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentGetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayPercentGetHeaders()
        return await self.release_gray_percent_get_with_options_async(request, headers, runtime)

    def release_gray_percent_set_with_options(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentSetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayPercentSetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentSetResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.value):
            body['value'] = request.value
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayPercentSet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/users/percents/release',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayPercentSetResponse(),
            self.execute(params, req, runtime)
        )

    async def release_gray_percent_set_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentSetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayPercentSetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentSetResponse:
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mini_app_id):
            body['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.value):
            body['value'] = request.value
        if not UtilClient.is_unset(request.version):
            body['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ReleaseGrayPercentSet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/users/percents/release',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayPercentSetResponse(),
            await self.execute_async(params, req, runtime)
        )

    def release_gray_percent_set(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentSetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentSetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayPercentSetHeaders()
        return self.release_gray_percent_set_with_options(request, headers, runtime)

    async def release_gray_percent_set_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayPercentSetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayPercentSetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayPercentSetHeaders()
        return await self.release_gray_percent_set_with_options_async(request, headers, runtime)

    def release_gray_user_id_get_with_options(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayUserIdGetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayUserIdGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayUserIdGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseGrayUserIdGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/users',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayUserIdGetResponse(),
            self.execute(params, req, runtime)
        )

    async def release_gray_user_id_get_with_options_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayUserIdGetRequest,
        headers: dingtalkpackage__1__0_models.ReleaseGrayUserIdGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayUserIdGetResponse:
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.mini_app_id):
            query['miniAppId'] = request.mini_app_id
        if not UtilClient.is_unset(request.version):
            query['version'] = request.version
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_dingtalk_access_token):
            real_headers['x-acs-dingtalk-access-token'] = UtilClient.to_jsonstring(headers.x_acs_dingtalk_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ReleaseGrayUserIdGet',
            version='package_1.0',
            protocol='HTTP',
            pathname=f'/v1.0/package/greys/users',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='none',
            body_type='json'
        )
        return TeaCore.from_map(
            dingtalkpackage__1__0_models.ReleaseGrayUserIdGetResponse(),
            await self.execute_async(params, req, runtime)
        )

    def release_gray_user_id_get(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayUserIdGetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayUserIdGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayUserIdGetHeaders()
        return self.release_gray_user_id_get_with_options(request, headers, runtime)

    async def release_gray_user_id_get_async(
        self,
        request: dingtalkpackage__1__0_models.ReleaseGrayUserIdGetRequest,
    ) -> dingtalkpackage__1__0_models.ReleaseGrayUserIdGetResponse:
        runtime = util_models.RuntimeOptions()
        headers = dingtalkpackage__1__0_models.ReleaseGrayUserIdGetHeaders()
        return await self.release_gray_user_id_get_with_options_async(request, headers, runtime)
