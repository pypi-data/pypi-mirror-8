# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.toomanyrequestexception

class TooManyRequestException(HttpServiceUnavailableException):
    ## 要求を受け付けできません。リクエストの密度が高すぎます。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(TooManyRequestException, self).__init__(status, code, "要求を受け付けできません。リクエストの密度が高すぎます。" if message is None or message == "" else message)
    
