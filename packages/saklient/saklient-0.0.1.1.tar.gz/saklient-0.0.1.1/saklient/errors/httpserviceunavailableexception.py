# -*- coding:utf-8 -*-

from .httpexception import HttpException

# module saklient.errors.httpserviceunavailableexception

class HttpServiceUnavailableException(HttpException):
    ## サービスが利用できません。対象は利用できない、またはサーバが混雑しています。このエラーが繰り返し発生する場合は、メンテナンス情報、サポートサイトをご確認ください。
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(HttpServiceUnavailableException, self).__init__(status, code, "サービスが利用できません。対象は利用できない、またはサーバが混雑しています。このエラーが繰り返し発生する場合は、メンテナンス情報、サポートサイトをご確認ください。" if message is None or message == "" else message)
    
