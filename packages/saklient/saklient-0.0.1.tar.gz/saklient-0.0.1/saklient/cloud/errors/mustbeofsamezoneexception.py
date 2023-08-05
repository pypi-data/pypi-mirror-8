# -*- coding:utf-8 -*-

from ...errors.httpbadrequestexception import HttpBadRequestException

# module saklient.cloud.errors.mustbeofsamezoneexception

class MustBeOfSameZoneException(HttpBadRequestException):
    ## 不適切な要求です。参照するリソースは同一ゾーンに存在しなければなりません。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(MustBeOfSameZoneException, self).__init__(status, code, "不適切な要求です。参照するリソースは同一ゾーンに存在しなければなりません。" if message is None or message == "" else message)
    
