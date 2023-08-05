# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.operationfailureexception

class OperationFailureException(HttpServiceUnavailableException):
    ## サービスが利用できません。操作に失敗しました。サーバが混雑している可能性があります。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(OperationFailureException, self).__init__(status, code, "サービスが利用できません。操作に失敗しました。サーバが混雑している可能性があります。" if message is None or message == "" else message)
    
