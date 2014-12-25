from __future__ import unicode_literals

'''
Copyright 2010-2014 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet.

sourcenet is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet. If not, see http://www.gnu.org/licenses/.
'''

'''
This code file contains a class that implements functions for interacting with
   the online database of Newsbank.  It mostly includes methods for building and
   connecting to URLs that represent issues of newspapers and articles within an
   issue, and then Beautiful Soup code for interacting with the HTML contents of
   those pages once they are retrieved.  The actual work of retrieving pages is
   outside the scope of this class.
'''

#================================================================================
# Imports
#================================================================================


# python utilities
from python_utilities.network.http_helper import Http_Helper

# parent abstract class.
from sourcenet.article_coding.article_coder import ArticleCoder


#================================================================================
# Package constants-ish
#================================================================================


#================================================================================
# OpenCalaisArticleCoder class
#================================================================================

# define OpenCalaisArticleCoder class.
class OpenCalaisArticleCoder( ArticleCoder ):

    '''
    This class is a helper for Collecting articles out of NewsBank.  It implements
       functions for interacting with the online database of Newsbank.  It mostly
       includes methods for building and connecting to URLs that represent issues
       of newspapers and articles within an issue, and then Beautiful Soup code
       for interacting with the HTML contents of those pages once they are
       retrieved.  The actual work of retrieving pages is outside the scope of
       this class.
    Preconditions: It depends on cookielib, datetime, os, re, sys, urllib2 and
       BeautifulSoup 3.
    '''

    #============================================================================
    # Constants-ish
    #============================================================================
    

    # status constants
    STATUS_SUCCESS = "Success!"
    
    # config application
    CONFIG_APPLICATION = "OpenCalais_REST_API"
    
    # config property names.
    CONFIG_PROP_OPEN_CALAIS_API_KEY = "open_calais_api_key"
    CONFIG_PROP_SUBMITTER = "submitter"
    
    # content types
    CONTENT_TYPE_TEXT = "TEXT/RAW"
    CONTENT_TYPE_HTML = "TEXT/HTML"
    CONTENT_TYPE_DEFAULT = CONTENT_TYPE_HTML
    
    # output formats
    OUTPUT_FORMAT_JSON = "Application/JSON"
    OUTPUT_FORMAT_DEFAULT = OUTPUT_FORMAT_JSON
    
    # Open Calais API URL
    OPEN_CALAIS_REST_API_URL = "http://api.opencalais.com/tag/rs/enrich"
    

    #============================================================================
    # Instance variables
    #============================================================================

    
    # debug
    debug = False
    http_helper = None
    content_type = ""
    output_format = ""

    
    #============================================================================
    # Instance methods
    #============================================================================


    def __init__( self ):

        # call parent's __init__() - I think...
        super( OpenCalaisArticleCoder, self ).__init__()
        
        # initialize variables
        self.http_helper = None
        self.content_type = ""
        self.output_format = ""

    #-- END method __init__() --#


    def code_article( self, article_IN, *args, **kwargs ):

        '''
        purpose: After the ArticleCoder is initialized, this method accepts one
           article instance and codes it for sourcing.  In regards to articles,
           this class is stateless, so you can process many articles with a
           single instance of this object without having to reconfigure each
           time.
        preconditions: load_config_properties() should have been invoked before
           running this method.
        postconditions: article passed in is coded, which means an Article_Data
           instance is created for it and populated to the extent the child
           class is capable of coding the article.
        '''

        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        article_text = None
        article_body_html = ""
        my_http_helper = None
        requests_response = None
        requests_raw_text = ""
        requests_response_json = None

        # got an article?
        if ( article_IN is not None ):

            # then, get text.
            article_text = article_IN.article_text_set.get()
            
            # retrieve article body
            article_body_html = article_text.get_content()
            
            # get Http_Helper instance
            my_http_helper = self.get_http_helper()
            
            # make the request.
            requests_response = my_http_helper.load_url_requests( self.OPEN_CALAIS_REST_API_URL, data_IN = article_body_html )
            
            # raw text:
            requests_raw_text = requests_response.text
            
            # convert to a json object:
            requests_response_json = requests_response.json()
            
            # loop over the stuff in the response:
            print( "=============================================" )
            print( "requests_response_json" )
            print( "=============================================" )
            self.print_calais_json( requests_response_json )

        #-- END check to see if article. --#
        
        return status_OUT

    #-- END abstract method code_article() --#
    

    def get_content_type( self ):

        '''
        Retrieves content type of content to be passed to OpenCalais.
        '''
        
        # return reference
        value_OUT = None

        # get Http_Helper instance.
        value_OUT = self.content_type
        
        # got anything?
        if ( ( value_OUT is None ) or ( value_OUT == "" ) ):
        
            # no - return default.
            value_OUT = self.CONTENT_TYPE_DEFAULT
        
        #-- END check to see if value --#

        return value_OUT

    #-- END get_content_type() --#


    def get_http_helper( self ):

        '''
        Retrieves Http_Helper instance.
        '''
        
        # return reference
        instance_OUT = None

        # get Http_Helper instance.
        instance_OUT = self.http_helper

        return instance_OUT

    #-- END get_http_helper() --#


    def get_output_format( self ):

        '''
        Retrieves output format for OpenCalais request.
        '''
        
        # return reference
        value_OUT = None

        # get Http_Helper instance.
        value_OUT = self.output_format
        
        # got anything?
        if ( ( value_OUT is None ) or ( value_OUT == "" ) ):
        
            # no - return default.
            value_OUT = self.OUTPUT_FORMAT_DEFAULT
        
        #-- END check to see if value --#

        return value_OUT

    #-- END get_output_format() --#


    def init_config_properties( self, *args, **kwargs ):

        '''
        purpose: Called as part of the base __init__() method, so that loading
           config properties can also be included in the parent __init__()
           method.  The application for django_config and any properties that
           need to be loaded should be set here.  To set a property use
           add_config_property( name_IN ).  To set application, use
           set_config_application( app_name_IN ).
        preconditions: None.
        postconditions: This instance should be ready to have
           load_config_properties() called on it after this method is invoked.
        '''

        self.set_config_application( self.CONFIG_APPLICATION )
        self.add_config_property( self.CONFIG_PROP_OPEN_CALAIS_API_KEY )
        self.add_config_property( self.CONFIG_PROP_SUBMITTER )

    #-- END abstract method init_config_properties() --#
    

    def initialize_from_params( self, params_IN, *args, **kwargs ):

        '''
        purpose: Accepts a dictionary of run-time parameters, uses them to
           initialize this instance.
        preconditions: None.
        postconditions: None.
        '''

        # declare variables
        my_http_helper = None
        my_open_calais_api_key = ""
        my_content_type = ""
        my_output_format = ""
        my_submitter = "sourcenet"
        
        # update config properties with params passed in.
        self.update_config_properties( params_IN )
        
        # create Http_Helper
        my_http_helper = Http_Helper()
        
        # retrieve API key.
        my_open_calais_api_key = self.get_config_property( self.CONFIG_PROP_OPEN_CALAIS_API_KEY )
        
        # content type
        my_content_type = self.get_content_type()

        # output format
        my_output_format = self.get_output_format()

        # retrieve submitter
        my_submitter = self.get_config_property( self.CONFIG_PROP_SUBMITTER, "sourcenet" )
        
        # set http headers
        my_http_helper.set_http_header( "x-calais-licenseID", my_open_calais_api_key, None )
        my_http_helper.set_http_header( "Content-Type", my_content_type, None )
        my_http_helper.set_http_header( "outputformat", my_output_format, None )
        my_http_helper.set_http_header( "submitter", my_submitter, None )
        
        # request type
        my_http_helper.request_type = Http_Helper.REQUEST_TYPE_POST
        
        # store the http_helper
        self.set_http_helper( my_http_helper )

    #-- END abstract method initialize_from_params() --#
    

    def output_debug( self, message_IN ):
    
        '''
        Accepts message string.  If debug is on, passes it to print().  If not,
           does nothing for now.
        '''
    
        # got a message?
        if ( message_IN ):
        
            # only print if debug is on.
            if ( self.debug == True ):
            
                # debug is on.  For now, just print.
                print( message_IN )
            
            #-- END check to see if debug is on --#
        
        #-- END check to see if message. --#
    
    #-- END method output_debug() --#


    def print_calais_json( self, json_IN ):
    
        # loop over the stuff in the response:
        item_counter = 0
        current_container = json_IN
        for item in current_container.keys():
        
            item_counter += 1
            print( "==> " + str( item_counter ) + ": " + item )
            
            current_property = "_type"
            if ( current_property in current_container[ item ] ):
                current_property_value = current_container[ item ][ current_property ]
                print( "----> " + current_property + ": " + current_property_value )
                if ( ( current_property_value == "Quotation" ) or ( current_property_value == "Person" ) ):
                    print( current_container[ item ] )
                #-- END check to see if type is "Quotation" --#
            #-- END current_property --#
            current_property = "_typeGroup"
            if ( current_property in current_container[ item ] ):
                current_property_value = current_container[ item ][ current_property ]
                print( "----> " + current_property + ": " + current_property_value )
            #-- END current_property --#
            current_property = "commonname"
            if ( current_property in current_container[ item ] ):
                current_property_value = current_container[ item ][ current_property ]
                print( "----> " + current_property + ": " + current_property_value )
            #-- END current_property --#
            current_property = "name"
            if ( current_property in current_container[ item ] ):
                current_property_value = current_container[ item ][ current_property ]
                print( "----> " + current_property + ": " + current_property_value )
            #-- END current_property --#
            current_property = "person"
            if ( current_property in current_container[ item ] ):
                current_property_value = current_container[ item ][ current_property ]
                print( "----> " + current_property + ": " + current_property_value )
            #-- END current_property --#
            
        #-- END loop over items --#
        
    #-- END function print_calais_json --#


    def set_http_helper( self, instance_IN ):
        
        # return reference
        instance_OUT = ""
        
        # set instance
        self.http_helper = instance_IN
        
        # return instance
        instance_OUT = self.get_http_helper()
        
        return instance_OUT
        
    #-- END method set_http_helper() --#
    

#-- END class OpenCalaisArticleCoder --#