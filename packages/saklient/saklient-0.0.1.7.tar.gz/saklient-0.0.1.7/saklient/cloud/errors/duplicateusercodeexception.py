# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.duplicateusercodeexception

class DuplicateUserCodeException(HttpConflictException):
    ## 要求された操作を行えません。同一ユーザ名で複数のユーザを作成することはできません。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(DuplicateUserCodeException, self).__init__(status, code, "要求された操作を行えません。同一ユーザ名で複数のユーザを作成することはできません。" if message is None or message == "" else message)
    
