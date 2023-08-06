gdrive_sync
************

Synchronize directories between Google Drive and your local machine. 
You can choose to synchronize only selected directories as opposed
to other tools where you need to keep all files on your Google Drive
in the same directory on your local computer in order for the 
synchronization to work.

The intended use is to backup directories from multiple locations on
your own machine, each to its own separate directory on Google Drive.

How it works
------------

The ``gdrive_sync`` program  will first download all changes that have 
happened on your Drive since it was first created. The first synchronization
will take equally long if you have one file with 1000 separate changes or
1000 files you have uploaded and not changed afterwards.

After the initial download of your change history ``gdrive_sync`` only
needs to download the changes that have occurred since the last time
you used the program. This is normally very fast.

After downloading the change history you can get a list of differences
between your backup on Google Drive and your local files. You can 
``sync-up`` to upload whatever changes you have made and new files added.

There is no ``sync-down`` functionality at the moment since the author of
this program has not needed that yet. It may be implemented later. Feel
free to submit a patch / pull request if you are tired of waiting for some
easy-to-implement feature and decide to write it yourself.

Installing
----------

The gdrive_sync program and underlying libraries are written in Python. 
The program is tested on Python 2.7.3 on Ubuntu Linux and Python 2.7.2
on Windows 7. The code is written so that it should work on Mac OS also,
but this has not been tested. Compatibility with Python 2.6 has not been
tested, it probably works with a few "from __future__ import ..." statements.

You can use the normal Python package managers, for example the
`pip <http://www.pip-installer.org>`_ tool, to install the program.
You do not need root or administrator access if you install inside a Python
`virtualenv <http://www.virtualenv.org/>`_.

  pip install gdrive_sync

You can run either the supplied gdrive_sync executable script or run the Python
package directly from a Python executable that has ``gdrive_sync`` on the import
path::

  gdrive_sync
  # or
  python -m gdrive_sync

Usage
-----
 
First time you first need to update the local database with all changes to your 
Drive up to now::
 
  gdrive_sync update
  
You can then for example sync your pictures to the Pictures directory on Google
Drive with your picture collection on /media/my_disk/Images. First see 
differences between the local and remote directory::
 
  gdrive_sync diff Pictures /media/my_disk/Images
  
The ``gdrive_sync`` command always expects the Google Drive directory name first
and then the local directory as argument number two. You can skip both, the
default is to synchronize the whole of your Drive ("/") with the local directory
(".")::
  
   cd Drive
   gdrive_sync diff
   gdrive_sync sync-up
   
And now you also know how to upload any changes :-)

The ``sync-up`` command will always run ``update``, then ``diff`` before it asks you if
you would like to continue. You can continue automatically with the ``-y`` switch to 
``sync-up`` and you must explicitly allow deleting (putting in Google Drive trash) files
or folders with the ``-x`` switch. You can "dry-run" without actually doing anything to
the remote Drive with the ``-d`` switch.
  
Limitations
-----------
  
1)  The program assumes that your Drive is a DAG (directed acyclic graph), where
    each file and directory is present in one and only one directory. This is
    normally the case. UPDATE: this is (mostly?) fixed in version 0.6    
     
2)  The program can currently only upload (``sync-up``), not download (``sync-down``). (1)

3)  The program is tested briefly and appears to work, but it might eat your files and
    I take no responsibility  for that. That being said it is just the ``sync-up`` 
    command that actually changes anything on your drive, the other commands are
    read-only. The ``diff`` command does not even connect to Google Drive at all.
    No files will ever be deleted (just put in trash), but files will be overwritten
    if the program detects that the file has changed.

 1: If I ever have use for that functionality I will implement it. It should be
 quite simple.
 
Development
-----------

Development happens at https://bitbucket.org/trlandet/gdrive_sync. There is only one main
development branch and no stable branch. For the code style PEP8 is followed, except for
the strict 80 characters line length requirement. 

Feel free to submit patches / pull requests as long as you feel comfortable with licensing
your code under the same three licenses as gdrive_sync (see License below). Simple five line
fixes to make the code run on Python 2.6 are appreciated, huge changes to make it run on
Python 2.3 are perhaps less so. I will seriously consider support for Python 3.3 if it is not
very invasive.

Version history
---------------

2014-11-10 - version 0.6
~~~~~~~~~~~~~~~~~~~~~~~~

Better support for real world drives and data. Huge thanks to Philipp Dreimann for most of the code!

- Changes by Philipp Dreimann to support multiple roots (non-DAG drive layouts) which are common for some reason
- Changes by Philipp Dreimann to use a much smarter MIME type selection
- Support excluding paths based on regular expressions
- Bugfixes for various problems when starting the program for the first time

2013-03-21 - version 0.5
~~~~~~~~~~~~~~~~~~~~~~~~

Initial semi-working release

- Can download list of changes and store the current state of the Google Drive
- Can find differences between local and remote Drive
- Can upload any missing files to the remote Drive
- Can delete (put in trash) files or folders on the remote drive

The program will still output some debug trash on the command line and will crash
with a stack traces every so often. I still use it for my backup, so it kind of
works... YMMV

License
-------

The code is copyright 2013 Tormod Landet and is released under the BSD (3 clause)/Python (PSFL)/GPL (2+) license
