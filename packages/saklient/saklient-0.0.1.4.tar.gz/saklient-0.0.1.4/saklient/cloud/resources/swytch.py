# -*- coding:utf-8 -*-

from ...errors.saklientexception import SaklientException
from ..client import Client
from .resource import Resource
from .icon import Icon
from .router import Router
from .ipv4net import Ipv4Net
from .ipv6net import Ipv6Net
from ...util import Util

# module saklient.cloud.resources.swytch

class Swytch(Resource):
    ## スイッチの実体1つに対応し、属性の取得や操作を行うためのクラス。
    
    # (instance field) m_id
    
    # (instance field) m_name
    
    # (instance field) m_description
    
    # (instance field) m_user_default_route
    
    # (instance field) m_user_mask_len
    
    # (instance field) m_router
    
    # (instance field) m_ipv4_nets
    
    # (instance field) m_ipv6_nets
    
    ## @private
    # @return {str}
    def _api_path(self):
        return "/switch"
    
    ## @private
    # @return {str}
    def _root_key(self):
        return "Switch"
    
    ## @private
    # @return {str}
    def _root_key_m(self):
        return "Switches"
    
    ## @private
    # @return {str}
    def _class_name(self):
        return "Swytch"
    
    ## @private
    # @return {str}
    def _id(self):
        return self.get_id()
    
    ## このローカルオブジェクトに現在設定されているリソース情報をAPIに送信し、新規作成または上書き保存します。
    # 
    # @return {saklient.cloud.resources.swytch.Swytch} this
    def save(self):
        return self._save()
    
    ## 最新のリソース情報を再取得します。
    # 
    # @return {saklient.cloud.resources.swytch.Swytch} this
    def reload(self):
        return self._reload()
    
    ## @ignore
    # @param {saklient.cloud.client.Client} client
    # @param {any} obj
    # @param {bool} wrapped=False
    def __init__(self, client, obj, wrapped=False):
        super(Swytch, self).__init__(client)
        Util.validate_type(client, "saklient.cloud.client.Client")
        Util.validate_type(wrapped, "bool")
        self.api_deserialize(obj, wrapped)
    
    ## このルータ＋スイッチでIPv6アドレスを有効にします。
    # 
    # @return {saklient.cloud.resources.ipv6net.Ipv6Net} 有効化されたIPv6ネットワーク
    def add_ipv6_net(self):
        ret = self.get_router().add_ipv6_net()
        self.reload()
        return ret
    
    ## このルータ＋スイッチでIPv6アドレスを無効にします。
    # 
    # @return {saklient.cloud.resources.swytch.Swytch} this
    def remove_ipv6_net(self):
        nets = self.get_ipv6_nets()
        self.get_router().remove_ipv6_net(nets[0])
        self.reload()
        return self
    
    ## このルータ＋スイッチにスタティックルートを追加します。
    # 
    # @param {int} maskLen
    # @param {str} nextHop
    # @return {saklient.cloud.resources.ipv4net.Ipv4Net} 追加されたIPv4ネットワーク
    def add_static_route(self, maskLen, nextHop):
        Util.validate_type(maskLen, "int")
        Util.validate_type(nextHop, "str")
        ret = self.get_router().add_static_route(maskLen, nextHop)
        self.reload()
        return ret
    
    ## このルータ＋スイッチからスタティックルートを削除します。
    # 
    # @param {saklient.cloud.resources.ipv4net.Ipv4Net} ipv4Net
    # @return {saklient.cloud.resources.swytch.Swytch} this
    def remove_static_route(self, ipv4Net):
        Util.validate_type(ipv4Net, "saklient.cloud.resources.ipv4net.Ipv4Net")
        self.get_router().remove_static_route(ipv4Net)
        self.reload()
        return self
    
    ## このルータ＋スイッチの帯域プランを変更します。
    # 
    # @param {int} bandWidthMbps
    # @return {saklient.cloud.resources.swytch.Swytch} this
    def change_plan(self, bandWidthMbps):
        Util.validate_type(bandWidthMbps, "int")
        self.get_router().change_plan(bandWidthMbps)
        self.reload()
        return self
    
    # (instance field) n_id = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {str}
    def get_id(self):
        return self.m_id
    
    ## ID
    id = property(get_id, None, None)
    
    # (instance field) n_name = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {str}
    def get_name(self):
        return self.m_name
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @param {str} v
    # @return {str}
    def set_name(self, v):
        Util.validate_type(v, "str")
        self.m_name = v
        self.n_name = True
        return self.m_name
    
    ## 名前
    name = property(get_name, set_name, None)
    
    # (instance field) n_description = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {str}
    def get_description(self):
        return self.m_description
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @param {str} v
    # @return {str}
    def set_description(self, v):
        Util.validate_type(v, "str")
        self.m_description = v
        self.n_description = True
        return self.m_description
    
    ## 説明
    description = property(get_description, set_description, None)
    
    # (instance field) n_user_default_route = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {str}
    def get_user_default_route(self):
        return self.m_user_default_route
    
    ## ユーザ設定IPv4ネットワークのゲートウェイ
    user_default_route = property(get_user_default_route, None, None)
    
    # (instance field) n_user_mask_len = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {int}
    def get_user_mask_len(self):
        return self.m_user_mask_len
    
    ## ユーザ設定IPv4ネットワークのマスク長
    user_mask_len = property(get_user_mask_len, None, None)
    
    # (instance field) n_router = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {saklient.cloud.resources.router.Router}
    def get_router(self):
        return self.m_router
    
    ## 接続されているルータ
    router = property(get_router, None, None)
    
    # (instance field) n_ipv4_nets = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {saklient.cloud.resources.ipv4net.Ipv4Net[]}
    def get_ipv4_nets(self):
        return self.m_ipv4_nets
    
    ## IPv4ネットワーク（ルータによる自動割当）
    ipv4_nets = property(get_ipv4_nets, None, None)
    
    # (instance field) n_ipv6_nets = False
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @return {saklient.cloud.resources.ipv6net.Ipv6Net[]}
    def get_ipv6_nets(self):
        return self.m_ipv6_nets
    
    ## IPv6ネットワーク（ルータによる自動割当）
    ipv6_nets = property(get_ipv6_nets, None, None)
    
    ## (This method is generated in Translator_default#buildImpl)
    # 
    # @param {any} r
    def api_deserialize_impl(self, r):
        self.is_new = r is None
        if self.is_new:
            r = {
                
            }
        self.is_incomplete = False
        if Util.exists_path(r, "ID"):
            self.m_id = None if Util.get_by_path(r, "ID") is None else str(Util.get_by_path(r, "ID"))
        else:
            self.m_id = None
            self.is_incomplete = True
        self.n_id = False
        if Util.exists_path(r, "Name"):
            self.m_name = None if Util.get_by_path(r, "Name") is None else str(Util.get_by_path(r, "Name"))
        else:
            self.m_name = None
            self.is_incomplete = True
        self.n_name = False
        if Util.exists_path(r, "Description"):
            self.m_description = None if Util.get_by_path(r, "Description") is None else str(Util.get_by_path(r, "Description"))
        else:
            self.m_description = None
            self.is_incomplete = True
        self.n_description = False
        if Util.exists_path(r, "UserSubnet.DefaultRoute"):
            self.m_user_default_route = None if Util.get_by_path(r, "UserSubnet.DefaultRoute") is None else str(Util.get_by_path(r, "UserSubnet.DefaultRoute"))
        else:
            self.m_user_default_route = None
            self.is_incomplete = True
        self.n_user_default_route = False
        if Util.exists_path(r, "UserSubnet.NetworkMaskLen"):
            self.m_user_mask_len = None if Util.get_by_path(r, "UserSubnet.NetworkMaskLen") is None else int(str(Util.get_by_path(r, "UserSubnet.NetworkMaskLen")))
        else:
            self.m_user_mask_len = None
            self.is_incomplete = True
        self.n_user_mask_len = False
        if Util.exists_path(r, "Internet"):
            self.m_router = None if Util.get_by_path(r, "Internet") is None else Router(self._client, Util.get_by_path(r, "Internet"))
        else:
            self.m_router = None
            self.is_incomplete = True
        self.n_router = False
        if Util.exists_path(r, "Subnets"):
            if Util.get_by_path(r, "Subnets") is None:
                self.m_ipv4_nets = []
            else:
                self.m_ipv4_nets = []
                for t in Util.get_by_path(r, "Subnets"):
                    v1 = None
                    v1 = None if t is None else Ipv4Net(self._client, t)
                    self.m_ipv4_nets.append(v1)
        else:
            self.m_ipv4_nets = None
            self.is_incomplete = True
        self.n_ipv4_nets = False
        if Util.exists_path(r, "IPv6Nets"):
            if Util.get_by_path(r, "IPv6Nets") is None:
                self.m_ipv6_nets = []
            else:
                self.m_ipv6_nets = []
                for t in Util.get_by_path(r, "IPv6Nets"):
                    v2 = None
                    v2 = None if t is None else Ipv6Net(self._client, t)
                    self.m_ipv6_nets.append(v2)
        else:
            self.m_ipv6_nets = None
            self.is_incomplete = True
        self.n_ipv6_nets = False
    
    ## @ignore
    # @param {bool} withClean=False
    # @return {any}
    def api_serialize_impl(self, withClean=False):
        Util.validate_type(withClean, "bool")
        missing = []
        ret = {
            
        }
        if withClean or self.n_id:
            Util.set_by_path(ret, "ID", self.m_id)
        if withClean or self.n_name:
            Util.set_by_path(ret, "Name", self.m_name)
        else:
            if self.is_new:
                missing.append("name")
        if withClean or self.n_description:
            Util.set_by_path(ret, "Description", self.m_description)
        if withClean or self.n_user_default_route:
            Util.set_by_path(ret, "UserSubnet.DefaultRoute", self.m_user_default_route)
        if withClean or self.n_user_mask_len:
            Util.set_by_path(ret, "UserSubnet.NetworkMaskLen", self.m_user_mask_len)
        if withClean or self.n_router:
            Util.set_by_path(ret, "Internet", (None if self.m_router is None else self.m_router.api_serialize(withClean)) if withClean else ({
                'ID': "0"
            } if self.m_router is None else self.m_router.api_serialize_id()))
        if withClean or self.n_ipv4_nets:
            Util.set_by_path(ret, "Subnets", [])
            for r1 in self.m_ipv4_nets:
                v = None
                v = (None if r1 is None else r1.api_serialize(withClean)) if withClean else ({
                    'ID': "0"
                } if r1 is None else r1.api_serialize_id())
                ( (ret["Subnets"] if "Subnets" in ret else None ) if isinstance(ret, dict) else getattr(ret, "Subnets")).append(v)
        if withClean or self.n_ipv6_nets:
            Util.set_by_path(ret, "IPv6Nets", [])
            for r2 in self.m_ipv6_nets:
                v = None
                v = (None if r2 is None else r2.api_serialize(withClean)) if withClean else ({
                    'ID': "0"
                } if r2 is None else r2.api_serialize_id())
                ( (ret["IPv6Nets"] if "IPv6Nets" in ret else None ) if isinstance(ret, dict) else getattr(ret, "IPv6Nets")).append(v)
        if len(missing) > 0:
            raise SaklientException("required_field", "Required fields must be set before the Swytch creation: " + ", ".join(missing))
        return ret
    
