# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.storageoperationfailureexception

class StorageOperationFailureException(HttpServiceUnavailableException):
    ## サービスが利用できません。ストレージの操作に失敗しました。サーバが混雑している可能性があります。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(StorageOperationFailureException, self).__init__(status, code, "サービスが利用できません。ストレージの操作に失敗しました。サーバが混雑している可能性があります。" if message is None or message == "" else message)
    
