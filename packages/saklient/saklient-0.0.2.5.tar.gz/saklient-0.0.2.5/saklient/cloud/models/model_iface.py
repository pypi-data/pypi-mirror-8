# -*- coding:utf-8 -*-

from ..client import Client
from .model import Model
from ..resources.resource import Resource
from ..resources.iface import Iface
from ...util import Util

# module saklient.cloud.models.model_iface

class Model_Iface(Model):
    ## インタフェースを検索・作成するための機能を備えたクラス。
    
    ## @private
    # @return {str}
    def _api_path(self):
        return "/interface"
    
    ## @private
    # @return {str}
    def _root_key(self):
        return "Interface"
    
    ## @private
    # @return {str}
    def _root_key_m(self):
        return "Interfaces"
    
    ## @private
    # @return {str}
    def _class_name(self):
        return "Iface"
    
    ## @private
    # @param {any} obj
    # @param {bool} wrapped=False
    # @return {saklient.cloud.resources.resource.Resource}
    def _create_resource_impl(self, obj, wrapped=False):
        Util.validate_type(wrapped, "bool")
        return Iface(self._client, obj, wrapped)
    
    ## 次に取得するリストの開始オフセットを指定します。
    # 
    # @param {int} offset オフセット
    # @return {saklient.cloud.models.model_iface.Model_Iface} this
    def offset(self, offset):
        Util.validate_type(offset, "int")
        return self._offset(offset)
    
    ## 次に取得するリストの上限レコード数を指定します。
    # 
    # @param {int} count 上限レコード数
    # @return {saklient.cloud.models.model_iface.Model_Iface} this
    def limit(self, count):
        Util.validate_type(count, "int")
        return self._limit(count)
    
    ## Web APIのフィルタリング設定を直接指定します。
    # 
    # @param {str} key キー
    # @param {any} value 値
    # @param {bool} multiple=False valueに配列を与え、OR条件で完全一致検索する場合にtrueを指定します。通常、valueはスカラ値であいまい検索されます。
    # @return {saklient.cloud.models.model_iface.Model_Iface}
    def filter_by(self, key, value, multiple=False):
        Util.validate_type(key, "str")
        Util.validate_type(multiple, "bool")
        return self._filter_by(key, value, multiple)
    
    ## 次のリクエストのために設定されているステートをすべて破棄します。
    # 
    # @return {saklient.cloud.models.model_iface.Model_Iface} this
    def reset(self):
        return self._reset()
    
    ## 新規リソース作成用のオブジェクトを用意します。
    # 
    # 返り値のオブジェクトにパラメータを設定し、save() を呼ぶことで実際のリソースが作成されます。
    # 
    # @return {saklient.cloud.resources.iface.Iface} リソースオブジェクト
    def create(self):
        return self._create()
    
    ## 指定したIDを持つ唯一のリソースを取得します。
    # 
    # @param {str} id
    # @return {saklient.cloud.resources.iface.Iface} リソースオブジェクト
    def get_by_id(self, id):
        Util.validate_type(id, "str")
        return self._get_by_id(id)
    
    ## リソースの検索リクエストを実行し、結果をリストで取得します。
    # 
    # @return {saklient.cloud.resources.iface.Iface[]} リソースオブジェクトの配列
    def find(self):
        return self._find()
    
    ## @ignore
    # @param {saklient.cloud.client.Client} client
    def __init__(self, client):
        super(Model_Iface, self).__init__(client)
        Util.validate_type(client, "saklient.cloud.client.Client")
    
