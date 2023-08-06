# -*- coding:utf-8 -*-

from ..client import Client
from .model import Model
from ..resources.resource import Resource
from ..resources.archive import Archive
from ..resources.loadbalancer import LoadBalancer
from ..resources.vpcrouter import VpcRouter
from ..enums.escope import EScope
from ...util import Util

# module saklient.cloud.models.model_archive

class Model_Archive(Model):
    ## アーカイブを検索・作成するための機能を備えたクラス。
    
    ## @private
    # @return {str}
    def _api_path(self):
        return "/archive"
    
    ## @private
    # @return {str}
    def _root_key(self):
        return "Archive"
    
    ## @private
    # @return {str}
    def _root_key_m(self):
        return "Archives"
    
    ## @private
    # @return {str}
    def _class_name(self):
        return "Archive"
    
    ## @private
    # @param {any} obj
    # @param {bool} wrapped=False
    # @return {saklient.cloud.resources.resource.Resource}
    def _create_resource_impl(self, obj, wrapped=False):
        Util.validate_type(wrapped, "bool")
        return Archive(self._client, obj, wrapped)
    
    ## 次に取得するリストの開始オフセットを指定します。
    # 
    # @param {int} offset オフセット
    # @return {saklient.cloud.models.model_archive.Model_Archive} this
    def offset(self, offset):
        Util.validate_type(offset, "int")
        return self._offset(offset)
    
    ## 次に取得するリストの上限レコード数を指定します。
    # 
    # @param {int} count 上限レコード数
    # @return {saklient.cloud.models.model_archive.Model_Archive} this
    def limit(self, count):
        Util.validate_type(count, "int")
        return self._limit(count)
    
    ## Web APIのフィルタリング設定を直接指定します。
    # 
    # @param {str} key キー
    # @param {any} value 値
    # @param {bool} multiple=False valueに配列を与え、OR条件で完全一致検索する場合にtrueを指定します。通常、valueはスカラ値であいまい検索されます。
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def filter_by(self, key, value, multiple=False):
        Util.validate_type(key, "str")
        Util.validate_type(multiple, "bool")
        return self._filter_by(key, value, multiple)
    
    ## 次のリクエストのために設定されているステートをすべて破棄します。
    # 
    # @return {saklient.cloud.models.model_archive.Model_Archive} this
    def reset(self):
        return self._reset()
    
    ## 新規リソース作成用のオブジェクトを用意します。
    # 
    # 返り値のオブジェクトにパラメータを設定し、save() を呼ぶことで実際のリソースが作成されます。
    # 
    # @return {saklient.cloud.resources.archive.Archive} リソースオブジェクト
    def create(self):
        return self._create()
    
    ## 指定したIDを持つ唯一のリソースを取得します。
    # 
    # @param {str} id
    # @return {saklient.cloud.resources.archive.Archive} リソースオブジェクト
    def get_by_id(self, id):
        Util.validate_type(id, "str")
        return self._get_by_id(id)
    
    ## リソースの検索リクエストを実行し、結果をリストで取得します。
    # 
    # @return {saklient.cloud.resources.archive.Archive[]} リソースオブジェクトの配列
    def find(self):
        return self._find()
    
    ## 指定した文字列を名前に含むリソースに絞り込みます。
    # 
    # 大文字・小文字は区別されません。
    # 半角スペースで区切られた複数の文字列は、それらをすべて含むことが条件とみなされます。
    # 
    # @todo Implement test case
    # @param {str} name
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def with_name_like(self, name):
        Util.validate_type(name, "str")
        return self._with_name_like(name)
    
    ## 指定したタグを持つリソースに絞り込みます。
    # 
    # 複数のタグを指定する場合は withTags() を利用してください。
    # 
    # @todo Implement test case
    # @param {str} tag
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def with_tag(self, tag):
        Util.validate_type(tag, "str")
        return self._with_tag(tag)
    
    ## 指定したすべてのタグを持つリソースに絞り込みます。
    # 
    # @todo Implement test case
    # @param {str[]} tags
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def with_tags(self, tags):
        Util.validate_type(tags, "list")
        return self._with_tags(tags)
    
    ## 指定したDNFに合致するタグを持つリソースに絞り込みます。
    # 
    # @todo Implement test case
    # @param {str[][]} dnf
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def with_tag_dnf(self, dnf):
        Util.validate_type(dnf, "list")
        return self._with_tag_dnf(dnf)
    
    ## 名前でソートします。
    # 
    # @todo Implement test case
    # @param {bool} reverse=False
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def sort_by_name(self, reverse=False):
        Util.validate_type(reverse, "bool")
        return self._sort_by_name(reverse)
    
    ## @ignore
    # @param {saklient.cloud.client.Client} client
    def __init__(self, client):
        super(Model_Archive, self).__init__(client)
        Util.validate_type(client, "saklient.cloud.client.Client")
    
    ## 指定したサイズのアーカイブに絞り込みます。
    # 
    # @param {int} sizeGib
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def with_size_gib(self, sizeGib):
        Util.validate_type(sizeGib, "int")
        self._filter_by("SizeMB", [sizeGib * 1024])
        return self
    
    ## パブリックアーカイブに絞り込みます。
    # 
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def with_shared_scope(self):
        self._filter_by("Scope", [EScope.shared])
        return self
    
    ## プライベートアーカイブに絞り込みます。
    # 
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def with_user_scope(self):
        self._filter_by("Scope", [EScope.user])
        return self
    
    ## サイズでソートします。
    # 
    # @param {bool} reverse=False
    # @return {saklient.cloud.models.model_archive.Model_Archive}
    def sort_by_size(self, reverse=False):
        Util.validate_type(reverse, "bool")
        self._sort("SizeMB", reverse)
        return self
    
