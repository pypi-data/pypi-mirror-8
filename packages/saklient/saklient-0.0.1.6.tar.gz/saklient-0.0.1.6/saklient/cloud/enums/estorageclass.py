# -*- coding:utf-8 -*-

from ...util import Util

# module saklient.cloud.enums.estorageclass

class EStorageClass:
    ## ストレージのクラスを表す列挙子。
    
    ISCSI1204 = "iscsi1204"
    iscsi1204 = "iscsi1204"
    
    ## @ignore
    _MAP = {
        "ISCSI1204": 110
    }
    
    ## @ignore
    @classmethod
    def compare(clazz, lhs, rhs):
        if not (isinstance(lhs, str) and isinstance(rhs, str)): return None
        lhs = lhs.upper()
        rhs = rhs.upper()
        if lhs not in clazz._MAP or rhs not in clazz._MAP: return None
        d = clazz._MAP[lhs] - clazz._MAP[rhs]
        return (0<d) - (d<0)
    
    
