'''
Created on Sep 14, 2012

@author: Nicklas Boerjesson
'''
from datetime import date
import datetime
from itertools import islice
from qal.common.strings import make_path_absolute, string_to_bool

from qal.dataset.custom import CustomDataset

import csv
from urllib.parse import unquote


class FlatfileDataset(CustomDataset):
    """This class loads a flat file into an array, self.data_table."""
    delimiter = None
    """The delimiter, typically ";", "," or "|"."""
    has_header = None
    """True if data begins with a header row containing field names."""
    filename = None
    """The name of the file"""
    field_names = None
    """The names of the fields(if applicable, see has_header)"""
    csv_dialect = None
    """Specifies the csv dialect"""
    quoting = None
    """To what degree does the file employ quoting, values:
     * None = No quoting at all, quotes will be treated as values
     * "MINIMAL" = Quoting is only used when necessary
     * "ALL" = Quoting is applied used on all fields.
     * "NONNUMERIC" = Non-numeric fields are quoted."""
    quotechar = "\""
    """What character to use for quoting. Normally "\\"\"."""
    escapechar = None
    """What character is used to escape special characters, typically "\\"."""
    lineterminator = None
    """What character is used to indicate the end of a line. typically "\\n"."""
    skipinitialspace = None
    """True if initial spaces should be disregarded."""
    
    def __init__(self, _delimiter = None, _filename = None, _has_header = None, _csv_dialect = None, _resource = None, _quoting = None, _quotechar = None, _skipinitialspace = None):
        """Constructor"""
        super(FlatfileDataset, self ).__init__()
       
        if _resource != None:
            self.read_resource_settings(_resource)
        else:
            if _delimiter != None: 
                self.delimiter = _delimiter
            else:  
                self.delimiter = None    
            if _filename != None: 
                self.filename = _filename
            else:
                self.filename = None      
            if _has_header != None: 
                self.has_header = _has_header
            else:
                self.has_header = None
                  
            if _csv_dialect != None: 
                self.csv_dialect = _csv_dialect
            else:
                self.csv_dialect = None      
             
            if _quoting != None: 
                self.quoting = _quoting
            else:
                self.quoting = None

            if _quotechar != None:
                self.quotechar = _quotechar
            else:
                self.quotechar = None

            if _skipinitialspace != None:
                self.skipinitialspace = _skipinitialspace
            else:
                self.skipinitialspace = None
        
    def read_resource_settings(self, _resource):
        if _resource.type.upper() != 'FLATFILE':
            raise Exception("FlatfileDataset.read_resource_settings.parse_resource error: Wrong resource type: " + _resource.type)
        self._base_path = _resource.base_path
        self.filename = _resource.data.get("filename")
        self.delimiter = _resource.data.get("delimiter")
        if _resource.data.get("has_header"):
            self.has_header = string_to_bool(str(_resource.data.get("has_header")))
        else:
            self.has_header = None
        self.csv_dialect = _resource.data.get("csv_dialect")
        self.quoting = _resource.data.get("quoting")
        self.escapechar = _resource.data.get("escapechar")
        if _resource.data.get("lineterminator") is not None:
            self.lineterminator = bytes(_resource.data.get("lineterminator"), "UTF-8").decode("unicode-escape")
        else:
            self.lineterminator = None
        self.quotechar = _resource.data.get("quotechar") or '"'       
        self.skipinitialspace = _resource.data.get("skipinitialspace")

    def write_resource_settings(self, _resource):
        # Clear first, one could be overwriting an resource with other data fields
        _resource.data = {}
        _resource.type = _resource.type
        _resource.data["filename"] = self.filename
        _resource.data["delimiter"] = self.delimiter
        _resource.data["has_header"] = self.has_header
        _resource.data["csv_dialect"] = self.csv_dialect
        _resource.data["quoting"] = self.quoting
        _resource.data["escapechar"] = self.escapechar
        _resource.data["lineterminator"] = self.lineterminator
        _resource.data["quotechar"] = self.quotechar
        _resource.data["skipinitialspace"] = self.skipinitialspace
         
    def _quotestr_to_constants(self, _str):
        if _str == None:
            return csv.QUOTE_NONE
        elif _str.upper() == "MINIMAL":
            return csv.QUOTE_MINIMAL
        elif _str.upper() == "ALL":
            return csv.QUOTE_ALL
        elif _str.upper() == "NONNUMERIC":
            return csv.QUOTE_NONNUMERIC
        else:
            raise Exception("Error in _quotestr_to_constants: " + str(_str) + " is an invalid quotestr.")
            

    def load(self):
        """Load data"""
        print("FlatfileDataset.load: Filename='" + str(self.filename) + "', Delimiter='"+str(self.delimiter)+"'" +
              ", Base_path "+ str(self._base_path))
        
        _file = open( make_path_absolute(self.filename, self._base_path), 'r')
        _reader = csv.reader(_file, 
                             delimiter=self.delimiter, 
                             quoting=self._quotestr_to_constants(self.quoting),
                             quotechar = self.quotechar,
                             skipinitialspace = self.skipinitialspace
                             )
        _first_row = True
        self.data_table = []
        for _row in _reader:
            # Save header row if existing.
            if (_first_row):
                if self.has_header == True:
                    self.field_names = [_curr_col.replace("'", "").replace("\"", "") for _curr_col in _row]
                    print("self.field_names :" + str(self.field_names))
                else:
                    self.field_names = []
                    for _curr_idx in range(0,len(_row)):
                        self.field_names.append("Field_"+ str(_curr_idx))

                _first_row = False
            else:
                self.data_table.append(_row)

        _file.close()
        return self.data_table   

    def save(self, _save_as = None):
        """Save data"""

        print("FlatfileDataset.save: Filename='" + str(self.filename) + "', Delimiter='"+str(self.delimiter)+"'")
        
        if _save_as:
            _filename = _save_as
        else:
            _filename =  make_path_absolute(self.filename, self._base_path)
            
        _file = open(_filename, 'w')

        # Work around silly line terminator default, has to be set if passed.
        if self.lineterminator:
            _writer = csv.writer(_file,                              
                             delimiter=self.delimiter, 
                             quoting=self._quotestr_to_constants(self.quoting),
                             quotechar = self.quotechar,
                             skipinitialspace = self.skipinitialspace,
                             lineterminator = self.lineterminator
                             )
        else:
            _writer = csv.writer(_file,                              
                             delimiter=self.delimiter, 
                             quoting=self._quotestr_to_constants(self.quoting),
                             quotechar = self.quotechar,
                             skipinitialspace = self.skipinitialspace
                             )

            
        if self.has_header == True:
            _writer.writerow(self.field_names)
    
            
        _writer.writerows(self.data_table)
            
        _file.close()