=====
Songs 
=====

Managing your songs in OpenLP is a relatively simple process. There are also 
converters provided to get data from other formats into OpenLP.

Song Importer
=============

If you are using an earlier version of OpenLP or come from another software 
package, you may be able to convert your existing database to work in OpenLP
2.0. To access the Song Importer :menuselection:`File --> Import --> Song`.
You will then see the Song Importer window, then click :guilabel:`Next`.

.. image:: pics/songimporter.png 

After choosing :guilabel:`Next` you can then select from the various types of 
software that OpenLP will convert songs from.

.. image:: pics/songimporterchoices.png

Then click on the file folder icon to choose the file of the song database you
want to import. See the following sections for information on the different 
formats that OpenLP will import.

Importing from OpenLP Version 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Converting from OpenLP Version 1 is a pretty simple process. You will first 
need to locate your version 1 database file.

Windows XP::

    C:\Documents and Settings\All Users\Application Data\openlp.org\Data\songs.olp

Windows Vista / Windows 7::

    C:\ProgramData\openlp.org\Data\songs.olp

After clicking :guilabel:`Next` your conversion should be complete. 

.. image:: pics/finishedimport.png

Then press :guilabel:`Finish` and you should now be ready to use your OpenLP 
version one songs.

Importing from OpenSong
^^^^^^^^^^^^^^^^^^^^^^^

Converting from OpenSong you will need to locate your songs database. In the 
later versions of OpenSong you are asked to define the location of this. The 
songs will be located in a folder named :guilabel:`Songs`. This folder should
contain files with all your songs in them without a file extension. (file.xxx).
When you have located this folder you will then need to select the songs from
the folder.

.. image:: pics/selectsongs.png

On most operating systems to select all the songs, first select the first song
in the lest then press shift and select the last song in the list. After this
press :guilabel:`Next` and you should see that your import has been successful.

.. image:: pics/finishedimport.png

Press :guilabel:`Finish` and you will now be ready to use your songs imported
from OpenSong.

Importing from CCLI Song Select
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To import from CCLI Song Select you must be a CCLI Subscriber and also a 
subscriber of the Song Select service. For info on that go to: 
http://www.ccli.com 

The first step for importing from CCLI Song Select is to log into your account.
Then search for your desired song. For this example we will be adding the song
"Amazing Grace". 

.. image:: pics/songselectsongsearch.png

For the song you are searching for select `lyrics` This should take you to a 
page displaying the lyrics and copyright info for your song.

.. image:: pics/songselectlyrics.png

Next, hover over the :guilabel:`Lyrics` menu from the upper right corner. Then
choose either the .txt or .usr file. You will then be asked to chose a download
location if your browser does not automatically select that for you. Select 
this file from the OpenLP import window and then click :guilabel:`Next` You can
also select multiple songs for import at once on most operating systems by 
selecting the first item in the list then holding shift select the last item in
the list. When finished you should see that your import has completed.

.. image:: pics/finishedimport.png

Press :guilabel:`Finish` and you will now be ready to use your songs imported
from CCLI SongSelect.


