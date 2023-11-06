from .common_webscraper_functions import get_element, get_children_element, row_has_link, true, get_field_with_text
import logging

class HTMLObjectIteratorFactory:


    def _get_narrow_down_function(self):
        function_name = self.data_dict['narrow_down_function']
        if function_name == 'row_has_link':
            return row_has_link
        elif function_name == 'object_has_text':
            return get_field_with_text(self.data_dict['text'])
        elif function_name == 'true':
            return true
        else:
            raise Exception("No match for narrow down function")
        
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def create(self):
        logging.info('[HTMLObjectIteratorFactory] [create] self.data_dict: ' + str(self.data_dict))
        base_object_fetcher = ObjectFetcherFactory(self.data_dict['base_object']).get_object_fetcher()
        children_object_fetcher = ChildrenObjectFetcher(self.data_dict['children_objects'])
        narrow_down_function = self._get_narrow_down_function()
        return HTMLObjectIterator(base_object_fetcher, children_object_fetcher, narrow_down_function, self.data_dict['may_not_exist'])


class HTMLObjectIterator:

    def __init__(self, base_object_fetcher, children_object_fetcher, narrow_down_function, may_not_exist):
        self.base_object_fetcher = base_object_fetcher
        self.children_object_fetcher = children_object_fetcher 
        self.narrow_down_function = narrow_down_function 
        self.may_not_exist = may_not_exist

    def get_valid_elements(self, soup):
        return_array = []
        base_object = self.base_object_fetcher.fetch(soup)
        if base_object is None and self.may_not_exist:
            return return_array
        logging.info('[HTMLObjectIterator] [get_valid_elements] base_object: ' + str(base_object))
        for eligible_element in self.children_object_fetcher.fetch_children(base_object):
            logging.info('[HTMLObjectIterator] [get_valid_elements] eligible_element ' + str(eligible_element))
            if self.narrow_down_function(eligible_element):
                logging.info('[HTMLObjectIterator] [get_valid_elements] adding_element: ' + str(eligible_element))
                return_array.append(eligible_element)
        return return_array




class ObjectFetcherFactory:

    def __init__(self, definition_dict):
        self.definition_dict = definition_dict

    def get_object_fetcher(self):
        child_fetcher = None
        if 'child' in self.definition_dict.keys():
            child_fetcher = ObjectFetcherFactory(self.definition_dict['child']).get_object_fetcher()
        return ObjectFetcher(self.definition_dict, child_fetcher)

class ObjectFetcher:

    def __init__(self, definition_dict, child_fetcher=None):
        self.element_function = get_element(definition_dict)
        self.child_fetcher = child_fetcher 


    def fetch(self, soup): 
        return_element = self.element_function(soup)
        if return_element is None:
            return None
        if self.child_fetcher is not None:
            return_element =  self.child_fetcher.fetch(return_element)  
        return return_element

class ChildrenObjectFetcher:

    def __init__(self, definition_dict):
        self.children_element_function = get_children_element(definition_dict)

    def fetch_children(self, soup):
        return self.children_element_function(soup)