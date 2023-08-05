# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.dnsptrupdatefailureexception

class DnsPtrUpdateFailureException(HttpServiceUnavailableException):
    ## サービスが利用できません。PTRレコードを設定できません。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(DnsPtrUpdateFailureException, self).__init__(status, code, "サービスが利用できません。PTRレコードを設定できません。" if message is None or message == "" else message)
    
