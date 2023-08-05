# -*- coding:utf-8 -*-

from ...errors.httpserviceunavailableexception import HttpServiceUnavailableException

# module saklient.cloud.errors.bootfailureingroupexception

class BootFailureInGroupException(HttpServiceUnavailableException):
    ## サービスが利用できません。サーバ起動グループ指定に問題がある可能性があります。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(BootFailureInGroupException, self).__init__(status, code, "サービスが利用できません。サーバ起動グループ指定に問題がある可能性があります。" if message is None or message == "" else message)
    
