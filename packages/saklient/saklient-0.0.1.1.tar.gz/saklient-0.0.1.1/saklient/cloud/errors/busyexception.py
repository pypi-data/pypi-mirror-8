# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.busyexception

class BusyException(HttpServiceUnavailableException):
    ## サービスが利用できません。サーバが混雑しています。しばらく時間をおいてから再度お試しください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(BusyException, self).__init__(status, code, "サービスが利用できません。サーバが混雑しています。しばらく時間をおいてから再度お試しください。" if message is None or message == "" else message)
    
