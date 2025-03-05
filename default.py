import xbmc
import xbmcaddon
import sys
import xbmcgui
import editor


from strings import *
from CThread import CThread

if MagicToggle == "Search":
    debug("Search main before")
    t = CThread()
    t.start()

    debug("Search main after")
    
elif MagicToggle == "Edit" and not xbmc.Player().isPlaying() :
    debug("Edit before")
    editor.editParser()
    
else:
    debug("Unknown MagicToggle or video in progress")