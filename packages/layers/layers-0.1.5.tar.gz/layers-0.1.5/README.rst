

Layers
--------------

Layers is small utility for software developers that use aufs to merge several layers project into one.

.. note::
    Project is in alpha-dev stage. Contributions, testing, feedback are really welcome.

Why?
====================

Layers allow to apply DRY principle to your project by merging several folders into one. Every software
project has some files that are copied from project to project without modification.

Examples:

    - configuration files for your development stack
    - .gitignore files
    - directory structure
    - ... more samples?


Usually this files are copied once, and it's big work to update them all after.


Aufs to help
===================

Aufs is layered filesystem that allows to merge several directories into one, and keep them writable.
Layers utility use aufs, to compose layers automatically.


Installation
===================


You need linux (not tested on other OSes yet) with aufs-tools installed, python-pip is also needed.
Usually you have all those if you ever use Docker, if not then google how to install this tools.

Install Layers::

    sudo pip install layers

As mount command against curent directory is not possible (shows "directory busy" error), add alias for layers
command to execute it from parent dir, and then get you back in project directory. Execute in shell::

    echo "layers() { LPD=\$PWD; cd ..; layers-util \$LPD \$@; cd \$LPD; }" >> ~/.bashrc
    source ~/.bashrc

This will update your .bashrc automatically.


Quick start
===================


Let's prepare example directory structure::

    mkdir project1
    mkdir some-layer
    mkdir another

project1 - is our project directory. Another too are layers.
We will put some data into "some-layer" and another::

    echo "*.pyc" > some-layer/.gitignore
    echo "Empty yet" > some-layer/README.txt

    echo "John Doe (c) 2076 year" > another/AUTHOR.txt

Now create layers.yml file in your project1 directory, like this::

    layers:

      every-python-project-should-have-this:
        path: ../some-layer

      just-my-ego:
        path: ../another

Now, lets mount this::

    cd project1
    layers mount

Now, ls should show the following::

    ls project1

    AUTHOR.txt  layers.yml  README.txt


Working with layers
=========================

If you make any changes in project1 directory, all changes will be recorded only on this layer,
so, if we change project1/README.txt, it will not affect "some-layer"::

    $ cat project1/README.txt

    Empty yet

    $ echo "This is project readme" > project1/README.txt

    $ cat project1/README.txt

    This is project readme

    $ cat some-layer/README.txt

    Empty yet

But if you modify layers, changes are reflected::

    $ echo ".more-to-ignore" >> some-layer/.gitignore

    $ cat project1/.gitignore

    *.pyc
    .more-to-ignore


Auto-create mount-points
==========================

layers.yml have one interesting option that allow to create mount point before it mounted.
For example it can be checked out from git::


    layers:

      mfcloud-python:
        path: ../python-django
        create: git clone git@bitbucket.org:ribozz/python-django.git


Syntax here is::

    create: {any valid bash command}


This may allow you to bootstrap your projects very quickly::

    $ git clone my-repo-url-here my-project
    $ cd my-project
    $ layers mount


And magically all your layers are checked out and mounted.



Mount to different directory
==============================

"to" allows to mount to sub-directories::

    layers:

      cratis:
        path: ../cratis
        create: git clone git@bitbucket.org:itpeople/cratis.git
        to: lib/cratis

      cratis-features:
        path: ../cratis-features
        create: git clone git@bitbucket.org:itpeople/cratis-features.git
        to: lib/cratis-features

      mfcloud-python:
        path: ../python-django
        create: git clone git@bitbucket.org:ribozz/python-django.git



Command reference
======================

layers mount
*****************

Syntax:

    layers mount

Mounts all layers referred in layers.yml


layers umount
*****************

Syntax:

    layers umount

Unmounts all layers from current directory


layers commands
*****************

Syntax:

    layers {some commmand}

chdir into every directory specified in layers.yml, and execute command.
Example::

    $ layers ls -la

    Layer /home/alex/dev/example/project1

    total 24
    drwxrwxr-x 8 alex alex 4096 sept  30 14:43 .
    drwxrwxr-x 5 alex alex 4096 sept  30 13:59 ..
    -rw-rw-r-- 1 alex alex   23 sept  30 14:04 AUTHOR.txt
    -rw-rw-r-- 1 alex alex   22 sept  30 14:46 .gitignore
    -rw-rw-r-- 1 alex alex  113 sept  30 14:05 layers.yml
    -rw-rw-r-- 1 alex alex   23 sept  30 14:43 README.txt

    Layer /home/alex/dev/example/some-layer

    total 24
    drwxrwxr-x 4 alex alex 4096 sept  30 14:06 .
    drwxrwxr-x 5 alex alex 4096 sept  30 13:59 ..
    -rw-rw-r-- 1 alex alex   22 sept  30 14:46 .gitignore
    -rw-rw-r-- 1 alex alex   10 sept  30 14:42 README.txt
    -r--r--r-- 1 root root    0 sept  30 14:06 .wh..wh.aufs
    drwx------ 2 root root 4096 sept  30 14:06 .wh..wh.orph
    drwx------ 2 root root 4096 sept  30 14:06 .wh..wh.plnk

    Layer /home/alex/dev/example/another

    total 20
    drwxrwxr-x 4 alex alex 4096 sept  30 14:06 .
    drwxrwxr-x 5 alex alex 4096 sept  30 13:59 ..
    -rw-rw-r-- 1 alex alex   23 sept  30 14:04 AUTHOR.txt
    -r--r--r-- 1 root root    0 sept  30 14:06 .wh..wh.aufs
    drwx------ 2 root root 4096 sept  30 14:06 .wh..wh.orph
    drwx------ 2 root root 4096 sept  30 14:06 .wh..wh.plnk


Another useful command is::

    layers git status

Licence
======================

Apache licecne. See LICENCE for details

Changelog
======================


----------------------

0.1.5

- Improved handling of sub-mounts (to: ). (Alex.R.)

----------------------

0.1.4

- Fix installation pocess in setup.py. (Alex. R.)
- Improved sh script, made it more user-friendly. Added instructions to README how to pudate bashrc (Alex.R.)

----------------------

0.1.3

Added "to" to layers.yml (Alex R.)

---------------------






