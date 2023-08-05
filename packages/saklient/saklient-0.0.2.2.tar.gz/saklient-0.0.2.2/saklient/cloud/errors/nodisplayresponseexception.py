# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.nodisplayresponseexception

class NoDisplayResponseException(HttpServiceUnavailableException):
    ## サービスが利用できません。サーバの画面が応答していません。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(NoDisplayResponseException, self).__init__(status, code, "サービスが利用できません。サーバの画面が応答していません。" if message is None or message == "" else message)
    
