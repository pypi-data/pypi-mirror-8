# -*- coding:utf-8 -*-

from .models.model_region import Model_Region
from .client import Client
from ..util import Util

# module saklient.cloud.facility

class Facility:
    ## 設備情報にアクセスするためのモデルを集めたクラス。
    
    # (instance field) _region
    
    ## @return {saklient.cloud.models.model_region.Model_Region}
    def get_region(self):
        return self._region
    
    ## リージョン情報。
    region = property(get_region, None, None)
    
    ## @ignore
    # @param {saklient.cloud.client.Client} client
    def __init__(self, client):
        Util.validate_type(client, "saklient.cloud.client.Client")
        self._region = Model_Region(client)
    
