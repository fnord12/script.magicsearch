Magic Search and Editor for Kodi 21 Omega
======

![screenshot](https://github.com/fnord12/script.magicsearch/blob/master/resources/fanart.jpg)
![screenshot](https://github.com/fnord12/script.magicsearch/blob/master/resources/fanart2.jpg)

## What is it?
Two things: an improvement over Kodi's stock actor & director search (the one where you click on a name or picture to see everything they've been in), plus a metadata editor.

---
## The Actor Search
There were a few things about the stock search that i wanted to improve:

* The results were listed alphabetically.  When looking at results, i wanted to see the actor's history, to see where a current movie was in their career.  A chronological result gives you a view similar to an actor's listing at IMDb (except just with your stuff, ofc course!).

* The results were separated by media type.  So it would list movies, then TVShows, then episodes.  I wanted to see it all integrated (again, like IMDb).

* The results would list someone for every episode even if they were already listed for the show.  This was especially a problem because if you export your data to .nfo files, the show actors are exported into each episode's .nfo file.  And then when you reimport that data, the actors will be listed for every show.  Sometimes that's actually inaccurate (e.g. Tom Baker being listed for EVERY Doctor Who episode) and in any event it's unnecessary (you don't need to see William Shatner listed for every episode of Star Trek) and makes the results a big mess where it's hard to see more interesting information (like Shatner being listed for an episode of Columbo).

* The results didn't give much information about the listings.  OK, i see John Smith listed for that episode, but who did he play in that episode?  And what the heck was that episode about, anyway?  The information that Kodi did give (e.g. the watched status) didn't seem that interesting to me.

* The results combine actor and director credits into a single list.  I LIKE that, but wanted to know when a person was appearing as a director or as an actor.  And why not include the writing credits as well?

* Remember who you're searching for!  This is small, but i wanted to see the name of the person i clicked on at the top of the search results.  I also wanted to be able to pop-up a bigger picture of the person.

* Intersection search - i wanted the ability to click on an actor and then input the name of a second actor to see all the videos they appeared in together - all of the Bela Lugosi and Boris Karloff team-ups, for example!


## The Actor List
In addition to the search results themselves, there were a few things i wanted to tweak on the page where you see the list (or card deck) of actors.  The above noted .nfo import problem would also mess with the Order field (since it was merging show actors into each episode).  I wanted to ensure that the true episode actors always appeared first (and were perhaps distiguished in some way: guest roles will be indicated with an asterisk) and that actors who were listed for the show always came next.  Additionally, i wanted to ability to sort the list.  The Order field is a great way to prioritize the list, but sometimes you just want to find an actor by their name, or by role.

## The Editor
Once you start looking at all this data more closely, you're going to see things that you want to change!  The traditional way to change data in Kodi is to export your .nfo files, edit them, and then refresh the video.  Not only does that lead to issues (the above noted show/episode merge, and also potentially problems with your artwork if you're not careful), it's tedious!  So i wanted to create a way to edit data about the actors directly in Kodi.  This editor allows you to do the following:

* Change an actor's name - this will affect the overall listing for this actor.  So if you are changing a listing for Jerry Angelo Brooks to JB Smoove, it will affect all instances of Jerry Angelo Brooks (which is what you'd want!).  If you already have listings for JB Smoove, it will merge the listings.

* Edit Role - affects the current listing only

* Edit Order

* Edit Picture - this allows you to input a URL of a picture that will replace the current actor photo

* Remove from an episode/movie/show

* Completely Remove Actor - use this for removing garbage data only

* Swap Actor and Role - this addresses a problem that is currently affecting the TMDb scraper, where it is sometimes bringing the actor and role data backwards.  This will fix all instances where the data is swapped (i.e. not just the current episode)

* Move from Episode to Show - if a person is in enough episodes and you think you just want to see them listed once for the show instead of each episode.  If you change your mind, remove them from the show; the fact that they were in the episodes is retained.

* Add a new actor - more on this below

Enable edit mode either by clicking the button on the skin or using a keyboard shortcut (see Setup below).  
Enabling edit mode will cause the Order values to be displayed next to the actor names.  The name will turn red when you hover over it, indicating that if you click on an actor it will offer edit options instead of generating search results.  When looking at an episode and selecting an actor to edit, you will be warned if the actor really exists for the show and not just the episode (you can still edit it).


Once i started allowing data to be edited, i figured why not do it for other data:

*Alternate title
*Studio
*Year
*Genre*
*Director
*Writer
*Tagline
*Plot
*Rating (MPAA or TV)

A button to Edit Details will appear when you enable edit mode.  These are all just basic text edits, nothing fancy.  

If you want to clear/blank out a field, input a single space. 

If you want multiples listed, use space slash space: " / ".  For example, if there are multiple writers (David Semel / Patience Thoreson) or if you want to list more than one genre.  This will enable the search to distinguish them.

Plot data is large and Kodi only allows for a single text line editor, so it's not the easiest thing to use, but i've found it useful for fixing a typos and appending some additional information at the end.  You can also clear out the current plot and paste in something you've copied from elsewhere (and/or edited in Notepad or something).

## Other searches
Once i was allowing the editing of fields like Studio, i thought why not enable the search for those as well.  So click on Studio, Year, Genre, Director, or Writer to trigger the search.  For Year and Genre, since there are potentially A LOT of results, i limited so that it's doing an intersectional search (e.g. click on Comedy for a movie made in 2002 and it will show you all comedies made in that year).  It's possible to configure it to just return all comedies or all movies in 2002, if your system can handle it.

## Add Actor
You can input an actor name to add them to the listing for the current video.

To save time, you can also input the actor and role name at the same time.  There are three delimiters that you can use:

```
Arnold Schwarzenegger>Terminator

Arnold Schwarzenegger as Terminator

Arnold Schwarzenegger 	... 	Terminator
```

The third thing, tab elipse tab, is what you get when you copy & paste from IMDb.  It'll look weird - the tabs come up as little boxes with Xs - but it'll work.

You can also input multiple actors at once.  To do this start off with an asterisk, and separate each actor/role pair with a comma:

*Arnold Schwarzenegger 	... 	Terminator, Michael Biehn 	... 	Kyle Reese, Linda Hamilton 	... 	Sarah Connor

If you're clever, you can create macros in Notepad++ (or similar) so that you can copy and paste large chunks of actor/role information from IMDb (or elsewhere) and then press a button to format it in the way that this program needs it.

If you input an actor that already exists, the system will handle it.  It will update the role information if you're providing that.

If you're doing a multi-actor add, make sure there are no commas in the roles (or actor names) since that is a delimeter.

Note that Kodi does not use unique keys to distinguish actors.  It goes entirely by names.  So you occasionally run into issues where multiple actors have the same name.


---
## Setup

This isn't a simple add-on to install.  First, if you're not using the stock SQLite database, you may need to tweak it to get it to work.  If you're using the tagoverview addon in my repository, this will work for you too.  Otherwise you may have to modify the CDatabase.py file.

A tip if using MYSQL:
>
>Download mysql-connector-python-8.0.17.tar.gz Source from 
>https://pypi.org/project/mysql-connector-python/#files
>copy from zip only folder ../lib/mysql/*.* to ../addons/script.tagoverview/mysql
>
>Add database parameters in CDatabase.py
>under
>class CDatabase:
>
>    baseconfig = {
>    }
>
>Add database parameters in MySQLconfig.py
>under
>class Config(object):

But the bigger thing is that you will have to modify your skin.  The DialogVideoInfo.xml file will have to be modified.  Under \resources\skins\Default\720p, i have included sample DialogVideoInfo files that can be used for Confluence and Estuary.  Best thing to do is to make a copy of your Confluence or Estuary skin and import the copy as its own skin (give it its own name).  Then rename the appropriate example file to replace the existing DialogVideoInfo file.  The Confluence file is fully baked - it's what i use myself.  The Estuary version is more of a proof of concept.  It'll work but you may want to tweak it.

The Skin Editing Notes.md file goes into more detail if you want to see the specifics but unless you've already got a customized version of the skin you will be better off starting with the example file and then tweaking it to your liking.

You will also have to modify your Includes.xml file.  I've also included a sample Includes file, but the change there is more simple.  You just have to add the following to your Variables section (in Estuary, you can either put it in the Includes file or in the Variables file that it includes; either will work):


```
<variable name="MagicSearch">
	<value condition="Skin.HasSetting(MagicToggle)">Search</value>
	<value condition="!Skin.HasSetting(MagicToggle)">Edit</value>
	<value>Search</value>
</variable>
```

You may also want to map the ability to toggle between Search and Edit mode to a key.  In the Confluence example, there is a button that you can click to toggle.  But i find just pushing my E button to be easier:


```
<keymap>
    <global>
        <keyboard>
		<!-- leave other stuff already here -->
			
		<e>Skin.ToggleSetting(MagicToggle)</e>
	</keyboard>
    </global>
	
<!-- leave other stuff already here -->
	
</keymap>
```

Finally, if you want, you can further customize the search results pop-up.  This is optional, and of course i think that the results are perfect as is.  But the MagicSearchResults.xml can be edited however you like - add/remove fields, etc..  Estuary users in particular may want to tweak the look&feel of it since it was designed to match Confluence style pop-ups.  Note that unlike the example files, the MagicSearchResults.xml is used by the addon, so don't remove it completely.

---
## Caveats:

### Danger Zone
The metadata editor works by modifying your database directly.  I've been using this for years with no problems.  I've tested by inputting all sorts of garbage into the edit fields, trying to find something that will break the database.  So far, it's handled it all (it mostly just takes your garbage and displays it back to you as text).  But i can't promise that your set-up won't have some difference that will cause a problem that could corrupt your database.  The search should be safe no matter what.  If you're going to try the editor, back up your database regularly, at least at first.  The standard Backup program that is part of the Kodi addon repository can backup your database on a daily schedule.

Also, be aware of what you're doing when COMPLETELY REMOVING an actor or using the Swap fix.


### What's Supported

Tested in Kodi 21 Omega.  Tested with local files only (not with streaming, not with SMBs).  It may still work in other cases.  See above regarding the database set-up; i personally can only support SQLite.

---
### Challenges

1. In order to make your changes visible to you, i use Kodi's Skin Refresh function.  The Skin Refresh function was really meant to allow Skin developers the ability to check their work, and it occassionally/rarely causes a crash.  The crash doesn't cause anything to break, it just means you have to restart Kodi.

2. Right clicking on actor list will show some weird options (like "Play").  That's just due to the nature of how i'm generating the list (and the fact that the Kodi developers removed the ability to customize plugin context menus in v18).  Nothing bad will happen if you choose one of the options (in fact, nothing at all will happen).

---

## Credit

1. The core database code for both searching and editing was taken from the tagoverview add-on, which i'm currently maintaining but which was originally developed by olivarr.  I could not have written this without using that code.

2. Also thanks to ronie and Lunatix, who provided help on the Kodi forum.
