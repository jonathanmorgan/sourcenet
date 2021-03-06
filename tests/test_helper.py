from __future__ import unicode_literals

'''
Copyright 2010-2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_text.

context_text is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_text is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_text. If not, see http://www.gnu.org/licenses/.
'''


#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# python libraries

# Django imports
from django.contrib.auth.models import User
from django.core.management import call_command

# import basic django configuration application.
from django_config.models import Config_Property

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper

# context imports
import context.tests.test_helper

# context_text imports
from context_text.article_coding.open_calais_v2.open_calais_v2_article_coder import OpenCalaisV2ArticleCoder
from context_text.models import Article
from context_text.models import Newspaper
from context_text.shared.context_text_base import ContextTextBase


#================================================================================
# Shared variables and functions
#================================================================================


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class TestHelper( context.tests.test_helper.TestHelper ):

    
    #----------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # ! ----> fixtures

    # standard context entity setup fixture
    FIXTURE_UNIT_TEST_CONTEXT_BASE = "context-sourcenet_entity_and_relation_types.json"

    # fixtures paths, in order they should be loaded.
    FIXTURE_UNIT_TEST_AUTH_DATA = "context_text_unittest_auth_data.json"
    FIXTURE_UNIT_TEST_CONFIG_PROPERTIES = "context_text_unittest_django_config_data.json"
    FIXTURE_UNIT_TEST_BASE_DATA = "context_text_unittest_data.json"
    FIXTURE_UNIT_TEST_TAGGIT_DATA = "context_text_unittest_taggit_data.json"
    
    # list of fixtures, in order.
    FIXTURE_LIST = []
    FIXTURE_LIST.append( FIXTURE_UNIT_TEST_AUTH_DATA )
    FIXTURE_LIST.append( FIXTURE_UNIT_TEST_CONFIG_PROPERTIES )
    FIXTURE_LIST.append( FIXTURE_UNIT_TEST_BASE_DATA )
    FIXTURE_LIST.append( FIXTURE_UNIT_TEST_TAGGIT_DATA )
    
    # fixtures for exporting complete data to context
    FIXTURE_UNIT_TEST_EXPORT_AUTH_DATA = "context_text_unittest_export_auth_data.json"
    FIXTURE_UNIT_TEST_EXPORT_BASE_DATA = "context_text_unittest_export_data.json"
    FIXTURE_UNIT_TEST_EXPORT_TAGGIT_DATA = "context_text_unittest_export_taggit_data.json"

    # list of export testing fixtures, in order.
    EXPORT_FIXTURE_LIST = []
    EXPORT_FIXTURE_LIST.append( FIXTURE_UNIT_TEST_EXPORT_AUTH_DATA )
    EXPORT_FIXTURE_LIST.append( FIXTURE_UNIT_TEST_CONFIG_PROPERTIES )
    EXPORT_FIXTURE_LIST.append( FIXTURE_UNIT_TEST_EXPORT_BASE_DATA )
    EXPORT_FIXTURE_LIST.append( FIXTURE_UNIT_TEST_EXPORT_TAGGIT_DATA )
    EXPORT_FIXTURE_LIST.append( FIXTURE_UNIT_TEST_CONTEXT_BASE )
    
    #----------------------------------------------------------------------------
    # ! ----> OpenCalais

    OPEN_CALAIS_ACCESS_TOKEN_FILE_NAME = "open_calais_access_token.txt"

    # Test user
    #TEST_USER_NAME = "test_user"
    #TEST_USER_EMAIL = "test@email.com"
    #TEST_USER_PASSWORD = "calliope"

    # test authors
    TEST_AUTHOR_1 = "Nate Reems"
    TEST_AUTHOR_2 = "Nardy Baeza Bickel"
    TEST_AUTHOR_LIST = [ TEST_AUTHOR_1, TEST_AUTHOR_2 ]

    # test subjects
    TEST_SUBJECT_1 = "Alex McNamara"
    TEST_SUBJECT_2 = "Justin VanderVelde"
    TEST_SUBJECT_3 = "Pete Goodell"
    TEST_SUBJECT_4 = "Bob Dukesherer"
    TEST_SUBJECT_5 = "Steve Brown"
    TEST_SUBJECT_6 = "Rick DeGraaf"
    TEST_SUBJECT_LIST = [ TEST_SUBJECT_1, TEST_SUBJECT_2, TEST_SUBJECT_3, TEST_SUBJECT_4, TEST_SUBJECT_5, TEST_SUBJECT_6 ]

    # test quotations
    TEST_QUOTATION_1 = "The snow-covered runs are a beautiful sight to snowboarders Alex McNamara and Justin VanderVelde."
    TEST_QUOTATION_2 = "The Rockford friends, who have been practicing jumping and twirling tricks at Cannonsburg for a decade, said a \"long\" summer and fall left them eager to bust out their boards."
    
    #----------------------------------------------------------------------------
    # ! ----> Context-related variables.

    # ! --------> Entity_Identifier_Type
    
    # entity identifier types - testing
    IDENTIFIER_TYPE_NAME_DOES_NOT_EXIST = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_NAME_DOES_NOT_EXIST

    # entity identifier types - general
    IDENTIFIER_TYPE_NAME_PERMALINK = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_PERMALINK
    
    # entity identifier types - articles
    IDENTIFIER_TYPE_NAME_ARTICLE_ARCHIVE_IDENTIFIER = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_ARTICLE_ARCHIVE_IDENTIFIER
    IDENTIFIER_TYPE_NAME_ARTICLE_NEWSBANK_ID = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_ARTICLE_NEWSBANK_ID
    IDENTIFIER_TYPE_NAME_ARTICLE_SOURCENET_ID = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_ARTICLE_SOURCENET_ID

    # entity identifier types - newspaper
    IDENTIFIER_TYPE_NAME_NEWSPAPER_NEWSBANK_CODE = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_NEWSPAPER_NEWSBANK_CODE
    IDENTIFIER_TYPE_NAME_NEWSPAPER_SOURCENET_ID = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_NEWSPAPER_SOURCENET_ID

    # entity identifier types - organization
    IDENTIFIER_TYPE_NAME_ORGANIZATION_SOURCENET_ID = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_ORGANIZATION_SOURCENET_ID

    # entity identifier types - person
    IDENTIFIER_TYPE_NAME_PERSON_OPEN_CALAIS_UUID = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_NAME_PERSON_OPEN_CALAIS_UUID
    IDENTIFIER_TYPE_NAME_PERSON_SOURCENET_ID = ContextTextBase.CONTEXT_ENTITY_ID_TYPE_NAME_PERSON_SOURCENET_ID

    # map of identifier type names to test IDs
    IDENTIFIER_TYPE_NAME_TO_ID_MAP = {}
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_PERSON_SOURCENET_ID ] = 1
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_PERSON_OPEN_CALAIS_UUID ] = 2
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_ARTICLE_SOURCENET_ID ] = 3
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_ARTICLE_NEWSBANK_ID ] = 4
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_PERMALINK ] = 5
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_ARTICLE_ARCHIVE_IDENTIFIER ] = 6
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_NEWSPAPER_SOURCENET_ID ] = 7
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_NEWSPAPER_NEWSBANK_CODE ] = 8
    IDENTIFIER_TYPE_NAME_TO_ID_MAP[ IDENTIFIER_TYPE_NAME_ORGANIZATION_SOURCENET_ID ] = 9    
    
    # ! --------> Entity_Type
    
    # Entity Type slugs
    ENTITY_TYPE_SLUG_ARTICLE = ContextTextBase.CONTEXT_ENTITY_TYPE_SLUG_ARTICLE
    ENTITY_TYPE_SLUG_NEWSPAPER = ContextTextBase.CONTEXT_ENTITY_TYPE_SLUG_NEWSPAPER
    ENTITY_TYPE_SLUG_PERSON = ContextTextBase.CONTEXT_ENTITY_TYPE_SLUG_PERSON
    
    # ! --------> trait names
    
    TEST_ENTITY_TRAIT_NAME = "flibble_glibble_pants"
    
    # ! --------> identifier names
    
    TEST_IDENTIFIER_NAME = "nickname"

    #----------------------------------------------------------------------------
    # Class variables - overriden by __init__() per instance if same names, but
    #    if not set there, shared!
    #----------------------------------------------------------------------------

    
    DEBUG = True


    #-----------------------------------------------------------------------------
    # ! ==> class methods
    #-----------------------------------------------------------------------------


    @classmethod
    def filter_article_data_open_calais_v2( cls, article_data_qs_IN ):
    
        # return reference
        qs_OUT = None
        
        # declare variables
        automated_coder_user = None
        
        # get automated coder
        automated_coder_user = ContextTextBase.get_automated_coding_user()
        
        # filter
        qs_OUT = article_data_qs_IN
        qs_OUT = qs_OUT.filter( coder = automated_coder_user )
        qs_OUT = qs_OUT.filter( coder_type = OpenCalaisV2ArticleCoder.CONFIG_APPLICATION )
        
        return qs_OUT
        
    #-- END method filter_article_data_open_calais_v2() --#
        
    
    @classmethod
    def load_open_calais_access_token( cls, directory_path_IN = "" ):
        
        # return references
        value_OUT = ""
        
        # declare variables
        file_path = ""
        file_pointer = None
        file_contents = ""
        config_property_qs = None
        config_property_count = -1
        config_property = None
        
        # loading file with API key in it.  Start with standard file name.
        file_path = cls.OPEN_CALAIS_ACCESS_TOKEN_FILE_NAME
        
        # got a directory path?
        if ( ( directory_path_IN is not None ) and ( directory_path_IN != "" ) ):
        
            # got a path - add file name to the end of it.
            file_path = directory_path_IN + "/" + file_path
            
        #-- END check for path passed in. --#

        # open the file and read the contents.
        with open( file_path, "rU" ) as file_pointer:
        
            # read contents into a variable
            file_contents = file_pointer.read()
            file_contents = file_contents.strip()
        
        #-- END file processing --#
        
        # got anything?
        if ( ( file_contents is not None ) and ( file_contents != "" ) ):
        
            # yes - there are contents.  place in configuration property.
            
            # first, try to retrieve the config property.
            config_property_qs = Config_Property.objects.filter( application = OpenCalaisV2ArticleCoder.CONFIG_APPLICATION )
            config_property_qs = config_property_qs.filter( property_name = OpenCalaisV2ArticleCoder.CONFIG_PROP_OPEN_CALAIS_ACCESS_TOKEN )
            
            # got anything?
            config_property_count = config_property_qs.count()
            if ( config_property_count == 0 ):
            
                # no match.  Create the property...
                config_property = Config_Property()
                config_property.application = OpenCalaisV2ArticleCoder.CONFIG_APPLICATION
                config_property.property_name = OpenCalaisV2ArticleCoder.CONFIG_PROP_OPEN_CALAIS_ACCESS_TOKEN
                config_property.save()
                
                # ...and retrieve it into a QuerySet
                config_property_qs = Config_Property.objects.filter( pk = config_property.id )
                
            #-- END check to see if we have right number of things. --#
            
            # get() the property instance - Will throw exception if > 1.
            config_property = config_property_qs.get()
            
            # set value
            config_property.property_value = file_contents
            
            # save
            config_property.save()
        
        #-- END check to see if anything in the file --#
        
        value_OUT = file_contents
        
        return value_OUT
        
    #-- END function load_open_calais_access_token() --#
    
    
    @classmethod
    def standardOpenCalaisSetUp( cls, test_case_IN = None ):
        
        """
        setup tasks.  Call function that we'll re-use.
        """

        # declare variables
        me = "standardOpenCalaisSetUp"
        status_instance = None
        current_fixture = ""
        
        print( "\n\nIn TestHelper." + me + "(): starting standardOpenCalaisSetUp.\n" )
        
        # see if test case passed in.  If so, set status variables on it.
        if ( test_case_IN is not None ):
        
            # not None, set status variables on it.
            status_instance = test_case_IN
            
        else:
        
            # no test case passed in.  Just set on self.
            status_instance = self
        
        #-- END check to see if test case --#

        # call standardSetup.
        cls.standardSetUp( status_instance, cls.FIXTURE_LIST )
        
        # Load OpenCalais Access Token.
        try:
        
            cls.load_open_calais_access_token()

        except Exception as e:
        
            # looks like there was a problem.
            status_instance.setup_error_count += 1
            status_instance.setup_error_list.append( OpenCalaisV2ArticleCoder.CONFIG_PROP_OPEN_CALAIS_ACCESS_TOKEN )
            
        #-- END try/except --#
        
        print( "In TestHelper." + me + "(): standardOpenCalaisSetUp complete." )

    #-- END function standardOpenCalaisSetUp() --#
        

    #----------------------------------------------------------------------------
    # ! ==> __init__() method
    #----------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( TestHelper, self ).__init__()

    #-- END method __init__() --#


    #----------------------------------------------------------------------------
    # ! ==> instance methods, in alphabetical order
    #----------------------------------------------------------------------------


#-- END class TestHelper --#