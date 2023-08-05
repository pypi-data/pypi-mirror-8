# -*- coding:utf-8 -*-

from ...errors.httpinternalservererrorexception import HttpInternalServerErrorException

# module saklient.cloud.errors.unknownexception

class UnknownException(HttpInternalServerErrorException):
    ## 予期しないエラーが発生しました。このエラーが繰り返し発生する場合は、サポートサイトやメンテナンス情報をご確認ください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(UnknownException, self).__init__(status, code, "予期しないエラーが発生しました。このエラーが繰り返し発生する場合は、サポートサイトやメンテナンス情報をご確認ください。" if message is None or message == "" else message)
    
