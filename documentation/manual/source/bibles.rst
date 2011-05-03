======
Bibles
======

Managing Bibles in OpenLP is a relatively simple process. There are also 
converters provided to get data from other formats into OpenLP.

.. _bibleimporter:

Bible Importer
==============

If you are using an earlier version of OpenLP or, come from another software 
package, you may be able to convert your existing database to work in OpenLP
2.0. To access the Bible Importer :menuselection:`File --> Import --> Bible`.
You may also enter the Bible Importer by clicking the :guilabel:`Import Icon:`

.. image:: pics/themeimportexport.png

You will see the Bible Importer window, click :guilabel:`Next`.

.. image:: pics/bibleimport01.png

After clicking :guilabel:`Next` you can select from the various types of
software that OpenLP will convert Bibles from. Click on the file folder icon to
choose the file(s) of the Bible database you want to import. See the sections
below for more information on the different formats that OpenLP will import.
Click :guilabel:`Next` to continue.

.. image:: pics/bibleimport02.png

After selecting your file(s), you'll be asked to fill in the details of the
Bible you are importing. Remember to check what information you need to display
for your Bible's translation, as some of them have strict rules around the
copyright notice. Click :guilabel:`Next` to continue.

.. image:: pics/bibleimportdetails1.png

After filling in the copyright details, OpenLP will start to import your Bible.
It may take some time to import your Bible so please be patient.

.. image:: pics/bibleimportfinished1.png

When the import has finished click :guilabel:`Finish` and you should be 
ready to use your Bible in OpenLP.

Importing from openlp.org 1.x
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Importing Bibles from openlp.org 1.x is a simple process. First you will need to 
locate your version 1.x Bibles. Version 1.x Bibles have the `.bible` file
extension.

Windows XP::

    C:\Documents and Settings\All Users\Application Data\openlp.org\Data\Bibles\

Windows Vista / Windows 7::

    C:\ProgramData\openlp.org\Data\Bibles\

After selecting all of the openlp.org 1.x Bibles you want to convert, click
:guilabel:`Next` to continue the import process.

Importing OSIS Bibles
^^^^^^^^^^^^^^^^^^^^^

Importing OSIS files is very simple. Select OSIS as your import source, select
your OSIS Bible file and continue the import process.

**About OSIS Formatted Bibles**

The OSIS XML standard was designed to provide a common format for distribution
of electronic Bibles. More information can be found out at the `Bible Technologies website 
<http://www.bibletechnologies.net/>`_. 

If you have any software installed that is part of the `Sword Project 
<http://www.crosswire.org/sword/index.jsp>`_ it can be easily converted.

You can use the commands below convert Bibles from that software to OSIS format. 

The following commands are used in all platforms and the commands are case 
sensitive across all platforms. To convert a Bible using the command prompt in 
Windows or a terminal in Linux or Mac OS X you would type::

    mod2osis biblename > biblename.osis

For example: if I wanted to convert a King James Version Bible I would type
something similar to this::

    mod2osis KJV > kjv.osis

You may also wish to dictate a file location for the conversion to place the 
osis file for example::

    mod2osis KJV > /home/user/bibles/kjv.osis

Importing OpenSong Bibles
^^^^^^^^^^^^^^^^^^^^^^^^^

Converting from OpenSong you will need to locate your bibles database. In the 
later versions of OpenSong you are asked to define the location of this. The 
songs will be located in a folder named :guilabel:`Bibles`. This folder should
contain files with all your bibles in them without a file extension. (file.xmms).
When you have located this folder you will need to select the bible from the 
folder. 

You may also import downloaded bibles from OpenSong. The process is the same,
except you will need to extract the bible from a zip file. This is usually done
by right clicking on the downloaded file and select `Extract` or `Extract Here`.

After selecting the OpenSong Bibles you want to import, follow the rest of the
import process. When the import has finished you should be ready to use your
OpenSong Bibles.

Importing Web Download Bibles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**About Web Download**

OpenLP provides a Web Download method to import Bibles when you do not have a
locally installed Bible available. The Web Download method registers the Bible
in OpenLP like the other bibles only it downloads the verses as you need them.
This import is not meant to be used as your sole source for Bibles, but rather
as another option and does require an internet connection.

To use the web download feature select web download from the import wizard.

You can select from several options of location to download from and also
what Bible translation you need. You will probably want to choose the location 
from where you get the best performance or has the translation you need.

.. image:: pics/webbible1.png

You can also select a proxy server if needed from the `Proxy Server` tab. Your
network administrator will know if this is necessary, in most cases this will
not be needed.

.. image:: pics/webbibleproxy1.png

After selecting your download location and the Bible you wish to use, click
:guilabel:`Next` to continue the import process. When your import is completed
you should now be ready to use the web bible.

Importing CSV formatted Bibles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have a Bible in .csv format OpenLP can import it. CSV Bibles will
consist of two files a `books` file and a `verse` file. Select CSV from the list
of Bible types to import.

You are now ready to select your .csv files. You will need to select both your 
books and verse file location.

.. image:: pics/csvimport1.png

After you have selected the file locations you can continue with the import
process. Once it is complete you should be ready to use your imported CSV Bible.
