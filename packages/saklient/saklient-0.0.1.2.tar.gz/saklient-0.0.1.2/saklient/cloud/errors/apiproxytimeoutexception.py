# -*- coding:utf-8 -*-

from ...errors.httpgatewaytimeoutexception import HttpGatewayTimeoutException

# module saklient.cloud.errors.apiproxytimeoutexception

class ApiProxyTimeoutException(HttpGatewayTimeoutException):
    ## APIプロクシがタイムアウトしました。サーバが混雑している可能性があります。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(ApiProxyTimeoutException, self).__init__(status, code, "APIプロクシがタイムアウトしました。サーバが混雑している可能性があります。" if message is None or message == "" else message)
    
