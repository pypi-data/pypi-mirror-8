# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.hostoperationfailureexception

class HostOperationFailureException(HttpServiceUnavailableException):
    ## サービスが利用できません。サーバの操作に失敗しました。このエラーが繰り返し発生する場合は、メンテナンス情報、サポートサイトをご確認ください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(HostOperationFailureException, self).__init__(status, code, "サービスが利用できません。サーバの操作に失敗しました。このエラーが繰り返し発生する場合は、メンテナンス情報、サポートサイトをご確認ください。" if message is None or message == "" else message)
    
