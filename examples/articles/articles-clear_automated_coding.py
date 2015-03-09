# imports
from sourcenet.models import Article_Data
from django.contrib.auth.models import User

# declare variables
automated_user = None
article_data_qs = None
article_data_count = -1
article_data = None
article_author_count = -1
article_source_count = -1
related_article = None
article_tags = []
article_author = None
article_source = None
article_id_list = []
article_data_id_list = []
article_author_id_list = []
article_source_id_list = []

# get User with name "automated"
automated_user = User.objects.filter( username = "automated" ).get()

# find all Article_Data for automated user.
article_data_qs = Article_Data.objects.filter( coder = automated_user )

# how many?
article_data_count = article_data_qs.count()

print( "Found " + str( article_data_count ) + " Article_Data for automated coder." )

# tell me more...
for article_data in article_data_qs:

    # add id to data list
    article_data_id_list.append( str( article_data.id ) )

    # how many Article_Author?
    article_author_count = article_data.article_author_set.count()
    
    # how many Article_Source
    article_source_count = article_data.article_source_set.count()

    print( "- Article_Data " + str( article_data.id ) + " - authors: " + str( article_author_count ) + "; sources: " + str( article_source_count ) + "; details: " + str( article_data ) )
    
    # loop over article_authors
    for article_author in article_data.article_author_set.all():
    
        # add id to data list
        article_author_id_list.append( str( article_author.id ) )

        print( "    - ==> Article_Author: " + str( article_author ) )
        
    #-- END loop over article_author_set --#
    
    # loop over article_sources
    for article_source in article_data.article_source_set.all():
    
        # add id to data list
        article_source_id_list.append( str( article_source.id ) )

        print( "    - ==> Article_Source: " + str( article_source ) )
        
    #-- END loop over article_author_set --#
    
    # get article...
    related_article = article_data.article
    
    # add ID to list
    article_id_list.append( str( related_article.id ) )
    
    # ...and get tags
    article_tags = related_article.tags.all()
    
    if ( len( article_tags ) == 0 ):
    
        print( "    - NO TAGS HOLY SMOKES NO WAY!!!" )
    
    else:
    
        print( "    - related article tags: " + str( article_tags ) )
    
    #-- END check if there are tags --#
    
    # delete Article_Data and children
    article_data.delete()
    
#-- END loop over article data. --#

print( "\n\nID lists:\n" )
print( "- Article ( " + str( len( article_id_list ) ) + " ): " + str( ", ".join( article_id_list ) ) )
print( "- Article_Data ( " + str( len( article_data_id_list ) ) + " ): " + str( ", ".join( article_data_id_list ) ) )
print( "- Article_Author ( " + str( len( article_author_id_list ) ) + " ): " + str( ", ".join( article_author_id_list ) ) )
print( "- Article_Source ( " + str( len( article_source_id_list ) ) + " ): " + str( ", ".join( article_source_id_list ) ) )