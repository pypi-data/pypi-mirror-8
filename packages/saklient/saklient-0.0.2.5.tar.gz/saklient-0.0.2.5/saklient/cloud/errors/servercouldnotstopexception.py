# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.servercouldnotstopexception

class ServerCouldNotStopException(HttpServiceUnavailableException):
    ## サービスが利用できません。サーバを停止できません。再度お試しください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(ServerCouldNotStopException, self).__init__(status, code, "サービスが利用できません。サーバを停止できません。再度お試しください。" if message is None or message == "" else message)
    
