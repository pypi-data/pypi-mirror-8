# -*- coding:utf-8 -*-

from ...util import Util

# module saklient.cloud.enums.eavailability

class EAvailability:
    ## リソースの有効性を表す列挙子。
    
    SELECTABLE = "selectable"
    selectable = "selectable"
    
    MIGRATING = "migrating"
    migrating = "migrating"
    
    PRECREATE = "precreate"
    precreate = "precreate"
    
    REPLICATING = "replicating"
    replicating = "replicating"
    
    TRANSFERING = "transfering"
    transfering = "transfering"
    
    STOPPED = "stopped"
    stopped = "stopped"
    
    FAILED = "failed"
    failed = "failed"
    
    CHARGED = "charged"
    charged = "charged"
    
    UPLOADING = "uploading"
    uploading = "uploading"
    
    AVAILABLE = "available"
    available = "available"
    
    ## @ignore
    _MAP = {
        "SELECTABLE": 69,
        "MIGRATING": 70,
        "PRECREATE": 71,
        "REPLICATING": 72,
        "TRANSFERING": 73,
        "STOPPED": 75,
        "FAILED": 78,
        "CHARGED": 79,
        "UPLOADING": 80,
        "AVAILABLE": 100
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
    
    
