# -*- coding:utf-8 -*-

from .httpexception import HttpException

# module saklient.errors.httpunauthorizedexception

class HttpUnauthorizedException(HttpException):
    ## この操作は認証が必要です。IDまたはパスワードが誤っている可能性があります。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(HttpUnauthorizedException, self).__init__(status, code, "この操作は認証が必要です。IDまたはパスワードが誤っている可能性があります。" if message is None or message == "" else message)
    
