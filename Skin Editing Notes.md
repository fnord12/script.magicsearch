Editing your DialogVideoInfo.xml file 
======

This document has some rough notes on what needs to be done to get magicsearch working with your skin.  Please read the readme.md file first, especially the setup section (Don't forget to add the variable in the Includes file!).    Generally speaking it is better to use the Confluence file as is.  For Estuary i would at least start with the example file and then tweak it to your preference.  These notes are if you are starting with an existing file instead of one of my examples, which isn't what i recommend.

These notes could probably use some improvements; if you're having trouble let me know and i'll help and also update the notes where they are unclear.  For the most part, the notes just tell you which control you can copy into your skin file, by ID.

## Skin variables

At the top add two new onloads:

<onload>Skin.SetBool(MagicToggle)</onload>
<onload>Skin.SetString(SortBy, "Order")</onload>

The first toggles between Search and Edit mode, the second affects the order of the actor list

## Replacing the actor panel

The stock actor panel is id 50.  This is going to be replaced with the id 500 in my sample.  You can't completely remove id 50 because Kodi is expecting to see it, but you can wipe out its contents and/or move it far offscreen so it won't be seen.  In my examples, i do both:

<control type="panel" id="50">
	<left>9999</left>
	<top>9999</top>
</control>

You can then copy in control id 500 from the appropriate example file.


## Enabling additional fields

If you're using Confluence and you want to enable additional fields for searching, add the onclicks.  See the Confluence example file for all the possibilities. 

<item>
	<label>$LOCALIZE[515]:</label>
	<label2>$INFO[ListItem.Genre]</label2>
	<onclick>RunScript(script.magicsearch,c14,"$INFO[ListItem.Genre]","$INFO[ListItem.DBTYPE]&$INFO[ListItem.DBID]&$INFO[ListItem.Year]&$VAR[MagicSearch]")</onclick>
	<visible>!IsEmpty(ListItem.Genre)</visible>
</item>

In Estuary, the fields are not clickable, which is why they had to put in a separate button for Same Director even though director is listed above.  You can see how i replaced the Same Director button - value="13" replaced with value="133" - but it's not easy to modify the other fields.

## Edit details
The edit details button is ID 67.  Note that in the Estuary version i put it at the bottom with the other buttons.  It wanted an icon so i stole an image from another button.  You may want to replace it with your own icon.

## Sort By Buttons

The Actor Sort By buttons are IDs 515,516,517 in the example files.  For Confluence you can use them as-is.  For Estuary you may want to update them into an existing Estuary button format.

## Toggle button

This is the button that will switch between search and edit mode.  Note that per the readme you can also toggle via a key, so the button isn't necessary.  If you want it, you can copy in IDs 66 and 666 from the Confluence example.  

In Estuary, i did not put in the button because i didn't see a great place to put it (again the idea is you can just use a keyboard shortcut).  But if you find a spot for it you should be able to copy in the controls from the Confluence example and then update the format to match Estuary.
	