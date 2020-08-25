import xbmc, xbmcgui, xbmcaddon, xbmcplugin, json
from CVideoDatabase import CVideoDatabase
from strings import *

t=None
assetID = xbmc.getInfoLabel('ListItem.DBID')
assetTYPE = xbmc.getInfoLabel('ListItem.DBtype')
assetTITLE = xbmc.getInfoLabel('ListItem.label')

class CDialogMagicSearch(xbmcgui.WindowXMLDialog):
    #subclassing new to integrate the dialog definition into the dialog control class
    def __new__(cls):
        return super(CDialogMagicSearch, cls).__new__(cls, "MagicSearchResults.xml", ADDON.getAddonInfo('path')) 

    #init window
    def __init__(self, *args, **kwargs):
        self.getFileInfos()
        super(CDialogMagicSearch, self).__init__()
        
    def doModal(self,id=0, type=''):
        if id!=0:
            self.entry = "modal"
            if type == PROPERTY_MOVIE:
                result = self.vdb.getMovieById(id)
            elif type == PROPERTY_MUSICVIDEO:
                result = self.vdb.getMusicvideosById(id)
            elif type == PROPERTY_TVSHOW:
                result = self.vdb.getTVShowsById(id)
            self.name = result[0][2]
            self.id     = assetID
            self.type   = assetTITLE
        xbmcgui.WindowXMLDialog.doModal(self)

    #init eventhandler
    def onInit( self ):
        pl=self.getControl(SEARCHLABEL)
        
        if secondParameter !=" ":
            pl.setLabel(searchParameter + " in " + secondParameter)
        else:
            pl.setLabel(searchParameter)
        
        self.buildList("")
        self.setFocusId(MOVIELIST)

    def getFileInfos(self):
        self.player = xbmc.Player()
        self.vdb = CVideoDatabase()
        self.filepath = decode(xbmc.getInfoLabel('ListItem.FileNameAndPath'))
        self.path = xbmc.getInfoLabel('ListItem.Path')
        self.name = xbmc.getInfoLabel('ListItem.Label')
        self.dbid = xbmc.getInfoLabel('ListItem.DBID')
        self.entry = "selection"  
        
        if self.getData(self.vdb):
            debug(u"CDialogMagicSearch Load for '{0}' with path '{1}' by {2}, type: {3}, id: {4}".format(self.name, self.path, self.entry, self.type, self.id))
            return True
        else:
            debug(u"",self.name)
            debug(u"",self.path)
            debug(u"",self.entry)
            debug(u"",self.type)
            debug(u"",self.id)
            debug("CDialogMagicSearch No valid item selected")
            return False
    
    #create the search results listview - list of movies, shows, episodes
    def buildList(self, refine):
        movies = self.vdb.GetMovies(searchParameter)
        movieList = [list(x) for x in movies]
        debug("refine", refine)        
        for movie in movieList:
            if movie[4] == "" and searchField == 'actor':
                movie[4] = "[I]Actor[/I]"                   #subbing generic 'Actor' label when none is provided and doing very bad practice of embedding formatting
        for movie in movieList:
            if movie[1] == "":
                mediaID = movie[0]
                mediaPath = self.vdb.GetMediaPath(mediaID)
                debug('mediaPath', mediaPath)
                mediaPath = "".join(str(mediaPath))
                mediaPath = mediaPath.replace("[(u'","")
                mediaPath = mediaPath.replace("',)]","")
                mediaPath = mediaPath.replace('[(u"','')
                mediaPath = mediaPath.replace('",)]','')
                mediaPath = mediaPath.replace("\\\\","\\")
                movie[1] = mediaPath
                debug('movie[1]', movie[1])
        movieList = self.removeDuplicate(movieList)
        movieList = self.removeDupEpisodes(movieList)
        if refine != "":
            movieCompare = self.vdb.GetMovies(refine)
            movieCompareList = [list(x) for x in movieCompare]
            movieList = self. secondActorFilter(movieList,movieCompare)
        #actorThumb = self.getActorThumb()
        control=self.getControl(MOVIELIST)
        for movie in movieList:
          control.addItem(self.createListItem(
                                               movie[0],        # movie id
                                               movie[1],        # path
                                               movie[2],        # date
                                               movie[3],        # media
                                               movie[4]         # role
                                             )
                            )
        #creating the fake list item for the Refine by Actor Intersection button
        control.addItem(self.createListItem(
                                               0000,           # movie id
                                               "",             # path
                                               "",             # date
                                               "Refine",       # media
                                               refine          # role
                                             )
                            )
        
    def removeDuplicate(self,movieList):       #merges results where a person is an actor and/or a writer and/or an actor
        delList = []
        for movie in movieList[:]:
            movieCompareIndex = 0
            for movieCompare in movieList[:]:
             if movieCompare[1] == movie[1] and movie[4] != movieCompare[4] and movieCompare not in delList and movie not in delList:
                movie[4] = movie[4] + " + " + movieCompare[4]
                delList.append(movieList[movieCompareIndex])
                del movieList[movieCompareIndex]
                movieCompareIndex = movieCompareIndex - 1
             movieCompareIndex = movieCompareIndex + 1
        return movieList
 
    def removeDupEpisodes(self,movieList):       #supresses episode listings when the actor is in the TVShow (doesn't affect writers and directors and we don't want it to)
        debug('movieList',movieList)
        for movie in movieList[:]:
            movieCompareIndex = 0
            if movie[3] == 'TVShow':
               movieCompareIndex = 0
               pathLen = len(movie[1])
               for movieCompare in movieList[:]:  #  and movieCompare not in delList and movie not in delList - delete list not needed due to the way the entries are ordered
                   if (movieCompare[3] == 'Episode') and ("[I]Writer[/I]" not in movieCompare[4]) and ("[I]Director[/I]" not in movieCompare[4]):
                       if movieCompare[1][:pathLen] == movie[1]:
                           #delList.append(movieList[movieCompareIndex])
                           del movieList[movieCompareIndex]
                           movieCompareIndex = movieCompareIndex - 1
                   movieCompareIndex = movieCompareIndex + 1
        return movieList
        
    def secondActorFilter(self,movieList,movieCompareList):    #filters the search results when a second actor is provided via the refine by intersection button
        matchList = []
        
        for movie in movieList[:]:
            movieCompareIndex = 0
            for movieCompare in movieCompareList:
                if movieCompare[0] == movie[0] and movie[3] == movieCompare[3]:
                    matchList.append(movieCompareList[movieCompareIndex])
                    movieCompareIndex = movieCompareIndex - 1
                movieCompareIndex = movieCompareIndex + 1
        return matchList
        
    def getActorThumb(self):     #not used but the idea was to display actor thumbnail in search results (it worked, just didn't like the UI)
        actorThumb = self.vdb.GetActor()
        actorThumb = "".join(str(actorThumb))
        actorThumb = actorThumb.replace("[(u'<thumb>","")
        actorThumb = actorThumb.replace("</thumb>',)]","")
        return actorThumb
    
    #create a listitem for the listview and set properties
    def createListItem(self, movieid, path, date, media, role):
        if media != "Refine":
            moviedetails = self.getMovieDetails(movieid, media)
            li = xbmcgui.ListItem(moviedetails.get('title')) 
            li.setProperty(PROPERTY_MOVIEID, str(movieid))
            li.setProperty(YEAR, date)
            li.setProperty(POSTER, str(moviedetails.get('thumbnail')))
            li.setProperty(ROLE, role)
            if media == "Movie":
               # set the path to the file, kodi will use it to fetch additional info from the db
               
               li.setProperty(MEDIA, media)
               li.setPath(moviedetails.get('file'))
               li.setInfo('video', { 'mediatype': 'movie' }) 
            elif media == "TVShow":
               li.setProperty(MEDIA, media)
               #can't seem to set path to a TVShow  so setting path to the seasons folder instead
               tvpath = path = 'videodb://tvshows/titles/' + str(movieid) + '/'
               li.setProperty(PATH, tvpath)
               
               #li.setPath(moviedetails.get('file'))
               li.setInfo('video', { 'mediatype': 'tvshow' }) 
            elif media == "Episode":
               li.setProperty(MEDIA, str(moviedetails.get('season')) + 'x' + str(moviedetails.get('episode')))
               li.setProperty(SHOWTITLE, moviedetails.get('showtitle'))
               li.setPath(moviedetails.get('file'))
               li.setInfo('video', { 'mediatype': 'episode' }) 
            
            plot = moviedetails.get('plot')
            #plot = plot.encode(encoding="ascii",errors="replace")
            li.setProperty(PLOTSUM, plot)
            
            directorList = moviedetails.get('director')
            if directorList != None:
                director = '/'.join(directorList)
                li.setProperty(DIRECTOR, director)
            
            #li.setProperty(ACTORTHUMB, actorThumb)
            # add a video info tag, so kodi knows it's a video item
            #li.setInfo('video', {})
        else:
            li = xbmcgui.ListItem('Refine search')
            li.setLabel('Intersection search')
            li.setProperty(MEDIA, media)
            li.setProperty(ROLE, role)
        return li
 
    #getting the rest of what we need from JSON
    def getMovieDetails(self, movieid, media):
        if media == "Movie":
            paramsRaw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %d, "properties": ["title", "studio", "mpaa", "plot", "genre", "year", "runtime", "rating", "tagline", "director", "writer", "fanart", "thumbnail", "file"]}, "id": 1}' % ( movieid, ) ) 
            paramsRaw = paramsRaw.decode(encoding="utf-8",errors="ignore")
            params = json.loads(paramsRaw)
            result = params['result']
            moviedetails = result['moviedetails']
        elif media == "Episode":   
            debug('movieid',movieid)
            paramsRaw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"episodeid": %d, "properties": ["title", "showtitle", "season", "episode",  "plot", "firstaired", "runtime", "rating", "director", "writer", "fanart", "thumbnail", "file"]}, "id": 1}' % ( movieid, ) )
            paramsRaw = paramsRaw.decode(encoding="utf-8",errors="ignore")
            params = json.loads(paramsRaw)
            result = params['result']
            moviedetails = result['episodedetails']
        elif media == "TVShow":   
            paramsRaw = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShowDetails", "params": {"tvshowid": %d, "properties": ["title", "plot", "premiered", "rating", "fanart", "thumbnail", "file"]}, "id": 1}' % ( movieid, ) )
            paramsRaw = paramsRaw.decode(encoding="utf-8",errors="ignore")
            params = json.loads(paramsRaw)
            result = params['result']
            moviedetails = result['tvshowdetails']
        return moviedetails
   
    #not using this anymore but it found posters from the movie file path
    def pathSplitter(self, path):
        #if path.count(".") == 1:
        #    return path.split("//")[0]
        #else:
        #    return "//".join(path.split("//", 2)[:2])
        splitPath =path.rsplit('\\', 2)
        imgURL = splitPath[0] + "\\" + splitPath[1] + "\\" + splitPath[1] + "-poster.jpg"
        return imgURL
   
    #tagoverview legacy that I'm not comfortable removing/modifying
    def getData(self, vdb):
        fileid = vdb.GetFileId(self.filepath)
        data = vdb.GetTypeAndId(fileid, self.path)
        if data != 0:
            self.id     = data[1]
            self.type   = data[0]
            self.name   = data[2]
            return True
        else:
            self.id     = 0
            self.type   = ''
            self.name   = ""
            return False

    #control windowactions
    def onAction(self, action):
        if not (action.getId() == ACTION_SELECT_ITEM) or not (action.getId() == ACTION_SELECT_ITEM2):
            self.onAction1(action)  #cancels 
        if (action == ACTION_SELECT_ITEM) or (action == ACTION_SELECT_ITEM2):
            controlId = self.getFocusId()  
            if controlId == MOVIELIST:
                li = self.getControl(controlId).getSelectedItem()
                actionChoice = li.getProperty('media')
                if actionChoice == "Refine":
                    self.GetSecondActor(self.getControl(controlId),li)
                elif actionChoice == "TVShow":
                    tvpath = li.getProperty('path')
                    self._browse_video(tvpath)
                else:
                    self.displayVideoInfo(li)
    
    #show keyboard, get intersect criteria, and rebuild the listview
    def GetSecondActor(self,cntrl,li):
        keyboard = xbmc.Keyboard(li.getProperty(ROLE), 'Input second actor')
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            secondActor = (keyboard.getText().strip())
            debug ('secondActor', secondActor)
            li.setLabel2(': ' + secondActor)
            cntrl.reset()
            self.buildList(secondActor)                 
    
    #opens the video dialog after clicking on a search result...
    def displayVideoInfo(self,li):
        self.close()
        #xbmc.executebuiltin('ActivateWindow(12003)')
        dialog = xbmcgui.Dialog()
        dialog.info(li)
        xbmc.sleep(250)
        #debug('Trying to refocus actor list')
        #xbmc.executebuiltin('Control.SetFocus(5)')
        #xbmc.executebuiltin('SendClick(,5)')
        #xbmc.executebuiltin('Control.SetFocus(5)')
        xbmc.executebuiltin('Control.SetFocus(500,0,absolute)')
        
    #...except for tvshows, where we open the season view instead
    def _browse_video( self, path ):
        self.close()
        xbmc.executebuiltin('Dialog.Close(12003,true)')
        xbmc.executebuiltin('ReplaceWindow(Videos,' + path + ',return)')
        
    def onAction1(self, action):
        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_PARENT_DIR) or (action == ACTION_PREVIOUS_MENU2):
            self.state = -1 #success
            self.close() #exit
            