from CDatabase import CDatabase
from strings import *

      
class CVideoDatabase:
    def __init__(self, *args, **kwargs):
        debug("CVideoDatabase init")
        self.db = CDatabase()
        self.cur = self.db.con.cursor()
    
    def GetActorFrmDB(vdb, actorName, launchID, launchMedia):
        #actorNameFixed = '%'+actorName+'%'
        #actorNameFixed = actorNameFixed.replace("'","''")
        
        sql = 'SELECT actor.actor_ID, actor_link.role, actor.art_urls, actor_link.cast_order FROM actor LEFT JOIN actor_link ON actor.actor_ID = actor_link.actor_ID where actor.name is "%s" and actor_link.media_id = "%s" and actor_link.media_type = "%s"' % (actorName, launchID, launchMedia)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def getActorID(vdb, actorName):
        #actorNameFixed = '%'+actorName+'%'
        #actorNameFixed = actorNameFixed.replace("'","''")
                
        sql = 'SELECT actor.actor_ID FROM actor where actor.name is "%s"' % (actorName)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def getMaxCastOrderDB(vdb, media_id, media_type):
        sql = 'select max(cast_order) from actor_link where media_id is "%s" and media_type is "%s"' % (media_id, media_type)
        
        debug('getMaxCastOrderDB', sql)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
    
    def checkActorEpisodeDB(vdb, actorName, launchID):
        
        sql = 'select COUNT(1), actor_link.media_id from actor_link where actor_link.actor_id in (select actor.actor_id from actor where actor.name is "%s") and actor_link.media_id in (select episode.idShow from episode where episode.idEpisode = "%s") and actor_link.media_type = "tvshow"' % (actorName, launchID) 
       
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def moveToShowDB(vdb, actorID, launchID, role, cast_order):
       
        sql = 'INSERT INTO actor_link (actor_id, media_id, media_type, role, cast_order) SELECT "%s", episode.idShow, "tvshow", "%s", "%s" FROM episode where episode.idEpisode is "%s"' % (actorID, role, cast_order, launchID) 
        
        debug('moveToShowDB', sql)
       
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def checkActorExists(vdb, actorName):
                
        sql = 'select COUNT(1), actor_id from actor where name is "%s"' % (actorName) 
       
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def checkActorInMedia(vdb, actorID, launchID, launchMedia):
                
        sql = 'select COUNT(1), actor_id from actor_link where actor_id = "%s" and media_id = "%s" and media_type = "%s"' % (actorID, launchID, launchMedia) 
        
        debug ('checkActorInMedia', sql)
       
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def updateActorName(vdb, newName, actorID):
        newName = newName.replace('"','\'')
        sql = 'Update actor set name = "%s" where actor_id = "%s"' % (newName, int(actorID))
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def updateActorOrder(vdb, newOrder, actorID, launchID, launchMedia):
        sql = 'update actor_link set cast_order = "%d" where actor_id = "%s" and media_id = "%s" and media_type = "%s"' % (int(newOrder), actorID, launchID, launchMedia)
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def updateActorThumb(vdb, newURL, actorID):
        sql = 'Update actor set art_urls = "%s" where actor_id = "%s"' % (newURL, int(actorID))
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def updateActorRole(vdb, newRole, actorID, launchID, launchMedia):
        newRole = newRole.replace('"','\'')
        sql = 'update actor_link set role = "%s" where actor_id = "%s" and media_id = "%s" and media_type = "%s"' % (newRole, actorID, launchID, launchMedia)
        
        debug ('rolesql', sql)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
    
    def cleanActorRole(vdb, oldRole, newRole, actorID, launchMedia):
        newRole = newRole.replace('"','\'')
        sql = 'update actor_link set role = "%s" where actor_id = "%s" and role = "%s" and media_type = "%s"' % (newRole, actorID, oldRole, launchMedia)
        
        debug ('rolesql', sql)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()    
        
       
    def removeActorLink(vdb, actorID, MediaID, launchMedia):
        sql = 'DELETE FROM actor_link WHERE actor_id = "%s" and media_id = "%s" and media_type = "%s"' % (actorID, MediaID, launchMedia)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def removeActorLinkComplete(vdb, actorID):
        sql = 'DELETE FROM actor_link WHERE actor_id = "%s"' % (actorID)
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def addExistingActor (vdb, result, resultRole, launchID, launchMedia, cast_order):
    
        sql = 'INSERT INTO actor_link (actor_id, media_id, media_type, role, cast_order) SELECT actor.actor_id, "%s", "%s", "%s", "%s" FROM actor where actor.name is "%s"' % (launchID, launchMedia, resultRole, cast_order, result) 
        
        debug ('addExistingActorsql', sql)
               
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def addNewActor (vdb, result):
    
        sql = 'INSERT INTO actor (name, art_urls) VALUES ("%s", "")' % (result) 
               
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
    
    def mergeActorsDB (vdb, mergeThis, mergeTo):
    
        sql = 'update actor_link set actor_id = "%s" where actor_id = "%s"' % (mergeTo, mergeThis) 
               
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()
        
    def GetMovieFrmDB(vdb, launchID):
        sql = 'select c16 as "Alt", c18 as "Studio", premiered as "Year", c14 as "Genre", c15 as "Director", c06 as "Writer", c01 as "plot", c03 as "tagline", c12 as "MPAARating" from movie where idMovie = "%s"' % launchID
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def GetTVShowFrmDB(vdb, launchID):
        sql = 'select "" as "Alt", c14 as "Studio", c05 as "Year", c08 as "Genre", "" as "Director", "" as "Writer", c01 as "plot", "" as tagline, c13 as "MPAARating" from tvshow where idShow = "%s"' % launchID
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()   
    
    def GetEpisodeFrmDB(vdb, launchID):
        sql = 'select "" as "Alt", "" as "Studio", c05 as "Year", "" as "Genre", c10 as "Director", c04 as "Writer", c01 as "plot", "" as tagline, "" as "MPAARating" from episode where idEpisode = "%s"' % launchID
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def GetMusicVideoFrmDB(vdb, launchID):
        sql = 'select c09 as "Alt", c06 as "Studio", premiered as "Year", c11 as "Genre", c05 as "Director", c10 as "Writer", c08 as "plot", "" as tagline, "" as "MPAARating" from musicvideo where idMVideo = "%s"' % launchID
        
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        return cur.fetchall()
        
    def updateDetailDB(vdb, result, editfield, ID, media):
        result = result.replace('"','\'')
        if media == "movie":
            sql = 'update movie set %s = "%s" where idMovie = "%s"' % (editfield, result, ID)
        elif media == "tvshow":
            sql = 'update tvshow set %s = "%s" where idShow = "%s"' % (editfield, result, ID)
        elif media == "episode":
            sql = 'update episode set %s = "%s" where idEpisode = "%s"' % (editfield, result, ID)
        elif media == "musicvideo":
            sql = 'update musicvideo set %s = "%s" where idMVideo = "%s"' % (editfield, result, ID)    
    
        db = CDatabase()
        cur = db.con.cursor()
        cur.execute(sql)
        db.con.commit()