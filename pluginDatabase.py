from CDatabase import CDatabase

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
            xbmc.log(u"MSRCH: {0}".format(msg).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
        else:
            xbmc.log(u"MSRCH: {0}#{1}#".format(msg, txt).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
    except:
        print "Error in Debugoutput"
        print msg
        print args

      
class CVideoDatabase:
    def __init__(self, *args, **kwargs):
        debug("CVideoDatabase init")
        self.db = CDatabase()
        self.cur = self.db.con.cursor()
    
    def GetActorsDB(vdb,ID,Media):
        if Media == "episode":
            sql = 'select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "1" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id = "%s" and actor_link.media_type = "episode" and actor.name not in (select actor.name from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id in (select episode.idshow from episode where episode.idEpisode = "%s") and actor_link.media_type = "tvshow") UNION select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "2" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id in (select episode.idshow from episode where episode.idEpisode = "%s") and actor_link.media_type = "tvshow" order by SOrder, actor_link.cast_order, actor.name' % (ID, ID, ID) 
        else:
            sql = 'select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id = "%s" and actor_link.media_type = "%s" order by actor_link.cast_order, actor.name' % (ID, Media)
        
        debug('sql = ', sql)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def GetActorsDBOrderByName(vdb,ID,Media):
        if Media == "episode":
            sql = 'select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "1" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id = "%s" and actor_link.media_type = "episode" and actor.name not in (select actor.name from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id in (select episode.idshow from episode where episode.idEpisode = "%s") and actor_link.media_type = "tvshow") UNION select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "2" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id in (select episode.idshow from episode where episode.idEpisode = "%s") and actor_link.media_type = "tvshow" order by SOrder, actor.name' % (ID, ID, ID) 
        else:
            sql = 'select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id = "%s" and actor_link.media_type = "%s" order by actor.name' % (ID, Media)
        debug('sql = ', sql)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()   

    def GetActorsDBOrderByRole(vdb,ID,Media):
        if Media == "episode":
            sql = 'select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "1" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id = "%s" and actor_link.media_type = "episode" and actor.name not in (select actor.name from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id in (select episode.idshow from episode where episode.idEpisode = "%s") and actor_link.media_type = "tvshow") UNION select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "2" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id in (select episode.idshow from episode where episode.idEpisode = "%s") and actor_link.media_type = "tvshow" order by SOrder, actor_link.role, actor.name' % (ID, ID, ID) 
        else:
            sql = 'select actor.name, actor.art_urls, actor_link.role, actor_link.cast_order, "" as SOrder from actor left join actor_link on actor.actor_id = actor_link.actor_id where actor_link.media_id = "%s" and actor_link.media_type = "%s" order by actor_link.role, actor.name' % (ID, Media)
        debug('sql = ', sql)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()              