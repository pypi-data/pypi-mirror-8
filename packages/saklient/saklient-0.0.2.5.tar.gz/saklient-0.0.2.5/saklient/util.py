# -*- coding:utf-8 -*-

import datetime, re, types, time, urllib.parse
from .errors.saklientexception import SaklientException

# module saklient.util

class Util:
    
    ## @ignore
    @staticmethod
    def exists_path(obj, path):
        a_path = path.split(".")
        for seg in a_path:
            if obj is None: return False
            if not isinstance(obj, dict): return False
            if seg == "": continue
            if seg not in obj: return False
            obj = obj[seg]
        return True
    
    ## @ignore
    @staticmethod
    def get_by_path(obj, path):
        a_path = path.split(".")
        for seg in a_path:
            if obj is None: return None
            if not isinstance(obj, dict): return None
            if seg == "": continue
            if seg not in obj: return None
            obj = obj[seg]
        return obj
  
    ## @ignore
    @staticmethod
    def get_by_path_any(objects, pathes):
        for obj in objects:
            for path in pathes:
                ret = Util.get_by_path(obj, path)
                if ret is not None: return ret
        return None
    
    ## @ignore
    @staticmethod
    def set_by_path(obj, path, value):
        a_path = path.split(".")
        key = a_path.pop()
        for seg in a_path:
            if seg == "": continue
            if seg not in obj: obj[seg] = {}
            obj = obj[seg]
        obj[key] = value
    
    ## @ignore
    @staticmethod
    def create_class_instance(classPath, arguments):
        ret = None
        p = classPath.split(".")
        c = p.pop()
        m = __import__(classPath.lower(), fromlist=[c])
        ret = getattr(m, c)(*arguments)
        if ret is None:
            raise Exception.new("Could not create class instance of " + classPath)
        return ret
    
    ## @ignore
    @staticmethod
    def str2date(s):
        if s is None:
            return None
        return datetime.datetime.strptime(re.sub(r"([+-][0-9]{2}):([0-9]{2})$", "\\1\\2", s), "%Y-%m-%dT%H:%M:%S%z")
    
    ## @ignore
    @staticmethod
    def date2str(d):
        if d is None:
            return None
        return d.strftime("%Y-%m-%dT%H:%M:%S%z")
    
    ## @ignore
    @staticmethod
    def url_encode(s):
        return urllib.parse.quote_plus(s)
    
    ## @ignore
    @staticmethod
    def sleep(sec):
        time.sleep(sec)
    
    ## @ignore
    @staticmethod
    def validate_arg_count(actual, expected):
        if actual < expected: raise SaklientException('argument_count_mismatch', 'Argument count mismatch')
    
    ## @ignore
    @staticmethod
    def validate_type(value, type_name, force=False):
        is_ok = False
        if not force:
            if type_name=="any" or type_name=="void" or value is None: return
            clazz = type(value)
            if (type_name == "function"):
                is_ok = isinstance(value, types.FunctionType)
            elif (type_name in {"str", "float", "int", "bool", "dict", "list"}):
                is_ok = type(value).__name__ == type_name
            else:
                p = type_name.split(".")
                if 1 < len(p):
                    c = p.pop()
                    m = __import__(".".join(p), fromlist=[c])
                    is_ok = isinstance(value, getattr(m, c))
                else:
                    c = globals()["__builtins__"][type_name]
                    is_ok = isinstance(value, c)
            
        if not is_ok:
            raise SaklientException("argument_type_mismatch", "Argument type mismatch (expected "+type_name+", got "+str(type(value))+")")

