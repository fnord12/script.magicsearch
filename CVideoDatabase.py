from CDatabase import CDatabase
from strings import *

      
class CVideoDatabase:
    def __init__(self, *args, **kwargs):
        debug("CVideoDatabase init")
        self.db = CDatabase()
        self.cur = self.db.con.cursor()
    
    # The big get
    def GetMovies(self, searchPrm):
        
        #dealing with Actor or Director names like Sting or McG.
        if (searchField == 'actor') and ' ' not in searchPrm:
            searchParameterFixed = searchPrm
        else:
            searchParameterFixed = '%'+searchPrm+'%'
            #searchParameterFixed = searchParameterFixed.replace("'","''")
        
        debug ('searchField', searchField)
        debug ('searchParameterFixed', searchParameterFixed)
        debug ('searchPrm', searchPrm)
        debug ('secondParameter', secondParameter)
        debug ('launchMedia', launchMedia)
        
        if (searchField == 'actor') or (searchPrm != searchParameter):  #or if there's been a second search paramter inputted via the Intersection button
            debug ("Main actor search")
           
            sql = 'select idMovie as "ID", c22 as "Path", substr(premiered,1,4) as "Year", "Movie" as Media, "[I]Writer[/I] " as Role, premiered as Date, "2" as "SOrder" from movie where c06 like "%s" UNION select idMovie as "ID", c22 as "Path", substr(premiered,1,4) as "Year", "Movie" as Media, "[I]Director[/I] " as Role, premiered as Date, "1" as "SOrder" from movie where c15 like "%s" UNION select idEpisode as "ID", c18 as "Path", substr(c05,1,4) as "Year", "Episode" as Media, "[I]Director[/I] " as Role, c05 as Date, "1" as "SOrder" from episode where c10 like "%s" UNION select idEpisode as "ID", c18 as "Path", substr(c05,1,4) as "Year", "Episode" as Media, "[I]Writer[/I] " as Role, c05 as Date, "2" as "SOrder" from episode where c04 like "%s" UNION select idMovie as "ID", c22 as "Path", substr(premiered,1,4) as "Year", "Movie" as Media, (select actor_link.role from actor INNER JOIN actor_link on actor.actor_id  = actor_link.actor_id and actor_link.media_id = movie.idMovie where actor.name like "%s") as Role, premiered as Date, "3" as "SOrder" from movie where idMovie in ( select media_id from actor_link where media_type = "movie" and actor_id in (select actor_id from actor where name like "%s") ) UNION select idShow as "ID", "" as Path,  substr(c05,1,4) as "Year", "TVShow" as Media, (select actor_link.role from actor INNER JOIN actor_link on actor.actor_id  = actor_link.actor_id and actor_link.media_id = tvshow.idShow where actor.name like "%s") as Role, c05 as Date, "3" as "SOrder" from tvshow where idShow in ( select media_id from actor_link where media_type = "tvshow" and actor_id in (select actor_id from actor where name like "%s") ) UNION select idEpisode as "ID", c18 as "Path", substr(c05,1,4) as "Year", "Episode" as Media, (select actor_link.role from actor INNER JOIN actor_link on actor.actor_id  = actor_link.actor_id and actor_link.media_id = episode.idEpisode where actor.name like "%s") as Role, c05 as Date, "3" as "SOrder" from episode where idEpisode in ( select media_id from actor_link where media_type = "episode" and actor_id in (select actor_id from actor where name like "%s") ) order by Date, SOrder'  % (searchParameterFixed, searchParameterFixed, searchParameterFixed, searchParameterFixed, searchPrm, searchPrm, searchPrm, searchPrm, searchPrm, searchPrm)
        
        elif launchMedia == "movie":
            debug ("movie search")
            if secondParameter == " ":
                debug ("single paramter movie search")
                sql = 'select idMovie as "ID", c22 as "Path", substr(premiered,1,4) as "Date", "Movie" as Media, "" as Role from movie where %s like "%s" order by premiered' % (searchField, searchParameterFixed)
            else:  #if two params were given on the skin, e.g. genre by year
                debug ("double paramter movie search")
                secondParameterFixed = '%'+secondParameter+'%'
                secondParameterFixed = secondParameterFixed.replace("'","''")
                sql = 'select idMovie as "ID", c22 as "Path", substr(premiered,1,4) as "Date", "Movie" as Media, "" as Role from movie where %s like "%s" and substr(premiered,1,4) like "%s" order by premiered' % (searchField, searchParameterFixed, secondParameterFixed)
            
        elif launchMedia == "tvshow" or launchMedia == "episode":
            debug ("tv search")
            if secondParameter == " ":
                debug ("single paramter tv search")
                sql = 'select idShow as "ID", "" as "Path", substr(c05,1,4) as "Date", "TVShow" as Media, "" as Role from tvshow where %s like "%s" order by Date' % (searchField, searchParameterFixed)
            else:
                debug ("double paramter tv search")
                secondParameterFixed = '%'+secondParameter+'%'
                secondParameterFixed = secondParameterFixed.replace("'","''")
                sql = 'select idShow as "ID", "" as "Path", substr(c05,1,4) as "Date", "TVShow" as Media, "" as Role from tvshow where %s like "%s" and substr(c05,1,4) like "%s" order by Date' % (searchField, searchParameterFixed, secondParameterFixed)
            
        debug("sql = ", sql)
        self.cur.execute(sql)
        return self.cur.fetchall()
        
    # not used - part of the abandoned idea of displaying thumbnail in search results
    def GetActor(self):
        
        searchParameterFixed = '%'+searchPrm+'%'
        searchParameterFixed = searchParameterFixed.replace("'","''")
        
        sql = "select art_urls from actor where name like '%s' limit 1" % (searchParameterFixed)
        self.cur.execute(sql)
        return self.cur.fetchall()
        
    #called in the BuildList  
    def GetMediaPath(self,mediaID):
        sql = 'select path.strPath from path where path.idPath = (select tvshowlinkpath.idPath from tvshowlinkpath where tvshowlinkpath.idShow = "%d")' % (mediaID)
        self.cur.execute(sql)
        return self.cur.fetchall()
    
    #more tagoverview legacy
    def GetFileId(self, pathid):
        sql = u"select movie_view.idFile from movie_view where %s = %s" % (self.db.concatrows("movie_view.strPath","movie_view.strFileName"), self.db.pparam)
        debug("CVideoDatabase getfileid: sql:%s %s" % (type(pathid),pathid))
        self.cur.execute(sql,((pathid),))
        row = self.cur.fetchone()
        debug("CVideoDatabase getfileid: ROW:{0}".format(row))
        if row:
            return row[0]
        else:
            return 0

    #get type (tvshow, movie, musicvideo) and movieid in that table
    def GetTypeAndId(self, fileId, path):
        r = ['',0,'']
        if fileId>0:
            r = ['',0,'']
            sql = "select idMovie, c00 from movie where idFile = %s order by movie.c00" % (self.db.pparam)
            #sql = "select idMovie, c00 from movie where idFile = {0}".format(fileId)
            debug("CVideoDatabase typeandid movies: sql:{0}".format(sql))
            self.cur.execute(sql,((fileId),))
            row = self.cur.fetchone()
            if row:
                id = row[0]
                name = row[1]
                if id != 0:
                    r[0] = "movie"
                    r[1] = id
                    r[2] = name
                    return r
            #sql = "select idMVideo, c00 from musicvideo where idFile = {0}".format(fileId)
            sql = "select idMVideo, c00 from musicvideo where idFile = %s" % (self.db.pparam)
            debug("CVideoDatabase typeandid musicvideo: sql:{0}".format(sql))
            self.cur.execute(sql,((fileId),))
            row = self.cur.fetchone()
            if row:
                id = row[0]
                name = row[1]
                if id != 0:
                    r[0] = "musicvideo"
                    r[1] = id
                    r[2] = name
                    return r
        else:
            #sql = "select idShow, c00 from tvshow_view where strPath = '{0}'".format(path)
            sql = "select idShow, c00 from tvshow_view where strPath = %s" % (self.db.pparam)
            debug("CVideoDatabase typeandid tvshow: sql:{0}".format(sql))
            self.cur.execute(sql,((path),))
            row = self.cur.fetchone()
            if row:
                id = row[0]
                name = row[1]
                if id != 0:
                    r[0] = "tvshow"
                    r[1] = id
                    r[2] = name
                    return r
        return 0
