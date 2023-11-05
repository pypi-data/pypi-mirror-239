from bradleystevenson2015_database import database
import json
from bradleystevenson2015_webscraper.common_webscraper_functions import fetch_soup_from_page
from bradleystevenson2015_webscraper.parser import CreateFromPageParserFactory, ParserObjectFactory
from bradleystevenson2015_webscraper.url_generator import URLGeneratorFactory
import logging


class WebscraperObjectCollection:

    def __init__(self, webscraper_schema_filepath, database_path, database_schema_filepath, custom_objects):
        self.databaseObject = database.Database(database_path, database_schema_filepath)
        self._create_webscraper_objects(webscraper_schema_filepath, custom_objects)


    def _create_webscraper_objects(self, webscraper_schema_filepath, custom_objects):
        self.webscrapers = []
        file = open(webscraper_schema_filepath)
        data = json.load(file)
        file.close()
        for webscraper_object in data['objects']:
            self.webscrapers.append(WebscraperObjectFactory(webscraper_object, custom_objects).create())


    def get_webscraper_object_with_name(self, object_name):
        for webscraper in self.webscrapers:
            if webscraper.object_name == object_name:
                return webscraper

    def run(self, arguments):
        if '--create-tables' in arguments:
            self.run_create_tables()
        if '--help' in arguments:
            self.run_help()
        if '--single-page' in arguments:
            self.run_single_page
        self.run_normal(arguments)

    def run_help(self):
        print('--help')
        print(' print the help menu')
        print('--create-tables')
        print(' create the different tables in the database')
        print('--single-page')
        print(' create from a single page')
        print(' arguments:')
        print('     object_name: name of the object to run this for')
        print('     url: url of the page to test')
        print('     data_dict: data dict of the object to run')
        exit(0)

    def run_create_tables(self):
        self.databaseObject.create_tables()
        exit(0)

    def run_normal(self, arguments):
        create_from_web_dict = self._parse_arguments(arguments)
        for webscraper in self.webscrapers:
            webscraper.create(create_from_web_dict[webscraper.object_name], self)
        self.databaseObject.insert_into_database()

    def run_single_page(self, arguments):
        object_name = arguments[3]
        url = arguments[4]
        data_dict = arguments[5]
        url_dict = {'url': url, 'data_dict': data_dict}
        return_data = self.objects[object_name].create_from_url(url_dict, self)
        print(str(return_data))
        exit(0)
    

    def _parse_arguments(self, arguments):
        logging.info("[WEBSCRAPER] [_parse_arguments] arguments: " + str(arguments))
        return_dict = {}
        for webscraper in self.webscrapers:
            return_dict[webscraper.object_name] = False
        for argument in arguments[1:]:
            if argument not in return_dict.keys() and argument != 'all':
                raise Exception("No match for object name")
            return_dict[argument] = True
        if 'all' in arguments[1:]:
            for key in return_dict.keys():
                return_dict[key] = True
        return return_dict


class WebscraperObject:

    def __init__(self, object_name, tables, create_from_page_parser=None):
        self.object_name = object_name
        self.tables = tables
        self.create_from_page_parser = create_from_page_parser

    def create(self, create_from_web, webscraperObjectCollection):
        logging.info("[WebscraperObject] [create] " + self.object_name + " " + str(create_from_web))
        if create_from_web:
            self.create_from_web(webscraperObjectCollection)
        else:
            self.create_from_database(webscraperObjectCollection)

    def create_from_web(self, webscraperObjectCollection):
        pass

    def create_from_database(self, webscraperObjectCollection):
        for table_name in self.tables:
            webscraperObjectCollection.databaseObject.tables[table_name].generate_from_database()

    def create_from_page(self, url, webscraperObjectCollection):
        if self.create_from_page_parser is None:
            raise Exception("We have no way to create this object")
        data_dict = self.create_from_page_parser.parse(url, webscraperObjectCollection)
        data_dict['url'] = url
        return webscraperObjectCollection.databaseObject.tables[self.tables[0]].append(data_dict)
    
class NewWebscraperObject(WebscraperObject):

    def __init__(self, object_name, parsers, url_generator, create_from_page_parser):
        self.object_name = object_name
        self.parsers = parsers
        self.create_from_page_parser = create_from_page_parser
        self.url_generator = url_generator
        super().__init__(object_name, [object_name], create_from_page_parser)

    def create_from_web(self, webscraperObjectCollection):
        url_dicts = self.url_generator.generate_urls(webscraperObjectCollection)
        logging.info('[WEBSCRAPER] [WebscraperObject] [create_from_web] url_dicts: ' + str(url_dicts))
        for url_dict in url_dicts:
            data_dicts = self.create_from_url(webscraperObjectCollection, url_dict)
            for data_dict in data_dicts:
                webscraperObjectCollection.databaseObject.tables[self.object_name].append(data_dict)


    def create_from_url(self, webscraper_object_collection, url_dict):
        logging.info('[WebscraperObject] [create_from_url] url_dict: ' + str(url_dict))
        soup = fetch_soup_from_page(url_dict['url'])
        return_data = []
        for parser in self.parsers:
            data = parser.parse_page(soup, url_dict['data_dict'], webscraper_object_collection)
            return_data.extend(data)
        return return_data




class WebscraperObjectFactory:

    def __init__(self, webscraper_object_dict, custom_objects):
        self.webscraper_object_dict = webscraper_object_dict
        self.custom_objects = custom_objects


    def create(self):
        create_from_page_parser = None
        if 'create_from_page_parser' in self.webscraper_object_dict.keys():
            create_from_page_parser =  CreateFromPageParserFactory(self.webscraper_object_dict['create_from_page_parser']).create_from_page_parser
        if 'object_type' not in self.webscraper_object_dict.keys():
            parsers = []
            for parser_dict in self.webscraper_object_dict['parsers']:
                parsers.append(ParserObjectFactory(parser_dict).parser)
            url_generator = URLGeneratorFactory(self.webscraper_object_dict['urls']).get_url_generator()
            return NewWebscraperObject(self.webscraper_object_dict['object_name'], parsers, url_generator, create_from_page_parser)
        elif self.webscraper_object_dict['object_type'] == 'custom_object':
            for custom_object in self.custom_objects:
                if custom_object.object_name == self.webscraper_object_dict['object_name']:
                    return custom_object
        else:
            raise Exception("No match for object type")
