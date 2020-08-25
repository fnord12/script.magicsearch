import xbmc
import xbmcaddon
import sys
import xbmcgui
import xbmcplugin
from strings import *
from EditorDatabase import CVideoDatabase

ActorData=""
MovieData=""

vdb = CVideoDatabase()

def refresh():
    xbmc.executebuiltin('ReloadSkin()')
    xbmc.executebuiltin('ActivateWindow(12003)')
    xbmc.executebuiltin('SendClick(12003,5)')    
    
def checkActor(name):
    vdb = CVideoDatabase()
    ActorExistsTuple = vdb.checkActorExists(name)
    ActorExistsList = [list(x) for x in ActorExistsTuple]
    ActorExists = ActorExistsList[0]
    return ActorExists
    
def checkActorInMedia(name):
    ActorID = getActorID(name)
    debug('ActorID',ActorID)
    vdb = CVideoDatabase()
    ActorInMediaTuple = vdb.checkActorInMedia(ActorID,launchID,launchMedia)
    debug('ActorInMediaTuple', ActorInMediaTuple)
    ActorInMediaList = [list(x) for x in ActorInMediaTuple]
    debug('ActorInMediaList', ActorInMediaList)
    ActorInMedia = ActorInMediaList[0]
    debug('ActorInMedia', ActorInMedia)
    return ActorInMedia
    
def getActorID(name):
    vdb = CVideoDatabase()
    ActorIDTuple = vdb.getActorID(name)
    debug('ActorIDTuple',ActorIDTuple)
    ActorIDList = [list(x) for x in ActorIDTuple]
    ActorID = ActorIDList[0][0]
    return ActorID
    
def getMaxCastOrder():
    vdb = CVideoDatabase()
    MaxCastOrderTuple = vdb.getMaxCastOrderDB(launchID,launchMedia)
    debug('MaxCastOrderTuple',MaxCastOrderTuple)
    MaxCastOrderList = [list(x) for x in MaxCastOrderTuple]
    MaxCastOrder = MaxCastOrderList[0][0]
    if MaxCastOrder is None:
        MaxCastOrder = 0
    return MaxCastOrder
    
def checkActorEpisode():
    vdb = CVideoDatabase()
    isInShowTuple = vdb.checkActorEpisodeDB(actorName, launchID)
    isInShowList = [list(x) for x in isInShowTuple]
    isInShow = isInShowList[0]
    debug ('isInShow', isInShow)
    return isInShow

def getActorDetails():
    global ActorData
    ActorDataTuple = getActorData()
    ActorDataList = [list(x) for x in ActorDataTuple]
    ActorData = ActorDataList[0]
    # 0=ID, 1=role, 2=thumb, 3=order

def getActorData():
    global launchMedia, launchID
    if launchMedia == 'episode':
        isInShow = checkActorEpisode()
        if isInShow[0] == 1:    
            dialog = xbmcgui.Dialog()
            confirm = dialog.yesno('TVShow, not episode', 'Actor really exists for TV show, not episode.  Update actor\'s show data instead?')
            if confirm:
                launchMedia = 'tvshow'
                launchID = isInShow[1]
            else:
                exit()
    vdb = CVideoDatabase()
    ActorData = vdb.GetActorFrmDB(actorName, launchID, launchMedia)
    return ActorData
    
    
def getMovieDetails():
    global MovieData
    MovieDataTuple = getMovieData()
    MovieDataList = [list(x) for x in MovieDataTuple]
    MovieData = MovieDataList[0]
    # 0=Alt Title, 1=Studio, 2=Year, 3=Genre
    
def getMovieData():
    vdb = CVideoDatabase()
    if launchMedia == 'movie':
        MovieData = vdb.GetMovieFrmDB(launchID)
    elif launchMedia == 'tvshow':
        MovieData = vdb.GetTVShowFrmDB(launchID)
    elif launchMedia == 'episode':
        MovieData =  vdb.GetEpisodeFrmDB(launchID)
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')
        return
    return MovieData

def cleanThumb(dirtyThumb):
        dirtyThumb = dirtyThumb.replace("<thumb>","")
        cleanThumb = dirtyThumb.replace("</thumb>","")
        return cleanThumb

def dirtyThumb(cleanThumb):
    cleanThumb = "<thumb>" + cleanThumb + "</thumb>"
    return cleanThumb

def getChoice():
    removeString = "Remove from this " + launchMedia
    editChoices = ["Edit Name", "Edit Role", "Edit Order", "Edit Picture", removeString, "Completely Remove Actor", "Swap Actor and Role"]
    if launchMedia == "episode":
        editChoices.append("Move From Episode To Show")

    editChoice = xbmcgui.Dialog().select(actorName,editChoices)
        
    if editChoice < 0:
        sys.exit()
    if editChoice == 0:   
        editName()
    if editChoice == 1:   
        editRole()
    if editChoice == 2:   
        editOrder()
    if editChoice == 3:   
        editPicture()   
    if editChoice == 4:   
        delinkActor()
    if editChoice == 5:   
        delinkActorComplete()
    if editChoice == 6:   
        swapActorAndRole()    
    if editChoice == 7:   
        moveToShow()
        
def addActorParser():
    keyboard = xbmc.Keyboard("", "Add Actor")
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        result = (keyboard.getText().strip())
        if not result[0] == "*":
            addActor(result)
        else:
            result = result.replace("*", "")
            result = result.split(', ')
            for actor in result:
                addActor(actor)
    refresh()
    
def addActor(result):
    resultRole = ""
    debug('result', result)
    result = result.replace(" (as ", ">")
    result = result.replace(" 	... 	",">")
    result = result.replace(" as ", ">")
    result = result.replace(" - ", ">")
    
    if ">" in result:
        sep = ">"
        resultActor = result.split(sep, 2)[0]
        resultRole = result.split(sep, 2)[1]
        result = resultActor
    
    ActorExists = checkActor(result)
    debug ('ActorExists[0]', launchID, )
    
    cast_order = getMaxCastOrder()
    cast_order = cast_order + 1 
    
    if ActorExists[0] == 1:    
        ActorInMedia = checkActorInMedia(result)
        debug('ActorInMedia',ActorInMedia)
        if ActorInMedia[0] == 0:  #actor isn't already listed for this video
            vdb.addExistingActor(result, resultRole, launchID, launchMedia, cast_order)
        else:
            assetMsg = "Actor already listed: '%s'" % result
            xbmc.executebuiltin("Notification(\"Editor Extraordinaire\", \"%s\")" % assetMsg)
            if not resultRole == "":
                ActorID = getActorID(result)
                vdb.updateActorRole(resultRole, ActorID, launchID, launchMedia)
    else:   #new Actor name isn't aleady in use
        vdb.addNewActor(result)  #first add to actor table
        vdb.addExistingActor(result, resultRole, launchID, launchMedia, cast_order)  #then add to actor link for current video
    
def editName():
    keyboard = xbmc.Keyboard(actorName, "Edit Name")
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        result = (keyboard.getText().strip()) 
        debug('result', result)
        ActorExists = checkActor(result)
        debug ('ActorExists[0]', ActorExists[0])
        if ActorExists[0] == 0:    #new Actor name isn't aleady in use
            vdb.updateActorName(result, ActorData[0])
            refresh()
        else:
            mergeActors(ActorExists[1])
 
def mergeActors(MergeTo):
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno('This name already exists', 'Merge this entry into the existing one?')
    if confirm:
        vdb.mergeActorsDB(ActorData[0], MergeTo)
        refresh()   

def editRole():
    keyboard = xbmc.Keyboard(ActorData[1], "Edit Role")
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        result = (keyboard.getText().strip())
        vdb.updateActorRole(result, ActorData[0], launchID, launchMedia)
        refresh()            

def editOrder():
    keyboard = xbmc.Keyboard(str(ActorData[3]), "Edit Order")
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        result = (keyboard.getText().strip()) 
        vdb.updateActorOrder(result, ActorData[0], launchID, launchMedia)
        refresh()    

def editPicture():
    keyboard = xbmc.Keyboard("", "Paste new image link (e.g. from TMDb)")
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        result = (keyboard.getText().strip())
        result = dirtyThumb(result)        
        vdb.updateActorThumb(result, ActorData[0])
        refresh()
        
def delinkActor():
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno('Disassociate actor from this listing?', 'Are you sure?')
    if confirm:
        vdb.removeActorLink(ActorData[0], launchID, launchMedia)
        refresh()

def delinkActorComplete():
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno('Completely remove actor from all listings?', 'Are you COMPLETELY sure?')
    if confirm:
        vdb.removeActorLinkComplete(ActorData[0])
        refresh()   

def swapActorAndRole():
    newRole = actorName
    newName = ActorData[1]
    oldRole = ActorData[1]
    
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno('Swap actor and Role', 'Actor name will be **' + newName + '** and Role will be **' + newRole + '**. Are you COMPLETELY sure?')
    if confirm:
        ActorExists = checkActor(newName)
        debug ('ActorExists[0]', ActorExists[0])
        if ActorExists[0] == 0:    #new Actor name isn't aleady in use
            vdb.updateActorName(newName, ActorData[0])
            vdb.cleanActorRole(oldRole, newRole, ActorData[0], launchMedia)
        else:
            ActorInMedia = checkActorInMedia(newName)
            debug('ActorInMedia',ActorInMedia)
            if ActorInMedia[0] == 0:  #actor isn't already listed for this video
                vdb.mergeActorsDB(ActorData[0], ActorExists[1])
                vdb.cleanActorRole(oldRole, newRole, ActorExists[1], launchMedia)
            else:
                assetMsg = "Actor already exists for show: '%s'" % newName
                xbmc.executebuiltin("Notification(\"Editor Extraordinaire\", \"%s\")" % assetMsg)
        refresh()         
                
def moveToShow():
    dialog = xbmcgui.Dialog()
    confirm = dialog.yesno('List this actor for the entire show?', 'Are you sure?')
    if confirm:
        cast_order = getMaxCastOrder()
        cast_order = cast_order + 1 
        vdb. moveToShowDB(ActorData[0], launchID, ActorData[1],cast_order)
        refresh()   

def getDetailsChoice():
    
    editChoices = ["Alt Title", "Studio", "Year", "Genre", "Director", "Writer", "Tagline", "Plot", "MPAA Rating", "[B][COLOR orange]Add New Actor[/COLOR][/B]"]
   
    editChoice = xbmcgui.Dialog().select("Select field to edit",editChoices)
        
    if editChoice < 0:
        sys.exit()
    if editChoice == 0:   
        editAltTitle()
    if editChoice == 1:   
        editStudio()
    if editChoice == 2:   
        editYear()
    if editChoice == 3:   
        editGenre()
    if editChoice == 4:   
        editDirector()
    if editChoice == 5:   
        editWriter() 
    if editChoice == 6:   
        editTagline()    
    if editChoice == 7:   
        editPlot()
    if editChoice == 8:   
        editMPAARating()    
    if editChoice == 9:   
        addActorParser() 
        
def editAltTitle():
    if launchMedia == "movie":
        editfield = "c16"
        keyboard = xbmc.Keyboard(MovieData[0], "Edit Alt Title")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
            
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')
        
def editStudio():
    if launchMedia == "movie":
        editfield = "c18"
        keyboard = xbmc.Keyboard(MovieData[1], "Edit Studio")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    elif launchMedia == "tvshow":
        editfield = "c14"   
        keyboard = xbmc.Keyboard(MovieData[1], "Edit Studio")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "tvshow")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')
    
def editYear():
    if launchMedia == "movie":
        editfield = "premiered"
        keyboard = xbmc.Keyboard(MovieData[2], "Edit Year")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    
    elif launchMedia == "tvshow":
        editfield = "c05"
        keyboard = xbmc.Keyboard(MovieData[2], "Edit Year")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "tvshow")
    
    elif launchMedia == "episode":
        editfield = "c05"
        keyboard = xbmc.Keyboard(MovieData[2], "Edit Year")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "episode")
    
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')
          
def editGenre():
    if launchMedia == "movie":
       editfield = "c14"
       keyboard = xbmc.Keyboard(MovieData[3], "Edit Genre")
       keyboard.doModal()
       if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    
    elif launchMedia == "tvshow":
        editfield = "c08"
        keyboard = xbmc.Keyboard(MovieData[3], "Edit Genre")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "tvshow")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')
    
def editDirector():
    if launchMedia == "movie":
       editfield = "c15"
       keyboard = xbmc.Keyboard(MovieData[4], "Edit Director")
       keyboard.doModal()
       if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    
    elif launchMedia == "episode":
        editfield = "c10"
        keyboard = xbmc.Keyboard(MovieData[4], "Edit Director")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "episode")
    
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')

def editWriter():
    if launchMedia == "movie":
       editfield = "c06"
       keyboard = xbmc.Keyboard(MovieData[5], "Edit Writer")
       keyboard.doModal()
       if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    
    elif launchMedia == "episode":
        editfield = "c04"
        keyboard = xbmc.Keyboard(MovieData[5], "Edit Writer")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "episode")
    
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')
        
def editTagline():
    if launchMedia == "movie":
        editfield = "c03"
        keyboard = xbmc.Keyboard(MovieData[7], "Edit Tagline")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')


def editPlot():
    if launchMedia == "movie":
        editfield = "c01"
        keyboard = xbmc.Keyboard(MovieData[6], "Edit Plot")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    elif launchMedia == "tvshow":
        editfield = "c01"
        keyboard = xbmc.Keyboard(MovieData[6], "Edit Plot")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "tvshow")
    elif launchMedia == "episode":
        editfield = "c01"
        keyboard = xbmc.Keyboard(MovieData[6], "Edit Plot")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "episode")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'How did you get here?')
        
def editMPAARating():
    if launchMedia == "movie":
        editfield = "c12"
        keyboard = xbmc.Keyboard(MovieData[8], "Edit MPAA Rating")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "movie")
    elif launchMedia == "tvshow":
        editfield = "c13"
        keyboard = xbmc.Keyboard(MovieData[8], "Edit Content Rating")
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            result = (keyboard.getText().strip()) 
            detailEditor(result, editfield, "tvshow")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Not applicable', 'Not applicable for this video type')
        
        
def detailEditor(result,editfield, media):
    debug ('result', result)
    debug ('editfield', editfield)
    vdb = CVideoDatabase()
    vdb.updateDetailDB(result, editfield, launchID, media)
    xbmc.executebuiltin('ReloadSkin()')
    if launchMedia != "tvshow":
        xbmc.executebuiltin('Action(Select)')
    
def editParser():
   if ToEdit != "actor":   #using the field called 'genre' on the skin as a placeholder, checking if we should be editing movie details or actors
      getMovieDetails()
      if ToEdit == "director":
        editDirector()
      elif ToEdit == "writer":
        editWriter()
      else:
        getDetailsChoice()
   else:
      getActorDetails()
      getChoice()