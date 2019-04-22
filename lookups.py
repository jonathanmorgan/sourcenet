"""
Installation of "django-ajax-selects":
- Use pip to install "django-ajax-selects" and dependencies.
- In settings.py:

    - add "ajax_select" to INSTALLED_APPS.
    - Add:

            # magically include jqueryUI/js/css
            AJAX_SELECT_BOOTSTRAP = True
            AJAX_SELECT_INLINES = 'inline'

- Touch your project's wsgi.py file to load the "ajax_select" application.
- Run "python manage.py collectstatic".

To add a new ajax select:
- Include the import for the model class you will be selecting from at the top of this file (put it in alphabetical order).
- In this file, make a new class that extends LookupParent for the model you want to lookup using AJAX-selects (It is OK to just copy one of the other ones here).  Place it in alphabetical order in the file.
- Modify the get_query() and get_objects() methods to reference the correct model, fields in that model.
- If django 1.6 or earlier, in settings.py, add a line for your new channel to the AJAX_LOOKUP_CHANNELS property, like this, for person:
    'person' : ('context_text.lookups', 'PersonLookup'),
- In admin.py, either add or edit a form attribute to include your channel, and to tell the admin which field to map to which AJAX lookup.  So, for example, in Article, there is the following line:

        form = make_ajax_form( Article_Subject, dict( person = 'person', ) )

    - This line says, for Article_Subject, when entering 'person' field, lookup using the 'person' AJAX lookup channel.
    - The field names are the names from the model class definition, and can be any type of relation.  Channel names are the @register decorator contents in this file, or if django <= 1.6, the keys in AJAX_LOOKUP_CHANNELS in your settings.py file.
    - So, If you were to add a lookup for organization, then you'd have:

            form = make_ajax_form( Article_Subject, dict( person = 'person', subject_organization = 'organization', ) )

- To use in a plain django Form, use `ajax_select.make_ajax_field` inside a ModelForm child, assigned to a variable named for the field you want to look up:

    - person  = make_ajax_field( Article_Subject, 'person', 'coding_person', help_text = None )
"""

# python imports
import logging

# django imports
from django.db.models import Q

# context_text imports
from context_text.models import Article
from context_text.models import Article_Data
from context_text.models import Newspaper
from context_text.models import Organization
from context_text.models import Person

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper

# python_utilities - django_ajax_selects_lookup_helper
from python_utilities.django_utils.django_ajax_selects_lookup_helper import LookupParent

# ajax_select imports
from ajax_select import register, LookupChannel


#===============================================================================#
# Debug logging
#===============================================================================#


DEBUG = False

def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "" ):
    
    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''
    
    # declare variables
    my_message = ""
    my_logger = None
    my_logger_name = ""

    # got a message?
    if ( message_IN ):
    
        # only print if debug is on.
        if ( DEBUG == True ):
        
            my_message = message_IN
        
            # got a method?
            if ( method_IN ):
            
                # We do - append to front of message.
                my_message = "In " + method_IN + ": " + my_message
                
            #-- END check to see if method passed in --#
            
            # indent?
            if ( indent_with_IN ):
                
                my_message = indent_with_IN + my_message
                
            #-- END check to see if we indent. --#
        
            # debug is on.  Start logging rather than using print().
            #print( my_message )
            
            # got a logger name?
            my_logger_name = "context_text.lookups"
            if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
            
                # use logger name passed in.
                my_logger_name = logger_name_IN
                
            #-- END check to see if logger name --#
                
            # get logger
            my_logger = LoggingHelper.get_a_logger( my_logger_name )
            
            # log debug.
            my_logger.debug( my_message )
        
        #-- END check to see if debug is on --#
    
    #-- END check to see if message. --#

#-- END method output_debug() --#


#===============================================================================#
# Individual child Lookup classes
#===============================================================================#


@register( "article" )
class ArticleLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( ArticleLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Article
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an article?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( unique_identifier__icontains = q ) | Q( headline__icontains = q ) )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'unique_identifier', 'headline' )

    #-- END method get_objects --#

#-- END class ArticleLookup --#


@register( "article_data" )
class Article_DataLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( Article_DataLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Article_Data
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an article?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( coder_type__icontains = q ) | Q( status__icontains = q ) )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'article', 'coder' )

    #-- END method get_objects --#

#-- END class Article_DataLookup --#


@register( "newspaper" )
class NewspaperLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( NewspaperLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Newspaper
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an contributor?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( name__icontains = q ) | Q( description__icontains = q ) | Q( newsbank_code__icontains = q ) )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'name', 'description' )

    #-- END method get_objects --#

#-- END class NewspaperLookup --#


@register( "organization" )
class OrganizationLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( OrganizationLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Organization
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed
        """

        # return reference
        query_set_OUT = None

        # is the q a number and is it the ID of an contributor?
        query_set_OUT = self.get_instance_query( q, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Return search of text in contributor.
            query_set_OUT = self.my_class.objects.filter( Q( name__icontains = q ) | Q( description__icontains = q ) )

        #-- END retrieval of query set when no ID match. --#

        return query_set_OUT

    #-- END method get_query --#


    def get_objects(self,ids):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter(pk__in=ids).order_by( 'name', 'description' )

    #-- END method get_objects --#

#-- END class OrganizationLookup --#


@register( "person" )
class PersonLookup( LookupParent ):

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( PersonLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Person
        
    #-- END method __init__() --#

    def get_query( self, q, request ):

        """
        return a query set.  you also have access to request.user if needed.
        """

        # return reference
        query_set_OUT = None

        # declare variables
        me = "get_query"
        my_logger_name = ""
        person_name = ""
        match_count = -1
        name_part_list = None
        human_name = None
        
        # init logging info
        my_logger_name = "context_text.lookups.PersonLookup"
        
        # store q in a real variable
        person_name = q
        
        # output string passed in
        output_debug( "q = " + str( q ), method_IN = me, logger_name_IN = my_logger_name )

        # is the q a number and is it the ID of an contributor?
        query_set_OUT = self.get_instance_query( person_name, request, self.my_class )

        # got anything back?
        if ( query_set_OUT is None ):

            # No exact match for q as ID.  Try Person.find_person_from_name()
            query_set_OUT = Person.find_person_from_name( person_name, do_strict_match_IN = False, do_partial_match_IN = True )
            
        #-- END retrieval of QuerySet when no ID match. --#

        return query_set_OUT
    
    #-- END method get_query --#


    def get_objects( self, ids ):

        """
        given a list of ids, return the objects ordered as you would like them
            on the admin page.  This is for displaying the currently selected
            items (in the case of a ManyToMany field)
        """
        return self.my_class.objects.filter( pk__in = ids ).order_by( 'last_name', 'first_name', 'middle_name' )

    #-- END method get_objects --#

#-- END class PersonLookup --#


@register( "coding_person" )
class ArticleCodingPersonLookup( PersonLookup ):

    '''
    just extending PersonLookup for now.
    '''

    def __init__( self, *args, **kwargs ):
        
        # call parent's __init__()
        super( ArticleCodingPersonLookup, self ).__init__()
        
        # initialize variables
        self.my_class = Person
        
    #-- END method __init__() --#

#-- END class ArticleCodingPersonLookup --#