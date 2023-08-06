"""
Created on Jan 12, 2014

@author: Nicklas Boerjesson
"""
from qal.dataset.flatfile import FlatfileDataset
from qal.dataset.xpath import XpathDataset
from qal.dataset.rdbms import RDBMSDataset
from qal.dataset.spreadsheet import SpreadsheetDataset


def dataset_from_resource(_resource):
    """Create a qal dataset from a resource"""
    try:
        if _resource.type.upper() == "FLATFILE":
            _ds =  FlatfileDataset(_resource = _resource)
        elif _resource.type.upper() == "XPATH":
            _ds =  XpathDataset(_resource = _resource)
        elif _resource.type.upper() == "RDBMS":
            _ds =  RDBMSDataset(_resource = _resource)
        elif _resource.type.upper() == "SPREADSHEET":
            _ds =  SpreadsheetDataset(_resource = _resource)
        else:
            raise Exception("qal.dataset.factory.dataset_from_resource: Unsupported source resource type: " + str(_resource.type.upper()))
    except Exception as e:
        raise Exception("qal.dataset.factory.dataset_from_resource: Failed loading resource for " + _resource.type.upper() + ".\n" + \
                        "Resource: " + str(_resource.caption)+ "(" + str(_resource.uuid) + ")\n"+ \
                        "Error: \n" + str(e))
        
    return _ds    

if __name__ == '__main__':
    pass