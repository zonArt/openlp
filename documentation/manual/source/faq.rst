======
F.A.Q.
======

General Questions
=================

**What is OpenLP?**

OpenLP stands for "Open source Lyric Projection" and is presentation software 
developed for Churches to provide a single easy to use interface for the 
projection needs of a typical act of Worship. First created in 2004, it has 
steadily grown in features and maturity such that is it now a mainstay in 
hundreds of churches around the world. 

It can hold a searchable database of song lyrics and Bible verses allowing them 
to be projected instantly or saved in a pre-prepared order of service file. 
Themes allow song backgrounds to be changed instantly. PowerPoint presentations, 
videos and audio files can be run from within the program removing the need to 
switch between different programs. Alert messages can be displayed so the 
Nursery or Car park stewards can notify the congregation easily. Remote 
capability allows the worship leader to change songs, or for alert messages to 
be sent from anywhere on the network, even via a phone.

Being free, this software can be installed on as many PC's as required, even on 
the home PC's of worship leaders without additional cost. Compared to the 
expensive site licenses or restrictions of commercial software we believe OpenLP 
cannot be beaten for value.  Still in active development by a growing team of 
enthusiastic developers, features are being added all the time, meaning the 
software just improves all the time.

**When is the release date for OpenLP 2.0?**

`It will be ready when it's ready!` We do not have fixed dates, but we have 
set some [[Version_2_Milestones|targets for the releases]]. If you take part in 
the [[Development:Getting_Started|development]], start to 
[[Testing:Getting_Started|test OpenLP]] and [[Help:Contents|provide feedback]] 
this will speed up the progress.

**Can I help with OpenLP?**

OpenLP is possible because of the commitment of individuals. If you would like 
to help there are several things that you can get involved with. Please see: 
`Contributing <http://openlp.org/en/documentation/introduction/contributing.html>`_ 
for more information.

**I use and like OpenLP and would like to tell others online. Where can I do 
this?**

A variety of places!

* Are you on facebook? Then `become a fan <http://www.facebook.com/openlp>`_
* Are you on twitter? Then `follow openlp <http://twitter.com/openlp>`_, and retweet the announcements.
* Give us a thumbs up on the `SourceForge project page <http://www.sourceforge.net/projects/openlp>`_ 
* If you have a website or blog, then link to our site http://www.openlp.org with a few words saying what the software is and why you like it.
* Add a placemark on our `Worldwide Usage map <http://maps.google.com/maps/ms?ie=UTF8&source=embed&msa=0&msid=113314234297482809599.00047e88b1985e07ad495&ll=13.923404,0&spn=155.179835,316.054688&z=2>`_, so others in your locality can see someone close by is using it.
* If you are a member of any Christian Forums or websites, and their rules allow it, then perhaps review the software or ask others to review it.

What operating systems will OpenLP 2.0 support?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

OpenLP 2.0 is designed to be cross platform. Currently it has been known to run 
on Windows (XP, Vista, 7), Linux (Ubuntu/Kubuntu, Fedora), FreeBSD & Mac OSX. 
[[Help:Contents|Please let us know]] if you've successfully run it on something 
else.

**Which programming language is 2.0 developed in?**

OpenLP 2.0 is written in `Python <http://www.python.org>`_ and uses the 
`Qt4 toolkit <http://qt.nokia.com>`_. Both are cross-platform which allows the 
software to run on different types of machine and so allow more people access to 
free worship software. Python is one of the easier programming languages to 
learn, so this helps us develop and find [[Bug|bugs]] quicker, and also allows 
more developers to contribute with the project.

**Which written languages does OpenLP support?**

The beta now has support for a few languages which can be seen on the 
:menuselection:`Settings -->Translate` menu. However some of these translations 
are incomplete. If you would like to help complete or start to translate OpenLP 
into your language then see the [[Translation:Getting_Started|Getting started page]]. 

**What is a beta release?**

A beta release is a release which is almost feature complete and is fairly 
stable. However there may still be a few [[Version_2_Features|features]] to 
complete, and [[bugs]] we've not yet fixed. It is used by several people without 
serious problems. However there is a small possibility that it could still crash 
occasionally or do unexpected things. It is intended for those who want the 
latest version, and are prepared to give the program a good test before using it 
in a live situation to ensure they won't encounter any unexpected problems. If 
you want to have a look at the latest beta release then just 
`download it <http://openlp.org/en/download.html>`_.

**Should I use this beta release at Church in my Sunday services?**

As long as you have taken the time to run through your service a couple of times 
on your target machine, the answer to this question is **yes**. The OpenLP 
team believes that OpenLP 2.0 beta 1 is stable enough to be used in Sunday 
services. As of beta 1, there are a good number of churches already using 
version 2.0 successfully. The OpenLP team works hard to make sure each release 
is solid, but cannot yet guarantee that everything works perfectly, or even 
correctly.

If however your congregation is made up of 85 year old women who snarl when you 
suggest replacing the gas lamps with electric light bulbs and consider the pipe 
organ too loud and modern, then we recommend sticking with version 1.2 for now.

As of beta 1, version 1.2 of OpenLP is "put out to pasture" - no more 
development or even bugfixes will be performed on that version.

Upgrading
^^^^^^^^^

**Does 2.0 replace 1.2, or can they be run side by side?**

It is perfectly safe to install 2.0 on a system with 1.2. Both versions are 
installed in separate places, so you can still go back to 1.2. You can even run 
them at the same time!

2.0 stores its data in a separate folder to 1.2, so your data is perfectly safe, 
and whatever you do in 2.0 will not damage 1.2

**Are 1.2 and 2.0 compatible?**

No. However imports exist to transfer your data to the new version.

**I have a computer that is quite old, should I upgrade?**

2.0 does require significantly more resources than v1.2. Therefore if your 
computer does not have much memory you may find 2.0 will struggle, `especially` 
when changing between slides.

**Why can I not see my 1.2 songs, bibles and themes in 2.0?**

This is an beta release, which means it is not finished and one of the things we 
haven't completely finished yet is importing 1.2 data automatically. We plan to 
do this [[Version_2_Milestones#Version_1.9.6_.28beta_2.29|Version 1.9.6 (beta 2)]].

**How do I transfer my 1.2 song database?**

In OpenLP v2, go to the :menuselection:`File --> Import --> Song` menu.
In the Wizard that appears, click Next and choose "openlp.org v1.x" from the 
Format list. Click the search button on the Filename prompt, and at the bottom 
of the dialog, copy the following into the File name prompt::

  %ALLUSERSPROFILE%\Application Data\openlp.org\Data\songs.olp

`(This must be in the popup file chooser dialog. Don't enter it directly into 
the wizard).`

Click Open, then in the wizard just click Next and wait for the import to complete.

**How do I transfer my 1.2 Bibles?**

In OpenLP v2, go to the :menuselection:`File --> Import --> Bible` menu.
In the Wizard that appears, click Next and choose "openlp.org v1.x" from the 
Format list.
Click the search button on the Filename prompt, and at the bottom of the dialog, 
copy the following into the File name prompt::

  %ALLUSERSPROFILE%\Application Data\openlp.org\Data\Bibles

`(This must be in the popup file chooser dialog. Don't enter it directly into 
the wizard).`

Choose the Bible, Click Open, then in the wizard just click Next, enter the 
License details, and wait for the import to complete.

**How do I transfer my 1.2 Themes?**

In openlp.org v1, export each theme by selecting it in the Theme Manager, and 
then clicking the picture of a blue folder with red arrow on the Theme Managers 
toolbox. This theme file can then be imported into V2 using the 
:menuselection:`File --> Import --> Theme` menu.

**I can't get my 2.0 theme to look the same as 1.2**

OpenLP 2.0 is a complete rewrite using a completely different programming 
language so it would work on different types of system. There are differences in 
how the old and new languages draw text on the screen, and therefore it is 
unlikely you'll get an exact match.

Using OpenLP
^^^^^^^^^^^^

**Is there a manual or any documentation for 2.0?**

Some folks are working on a brand new manual for OpenLP 2.0. You can find the 
latest version of this manual at http://manual.openlp.org. If you need help, 
use the live chat feature or ask in the forums. If you would like to help write 
the manual, please let us know - we are always happy for new volunteers to join 
the team and contribute to the project.

**I've started OpenLP, but I can't see the songs or bibles section in the Media Manager**

When you installed OpenLP, the first time wizard would have asked which plugins 
you wanted, and songs and bibles should have been selected. If for some reason 
they were not, then you will need to activate them yourself. See 
[[#How do I activate / deactivate a plugin?|How do I activate / deactivate a plugin]] 
for instructions.

**How do I activate / deactivate a plugin?**

Plugins can be turned on and off from the Plugin List Screen. Select the plugin 
you wish to start/stop and change it's status. You should not need to restart 
OpenLP.

**What are these plugins that I keep seeing mentioned?**

The plugins allow OpenLP to be extend easily.  A number have been written 
(Songs, Bibles, Presentations) etc but it is possible for the application to be 
extended with functionality only you require.  If this is the case then go for 
it but lets us know as we can help and it may be something someone else wants.

**How do I enable PowerPoint/Impress/PowerPoint Viewer?**

First of all ensure that the presentation plugin is enabled (see above).
Then to enable a presentation application, go to the `Settings` dialog, switch 
to the `Presentations` tab and check one of the enabled checkboxes. OpenLP will 
automatically detect which of the three you have installed, and enable the 
appropriate checkbox(es). Check the applications you require, and then restart 
OpenLP for the change to be detected. 
Note, PowerPoint Viewer 2010 is not yet supported, use 2003 or 2007.

See also [[OpenLP_2_Introduction_and_FAQ#I.27m_on_Windows_and_PowerPoint_is_
installed.2C_but_it_doesn.27t_appear_as_an_option|I'm on Windows and PowerPoint 
is installed, but it doesn't appear as an option]]
and [[#Why_is_there_no_presentations_plugin_available_on_OS_X.3F|Why is there no 
presentations plugin available on OS X?]]

**Why is there no presentations plugin available on OS X?**

Currently the presentations plugin is not bundled with OpenLP on OS X. The 
reason for that is that the OpenOffice.org version on Mac OS X does not contain 
the (more exact: does only contain a broken) interoperability component (the so 
called pyuno bridge) which could be used by OpenLP. As soon as the 
interoperability component works on OS X we can re-enable the plugin and bundle 
it. We are really sorry for that.

**Is it possible to get Bible x? How?**

The Bible plugin has a much improved `Import Wizard` which can import Bibles 
from a variety of sources. The following sources are supported:

* CSV (in the same format as `openlp.org 1.x <http://www.openlp.org/en/documentation/importing_exporting_data/bibles/importing_comma_delimited_files.html>`_)

* OSIS (export from the `Sword Project <http://www.crosswire.org/sword/software/>`_ using the mod2osis tool)

 * After using the Sword software Media Manager to download the required bible.

 * From the command line (works on Windows and Linux):<br /><code>modernist <name>  > name.osis</code><br />`Note the <name> is case sensitive on all environments and should be the name of your bible, e.g. ESV.`

 * The Bible import wizard will the read name.osis file and import your bible.

* OpenSong

 * OpenSong have a good selection of Bibles on their `download page <http://www.opensong.org/d/downloads#bible_translations>`_

* Web Download 

 * `Crosswalk <http://biblestudy.crosswalk.com/bibles/>`_

 * `BibleGateway <http://www.biblegateway.com/versions/>`_

**Why do my Bible verses take a long time to load?**

In order to better conform to copyright law, the Web Download Bibles are not 
downloaded when you import them, but on the fly as you search for them. As a 
result, the search takes a little longer if you need to download those 
particular verses. Having said that, the Web Download Bibles cache downloaded 
verses so that you don't need to download them again.

**My Bible is on the Web Download sites, but my Church isn't on the internet. 
What options do I have?**

When you create and save a service, all the items in the service are saved with 
it. That means any images, presentations, songs and media items are saved. This 
is also true for bibles. What this means is you can create the service on your 
home computer, insert a bible passage from the web, save it and then open the 
service using your church computer and voila, the bible passage should be there! 
Note this can also be done with songs, etc!

(Advanced) Where do I find the configuration file?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Linux, FreeBSD & PC-BSD**

If your distribution supports the XDG standard, you'll find OpenLP's 
configuration file in::

 /home/<user>/.config/OpenLP/OpenLP.conf

If that file and/or directory does not exist, look for::

 /home/<user>/.openlp/openlp.conf

**OS X**

You'll find your configuration file here::

 /Users/<user>/Library/Preferences/com.openlp.OpenLP.plist
 /Users/<user>/Library/Preferences/org.openlp.OpenLP.plist

**Windows**

On Windows, OpenLP does not use a configuration file, it uses the Windows 
registry. You can find the settings here::

 HKEY_CURRENT_USER\Software\OpenLP\OpenLP

Troubleshooting
^^^^^^^^^^^^^^^

**Something has gone wrong, what should I do to help get it fixed?**

If you have found an error in the program (what we call a bug) you should report 
this to us so that OpenLP can be improved. Before reporting any bugs please 
first make sure that there isn't already a bug report about your problem:

#. Check the `Launchpad bug list <https://bugs.launchpad.net/openlp>`_
#. `OpenLP support System <http://www.support.openlp.org/projects/openlp>`_
#. Check the `bug reports <http://openlp.org/en/forums/openlp_20/bug_reports.html>`_ forum

If there **is already a bug report**, you may be able to help by providing 
further information. However, **if no one else has reported** it yet, then 
please post a new bug report.

#. The **preferred place** for reporting bugs is the `bugs list <https://bugs.launchpad.net/openlp>`_ on Launchpad.
#. Alternatively, if you don't have a Launchpad account and don't want to sign up for one, you can post in the `bug reports forum <http://openlp.org/en/forums/openlp_20/bug_reports.html>`_.
#. If none of these ways suits you, you can send an email to bugs (at) openlp.org.

What information should I include in a bug report?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Operating System
 
 * Version
 * Distribution - Ubuntu, Fedora, etc (if you're using Linux)
 * Edition \- Home, Basic, Business, etc (if you're using Windows)

* Version of OpenLP (:menuselection:`Help --> About`)
* The exact steps to take in order to reproduce the error
* Version of MS Office or OpenOffice (if you're using the song imports or the presentation plugin)
* What Bible translation and type you are importing (if you're using the Bible importer)
* `Any` other information that might remotely be related or useful.

The more information you give us, the better we can help you.

**I've been asked to email a debug log, where do I find this?**

We may need a debug log to help pin-point the issue. A new log file is created 
each time you start OpenLP so copy the file before you run the software a second 
time. On Windows a Debug option is available in the start menu. On other systems, 
you will need to run OpenLP from the command line, with the following 
option: <code>-l debug</code>. Please note, that is a lowercase **L**.

If you haven't been given a specific email address to send it to, then please do 
not paste the log contents straight into a forum post. Instead, open the log 
file in a text editor (such as notepad on Windows) and copy and paste the 
contents into somewhere like `pastebin.com <http://pastebin.com>`_. Then give us 
the link to the page that is created.

**Windows**

Find the OpenLP 2.0 folder in your Start menu. Choose the "OpenLP (Debug)" option.

OpenLP will start up. Go to the :menuselection:`Tools --> Open Data Folder` menu 
option, and an Explorer window will appear containing folders such as alerts, 
bibles, custom etc. Keep this Explorer window open.

Now repeat the steps you need to take in OpenLP to reproduce the problem you had, 
and then close down OpenLP. 

In the Explorer window you left open, navigate up one level into the openlp 
folder. You will see the <code>openlp.log</code> file. This is the file to e-mail.

**Linux**

If you installed OpenLP from a package::

 @:~$ openlp -l debug

Alternately, if you're running OpenLP from source::

 @:~$ ./openlp.pyw -l debug

If your Linux distribution supports the XDG standard, you'll find the log in::

 ~/.cache/openlp/openlp.log

Otherwise, you'll find the log file in::

 ~/.openlp/openlp.log

**Mac OS X**

Open Terminal.app and navigate to where you installed OpenLP, usually 
<code>/Applications</code>::

 @:~$ cd /Applications

Then go into the OpenLP.app directory, down to the OpenLP executable::

 @:~$ cd OpenLP.app/Contents/MacOS

And then run OpenLP in debug mode::

 @:~$ ./openlp -l debug

Once you've done that, you need to get the log file. In your home directory, 
open the Library directory, and the Application Support directory within that. 
Then open the openlp directory, and you should find the openlp.log file in that 
directory::

 /Users/<username>/Library/Application Support/openlp/openlp.log

**I'm on Windows and PowerPoint is installed, but it doesn't appear as an 
option**

Try installing the `Visual C++ Runtime Redistributable <http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en>`_.

**The command line shows many error messages**

When running OpenLP from the command line, you might get something like this::

 Logging to: /home/<User>/.config/openlp/openlp.log

* WARNING: bool Phonon::FactoryPrivate::createBackend() phonon backend plugin could not be loaded 
* WARNING: bool Phonon::FactoryPrivate::createBackend() phonon backend plugin could not be loaded 
* WARNING: Phonon::createPath: Cannot connect  Phonon::MediaObject ( no objectName ) to  VideoDisplay ( no objectName ). 
* WARNING: Phonon::createPath: Cannot connect  Phonon::MediaObject ( no objectName ) to  Phonon::AudioOutput ( no objectName ). 
* WARNING: bool Phonon::FactoryPrivate::createBackend() phonon backend plugin could not be loaded

These error messages indicate that you need to install an appropriate backend 
for Phonon.

**Linux/FreeBSD**

If you're using Gnome, you need to install the GStreamer backend for Phonon. On 
Ubuntu you would install the <code>phonon-backend-gstreamer</code> package::

 @:~$ sudo aptitude install phonon-backend-gstreamer

If you're using KDE, you need to install the Xine backend for Phonon. On Kubuntu 
you would install the <code>phonon-backend-xine</code> package::

 @:~$ sudo aptitude install phonon-backend-xine

If you know which audiovisual system you're using, then install the appropriate 
backend.

phonon-backend-vlc may also be worth trying on some systems.

**Windows & Mac OS X**

Phonon should already be set up properly. If you're still having issues, let the 
developers know.

**I've upgraded from 1.9.2 to a newer version, and now OpenLP crashes at start**

You need to upgrade your song database.
See this `blog post <http://openlp.org/en/users/jt/blog/2010-07-20-flag_day_database_schema_changes_in_trunk_revision_956.html>`_ for information on how to do this.

**I've upgraded to 1.9.5, and now OpenLP has duplicates of many songs in the Media Manager**

You need to run the :menuselection:`Tools --> Re-index Songs`.

**There are no menu icons in OpenLP**

This may affect (only) linux users with xfce. To solve the problem, follow the 
description `here <https://bugs.launchpad.net/ubuntu/+source/qt4-x11/+bug/501468/comments/3>`_.

**JPG images don't work**

This is a known issue on some Mac OS X 10.5 systems, and has also been seen on 
Windows XP too. The solution is to convert the image into another format such as 
PNG.

**MP3's and other audio formats don't work**

This is a known issue on some systems, including some XP machines, and we have 
no solution at the moment.

**Videos can be slow or pixelated. Background Videos are very slow**

If playing video by themselves, try selecting the 
:menuselection:`Settings --> Configure OpenLP --> Media`, Use Phonon for Video 
playback option. As for text over video, we have no solution for speeding these 
up. Reducing the monitor resolution and avoiding shadows and outline text will 
help. We are hoping a future release of the toolkit we are using (QtWebKit) will 
help improve this, but there is no timeframe at present.

Features
^^^^^^^^

**What new features will I find in v2?**

Since v2 was a rewrite from the ground up, you won't find a great deal of new 
features since initially we want to ensure all the v1.2 features are included. 
However the developers have managed to sneak a few in. Take a look at the 
[[Version 2 Features|Complete list]].

**Why hasn't popular feature request X been implemented?**

We made a decision to first implement v1.2 features, before going wild on new 
features. There are only a handful of developers working in their spare time. If 
we were to try and include everything we wanted to implement, then v2 would not 
likely ever get released.

**I have a great idea for a new feature, where should I suggest it?**

First of all check it isn't on the [[Feature Requests|Feature Requests]] page. 
If it is, then you need to say no more, it's already been suggested! If it isn't 
on the list, then head to the `feature request forum <http://openlp.org/en/forums/openlp_20/feature_requests.html>`_ 
and post the idea there.

`Help <http://wiki.openlp.org/Help:Contents>`_