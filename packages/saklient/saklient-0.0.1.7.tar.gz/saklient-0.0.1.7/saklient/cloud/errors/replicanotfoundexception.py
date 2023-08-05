# -*- coding:utf-8 -*-

from ...errors.httpnotfoundexception import HttpNotFoundException

# module saklient.cloud.errors.replicanotfoundexception

class ReplicaNotFoundException(HttpNotFoundException):
    ## 対象が見つかりません。このストレージには指定リソースの複製が存在しません。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(ReplicaNotFoundException, self).__init__(status, code, "対象が見つかりません。このストレージには指定リソースの複製が存在しません。" if message is None or message == "" else message)
    
