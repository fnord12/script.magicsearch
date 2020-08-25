import sys
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
from pluginDatabase import CVideoDatabase

def debug(msg, *args):
    try:
        txt=u''
        msg=unicode(msg)
        for arg in args:
            if type(arg) == int:
                arg = unicode(arg)
            if type(arg) == list:
                arg = unicode(arg)
            txt = txt + u"/" + arg
        if txt == u'':
            xbmc.log(u"ACT: {0}".format(msg).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
        else:
            xbmc.log(u"ACT: {0}#{1}#".format(msg, txt).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
    except:
        print "Error in Debugoutput"
        print msg
        print args

_handle = int(sys.argv[1])

def get_actors(category,ID,Media,SortBy):
    vdb = CVideoDatabase()
    
    if SortBy == "Role":
        ActorTuple = vdb.GetActorsDBOrderByRole(ID, Media)
    elif SortBy == "Name":
        ActorTuple = vdb.GetActorsDBOrderByName(ID, Media)
    else:
        ActorTuple = vdb.GetActorsDB(ID, Media)
    
    ActorList = [list(x) for x in ActorTuple]
    return ActorList

def list_videos(category, ID, Media, SortBy):
    xbmcplugin.setPluginCategory(_handle, category)
    xbmcplugin.setContent(_handle, 'actor')
    actors = get_actors(category,ID, Media, SortBy)
    for actor in actors:
        if actor[2] != "" and actor[2] != None:
            if not actor[4] == "1":        
                listitem = xbmcgui.ListItem(label=actor[0] + " as " + actor[2])
            else:
                listitem = xbmcgui.ListItem(label=actor[0] + " as " + actor[2] + "*")
        else:
            listitem = xbmcgui.ListItem(label=actor[0])
        
        #mapping the fields we need for magicsearch/edit to the fields that Kodi allows for plugins:
        #genre = role
        #country = cast_order
        #tvshowtitle = Media type (movie, episode, tvshow)
        #ID = Media DBID
        
        listitem.setInfo('video', {'genre': actor[0]})
        listitem.setInfo('video', {'country': str(actor[3])})  
        listitem.setInfo('video', {'path': 'xbmc.executebuiltin("Notification(\"Actor Plugin\", \"%s\")" % assetMsg)'})
        listitem.setInfo('video', {'tvshowtitle': Media})
        listitem.setInfo('video', {'top250': ID})
        
        thumb = getActorThumb(actor[1])
        listitem.setArt({'thumb': thumb})
        url = ''
        is_folder = False
        
        #setting context menu items doesn't work?
        listitem.addContextMenuItems([('Test', "Notification('Testing 125','Hello world')"),('Another Test', "Notification('Testing 126','Goodbye world')")])
        xbmcplugin.addDirectoryItem(_handle, url, listitem, is_folder)
    
    
    xbmcplugin.endOfDirectory(_handle,cacheToDisc=False)


def getActorThumb(actorThumb):
    if actorThumb is not None:
        actorThumb = actorThumb.replace("<thumb>","")
        actorThumb = actorThumb.replace("</thumb>","")
    if actorThumb == "" or actorThumb is None:
        actorThumb = "defaultactor.png"
    return actorThumb

def play_video(path):
   debug('This never runs')

def router(paramstring):
    
    debug('paramstring= ',paramstring)
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            debug('Media',params['action'])
            list_videos(params['category'],params['ID'],params['Media'],params['SortBy'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            debug('Here We are',params['action'])
            assetMsg = "Ok I'll Do It."
            xbmc.executebuiltin("Notification(\"Actor Plugin\", \"%s\")" % assetMsg)
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        raise ValueError('Invalid paramstring: {0}!'.format(paramstring))


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
    