# -*- coding:utf-8 -*-

from ...errors.httpbadrequestexception import HttpBadRequestException

# module saklient.cloud.errors.sizemismatchexception

class SizeMismatchException(HttpBadRequestException):
    ## 不適切な要求です。参照するリソースのサイズが合致しません。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(SizeMismatchException, self).__init__(status, code, "不適切な要求です。参照するリソースのサイズが合致しません。" if message is None or message == "" else message)
    
