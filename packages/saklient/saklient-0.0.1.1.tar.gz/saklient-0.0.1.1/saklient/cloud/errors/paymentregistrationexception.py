# -*- coding:utf-8 -*-

from ...errors.httppaymentrequiredexception import HttpPaymentRequiredException

# module saklient.cloud.errors.paymentregistrationexception

class PaymentRegistrationException(HttpPaymentRequiredException):
    ## 要求を受け付けできません。支払情報が未登録です。会員メニューから支払、クレジットカードの情報を登録してください
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(PaymentRegistrationException, self).__init__(status, code, "要求を受け付けできません。支払情報が未登録です。会員メニューから支払、クレジットカードの情報を登録してください" if message is None or message == "" else message)
    
