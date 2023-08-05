# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.servicetemporarilyunavailableexception

class ServiceTemporarilyUnavailableException(HttpServiceUnavailableException):
    ## サービスが利用できません。この機能は一時的に利用できない状態にあります。メンテナンス情報、サポートサイトをご確認ください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(ServiceTemporarilyUnavailableException, self).__init__(status, code, "サービスが利用できません。この機能は一時的に利用できない状態にあります。メンテナンス情報、サポートサイトをご確認ください。" if message is None or message == "" else message)
    
