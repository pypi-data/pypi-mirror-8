# -*- coding:utf-8 -*-

from ...errors.httpbadrequestexception import HttpBadRequestException

# module saklient.cloud.errors.filterunknownoperatorexception

class FilterUnknownOperatorException(HttpBadRequestException):
    ## 不適切な要求です。不明な演算子がフィルタ中に含まれています。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(FilterUnknownOperatorException, self).__init__(status, code, "不適切な要求です。不明な演算子がフィルタ中に含まれています。" if message is None or message == "" else message)
    
