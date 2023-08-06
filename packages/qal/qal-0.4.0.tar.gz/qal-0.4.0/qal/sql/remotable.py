'''
Created on Sep 30, 2013

@author: Nicklas Boerjesson
'''
from qal.dal.dal import DatabaseAbstractionLayer

class ParameterRemotable(object):
    """This class is an auxilliary class for all parameter classes that are remotable. 
    That is, they can fetch their data from, or perform their actions at, a different location than the parent class.
    If they return data, the data will be held in the temporary table, where it can be joined with or otherwise managed.
    """
    """The temporary table name is used by owners to reference the data correctly. It is prefixed by an underscore to 
    not be shown in the external structure.(it is possible that it will be removed)"""
    _temporary_table_name = None
    """The resource object, usually loaded by the XML importer"""
    _resource = None
    """The classes' DAL connection."""
    _dal = None
    """The nearest parent that is in another database context than self"""
    _out_of_context_parent = None
    """This value identifies what context this part of the query resides in"""
    resource_uuid = None
    
            
    def _bring_into_context(self, _db_type):
        """The _bring_into_context function checks whether the resource GUID is set and if resources need fetching
        If so, it fetches the data and puts it into a dataset, which is then inserted into the parents context.
        The parent is referenced to as the out-of-context parent.
        """
       
        print(self.__class__.__name__ + "._bring_into_context: Needs preparing, preparing for resource_uuid: " + str(self.resource_uuid))
        
        if not self._resource:
            raise Exception(self.__class__.__name__ + "._bring_into_context - Error: _resource not cached")
        
        # Generate random temp table name, max 1 (#) + 8 alphanumeric characters
        import random
        import string
        char_set = string.ascii_lowercase + string.digits
        _tmp_table_name = '#' +''.join(random.sample(char_set*8,8))
       
        from qal.sql.sql import ParameterIdentifier
        
        if self._resource.type.upper() == 'RDBMS':
            if not self._dal:
                """Make connection to resource defined by the resource_uuid"""
                self._dal = DatabaseAbstractionLayer(_resource = self._resource)
                self._dal.connect_to_db()
            
            _source_sql = self._generate_sql(self._dal.db_type)
            from qal.sql.sql import ParameterSource
            if  isinstance(self, ParameterSource):
                print("is ParameterSource")
                if isinstance(self.expression[0], ParameterIdentifier):
                    
                    _source_sql = 'SELECT * FROM ' + self.expression[0].as_sql(self._dal.db_type)
                    if _tmp_table_name[1] == "#":
                        self.expression[0].identifier = _tmp_table_name[1:len(_tmp_table_name)]
                    else:
                        self.expression[0].identifier = _tmp_table_name
                    

            _data = self._dal.query(_source_sql)
            _field_names = self._dal.field_names
            _field_types = self._dal.field_types
            self._dal.close()
            
        elif self._resource.type.upper() in ["FLATFILE"]:

            from qal.dataset.flatfile import FlatfileDataset
            
            self._data_source = FlatfileDataset(_resource = self._resource)
            
            _data = self._data_source.load()
            _field_names = self._data_source.field_names
            _field_types = ["string"] * len(_field_names)
            
        elif self._resource.type.upper() in ["XPATH"]:    
            from qal.dataset.xpath import XpathDataset
            
            self._data_source = XpathDataset(_resource = self._resource)
            
            _data = self._data_source.load()
            _field_names = self._data_source.field_names
            _field_types = self._data_source.field_types
                  
        else:
            raise Exception(self.__class__.__name__ + "._bring_into_context - Error: Invalid resource type : " + str(self._resource.type))    

        
        """Does the out-of-context parent have a connection? If so, that's where the data should go."""
        if self._out_of_context_parent._dal:
            _parent_dal = self._out_of_context_parent._dal
        else:
            """If it doesn't, create one to the resource, and use that."""
            _parent_dal = DatabaseAbstractionLayer(_resource=self._out_of_context_parent._resource)
            _parent_dal.connect_to_db()
            """Also set the parents _dal, since we are using temporary tables, they need to be in the same context.""" 
            self._out_of_context_parent._dal = _parent_dal
            
        """ The sql_macros library is imported locally, to not interfere with the qal.sql.* structure."""
        from qal.sql.macros import copy_to_table             
        """Copy the data into the parents' context so the parent can access it."""
        _table_name = copy_to_table(_dal = _parent_dal, _values =_data, _field_names = _field_names, _field_types = _field_types, _table_name = _tmp_table_name, _create_table = True)
        
        _ident = ParameterIdentifier(_identifier = _table_name)
        return _ident.as_sql(_parent_dal.db_type)
        

    def _check_need_prepare(self):
        """
        Checks context, whether a call to _bring_into_context is needed. It is needed if:
        1. If the nearest parent with resource has a different resource ID
        2. If no parent has a resourceID
        
        It is NOT needed if the nearest parent with resource has the same ID. 
        
        """
        _curr_parent = self._parent
        while _curr_parent:
            print(self.__class__.__name__ + "._check_need_prepare: level up" + str(_curr_parent))
            if hasattr(_curr_parent, 'resource_uuid') and _curr_parent.resource_uuid:
                if self.resource_uuid == _curr_parent.resource_uuid:
                    if _curr_parent._dal != None: 
                        self._dal = _curr_parent
                    return False
                else:
                    print(self.__class__.__name__ + "._check_need_prepare: Different resource uuid found:" + str(_curr_parent.resource_uuid) + " (own: " +str(self.resource_uuid)+ ")")
                    self._out_of_context_parent = _curr_parent
                    return True
            _curr_parent = _curr_parent._parent

        return False
                
