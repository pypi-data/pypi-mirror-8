from plone.indexer.decorator import indexer
from collective.media.interfaces import ICanContainMedia
from Products.CMFCore.interfaces import IFolderish
from plone.app.collection.interfaces import ICollection

@indexer(IFolderish)
def folderish_hasMedia(object, **kw):
    return ICanContainMedia(object).hasMedia()
    
@indexer(IFolderish)
def folderish_getLeadMedia(object, **kw):
    #print "re indexer"
    lead = ICanContainMedia(object).getLeadMedia()
    if lead is not None:
        return lead.UID
    else:
        return None

@indexer(IFolderish)
def folderish_getLeadMediaTag(object, **kw):
    lead = ICanContainMedia(object).getLeadMedia()
    if lead is not None:
        if hasattr(lead, 'getURL'):
            return lead.getURL()
        else:
            return lead.absolute_url()
    else:
        return None

@indexer(IFolderish)
def folderish_getLeadImageTag(object, **kw):
    #print "re indexer get lead image tag"
    lead = ICanContainMedia(object).getLeadMedia()
    print lead.getURL()
    if lead is not None:
        if hasattr(lead, 'getURL'):
            return lead.getURL()
        else:
            return lead.absolute_url()
    else:
        return None
    
@indexer(ICollection)
def collection_hasMedia(object, **kw):
    return ICanContainMedia(object).hasMedia()
    
@indexer(ICollection)
def collection_getLeadMedia(object, **kw):
    #print "re indexer"
    lead = ICanContainMedia(object).getLeadMedia()
    if lead is not None:
        return lead.UID
    else:
        return None
    