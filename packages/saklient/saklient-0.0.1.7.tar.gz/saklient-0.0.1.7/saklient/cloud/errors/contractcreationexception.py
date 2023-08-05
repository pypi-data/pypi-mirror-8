# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.contractcreationexception

class ContractCreationException(HttpServiceUnavailableException):
    ## 要求を受け付けできません。契約コードを発行することができません。メンテナンス情報、サポートサイトをご確認ください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(ContractCreationException, self).__init__(status, code, "要求を受け付けできません。契約コードを発行することができません。メンテナンス情報、サポートサイトをご確認ください。" if message is None or message == "" else message)
    
