# -*- coding:utf-8 -*-

from ...errors.httpconflictexception import HttpConflictException

# module saklient.cloud.errors.originalhashmismatchexception

class OriginalHashMismatchException(HttpConflictException):
    ## 要求された操作を行えません。オリジナルのデータを取得してからこのリクエストを行うまでの間に、他の変更が加わった可能性があります。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(OriginalHashMismatchException, self).__init__(status, code, "要求された操作を行えません。オリジナルのデータを取得してからこのリクエストを行うまでの間に、他の変更が加わった可能性があります。" if message is None or message == "" else message)
    
