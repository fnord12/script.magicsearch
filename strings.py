import xbmcaddon, xbmc, sys, xbmcgui

def debug(msg, *args):
    try:     
        xbmc.log("MAGICSEARCH: " + (str(msg)))
     
        for arg in args:
            print(str(arg))
    except:
        print("MAGICSEARCH strings.py: Error in Debugoutput")
        print(msg)
        print(args)

ADDON = xbmcaddon.Addon(id='script.magicsearch')
language = ADDON.getLocalizedString
ACTION_MOVE_LEFT       =  1 #Dpad Left
ACTION_MOVE_RIGHT      =  2 #Dpad Right
ACTION_MOVE_UP         =  3 #Dpad Up
ACTION_MOVE_DOWN       =  4 #Dpad Down
ACTION_PAGE_UP         =  5 #Left trigger
ACTION_PAGE_DOWN       =  6 #Right trigger
ACTION_SELECT_ITEM     =  7 #'A'
ACTION_SELECT_ITEM2    =  100 #Mouse Left Click'
ACTION_HIGHLIGHT_ITEM  =  8
ACTION_PARENT_DIR      =  9 #'B'
ACTION_PREVIOUS_MENU   = 10 #'Back'
ACTION_SHOW_INFO       = 11
ACTION_PAUSE           = 12
ACTION_STOP            = 13 #'Start'
ACTION_NEXT_ITEM       = 14
ACTION_PREV_ITEM       = 15
ACTION_XBUTTON	       = 18 #'X'
ACTION_YBUTTON 	       = 34	#'Y'
ACTION_MOUSEMOVE       = 90 # Mouse has moved
ACTION_PREVIOUS_MENU2  = 92 #'Back'
ACTION_CONTEXT_MENU    = 117 # pops up the context menu
ACTION_CONTEXT_MENU2   = 229 # pops up the context menu (remote control "title" button)

MOVIELIST = 4
SEARCHLABEL = 3
SEARCHTHUMB = 20

PROPERTY_TAGID                  = "movieid"
PROPERTY_MOVIEID                = "movieid" #???
PROPERTY_TYPE                   = "type"

PROPERTY_ENABLED = "enabled"
YEAR = "year"
POSTER = "poster"
PLOTSUM = "plotsum"
ROLE = "role"           #director, writer, or actor role
MEDIA = "media"         #movie, TVShow, or Episode
SHOWTITLE = "showtitle"
PATH = "path"
ACTORTHUMB = "actorThumb"
DIRECTOR = "Director"

PROPERTY_MOVIE          = 'movie'
PROPERTY_TVSHOW         = 'tvshow'
PROPERTY_MUSICVIDEO     = 'musicvideo'

combinedParameter = sys.argv[3]
combinedParameter = combinedParameter.replace("?","")
combinedParameter = combinedParameter = combinedParameter.split('&')

searchField = ToEdit = sys.argv[1]

if searchField == "director" or searchField == "writer":
    searchField = "actor"
    
actorName = searchParameter = sys.argv[2]

MagicToggle = combinedParameter[3]

if MagicToggle == "Search":
    if " / " in searchParameter:
            searchParameterChoices = searchParameter.split(" / ")
            Choice = xbmcgui.Dialog().select("Choose an option",searchParameterChoices)
        
            if Choice < 0:
                sys.exit()
        
            searchParameter = searchParameterChoices[Choice]

launchMedia = combinedParameter[0]
launchID = combinedParameter[1]
secondParameter = combinedParameter[2]


debug("combinedParameter", combinedParameter)
debug("searchField", searchField)
debug("ToEdit", ToEdit)
debug("actorName", searchParameter)
debug("searchParameter", searchParameter)
debug("launchMedia", launchMedia)
debug("launchID", launchID)
debug("secondParameter", secondParameter)
debug("MagicToggle", MagicToggle)


def error(msg, *args):
    txt=''
    for arg in args:
        if type(arg) == int:
            arg = str(arg)
        txt = txt + "/" + str(arg)
    if txt == '':
        xbmc.log("Tag: "+str(msg), xbmc.LOGERROR)
    else:
        xbmc.log("Tag: "+str(msg)+"#"+txt+"#", xbmc.LOGERROR)        

def encode(s):
    return s.encode('utf-8','replace')

def decode(string):
    #return string.decode('utf-8','replace')
    return

def uc(s):
    return unicode(s, 'utf-8','replace')
   