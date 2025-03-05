import threading
from CDialogMagicSearch import CDialogMagicSearch
from strings import *

class CThread(threading.Thread):
    def __init__(self, movieId=0, type=''):
        threading.Thread.__init__(self)
        self.movieId = movieId
        self.type = type
    def run(self):
        wnd = CDialogMagicSearch()
        if self.movieId != 0 and self.type != '':
            wnd.doModal(self.movieId, self.type)
        else:
            wnd.doModal()
        
        