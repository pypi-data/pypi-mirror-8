'''
Created on Sep 19, 2010

@author: Nicklas Boerjesson
@note: This module accesses the Parameter_* and Verb_* classes 
from the SQL.py and generates meta data by analyzing its objects.
'''

# Import the entire SQL namespace to make it searchable and suppress warnings.
from qal.sql.sql import * #@UnusedWildImport #IGNORE:W0401
from qal.sql.base import *
from qal.sql.remotable import *
from qal.dataset.flatfile import FlatfileDataset #@UnusedWildImport #IGNORE:W0401
from qal.dataset.xpath import XpathDataset #@UnusedWildImport #IGNORE:W0401
from qal.dataset.matrix import MatrixDataset #@UnusedWildImport #IGNORE:W0401

def list_parameter_classes():
    """List all parameter classes"""
    result = list()
    for k in globals().items():
        if (k[0][0:9]).lower() == 'parameter':
            result.append(k[0]) 
    return result    
def list_verb_classes():
    """List all verb classes"""
    result = list()
    for k in globals().items():
        if (k[0][0:4]).lower() == 'verb':
            result.append(k[0]) 
    return result    

def list_class_properties(_classname):
    """List properties for the class specified in _classname"""
    _classname = _classname.rpartition(".")[2]
    result = list()
    if (_classname in globals()):
        for k in globals()[_classname].__dict__.items():
            if not hasattr(k[1], '__call__') and k[0][0:1] != '_': 
                result.append(k[0])
        _mro_length = len(globals()[_classname]().__class__.__mro__)        
        if _mro_length > 2:
            for _mro_idx in range(1, _mro_length - 1):
                result.extend(list_class_properties(globals()[_classname]().__class__.__mro__[_mro_idx].__name__))
    
    return result

def find_class(_name, _raiserror = True):
    """Using name, find a class reference""" 
    try:
    
        Obj = None
        ObjName = None
        for k in globals().items():
            if k[0].lower() == _name.lower():
                Obj = k[1]()
                ObjName = k[0]
                break
        # Python types
        if _name == "list":
            return [], "list"
    except Exception as e:
        raise Exception("sql_meta - find_class: Error looking for " + str(_name) + " : " + str(e))
    
    if (Obj == None and _raiserror):
        raise Exception("sql_meta - find_class: Cannot find matching class - " + _name)
    
    return Obj, ObjName
    
                
