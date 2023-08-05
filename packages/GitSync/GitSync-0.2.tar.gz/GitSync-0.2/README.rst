=======
GitSync
=======

This tool allows a developer to work on files on their local machine and have their work synced on a remote system. It uses git to manage the syncing process.

The use case that inspired this tool is web development where the development environment is a remote server. Many of the most useful development tools require (or at least work a lot better) in low latency environments. Since you local file system is about as low latency as it gets there's really where you want to do your work. However if you actually want to run your application you need your code to be on a remote system, this presents a problem. Especially if you do not have a screaming fast connection between your local machine and the remote one.

This tool takes the syncing of your local file system and the remote system "out of band" so there are fewer interruptions.

This tool relies heavily on the git version control system. Before you try to use it I would recommend getting a basic understanding of how git works. This tool should take care of most (if not all) of the work but if you want take advantage of its full power you will need to understand how git works. Here are some places to get started:

 - Git Home http://git-scm.com/

 - Git Tutorial http://www.ralfebert.de/tutorials/git/

 - Understanding Git Conceptually http://www.eecs.harvard.edu/~cduan/technical/git/


OS X Dependencies
=================

Skip any steps that install software you already have.

#. Install the Xcode and the command line tools.
   https://duckduckgo.com/?q=OS+X+xcode+command+line+tools

#. Install Homebrew
   http://mxcl.github.io/homebrew/

#. Install git

   ``brew install git``

#. Install python

   ``brew install python``

#. Install terminal-notifier.

   ``brew install terminal-notifier``

#. Install pip

   ``easy_install pip``

#. Install GitSync

   ``pip install GitSync``

#. Manually install the latest version of pync. If you get errors complaining
   about pync not being properly installed you should manually install the
   latest version from here.
   https://github.com/SeTeM/pync


Remote Dependencies
===================

The Remote system needs to be setup with the following things.

#. SSH access.

#. SSH Keys to allow authentication with having to put in passwords.

#. Git needs to be installed.


Configuration
=============

The assumption git sync makes (right now) is that the latest version of your stuff is on the remote system.

On the first sync it will assume the location on the local file system is empty and the first thing it needs to do is pull down the files from the remote system.

#. Copy the example configuration file (examples/git_sync.yaml) giving it an appropriate name.

#. Set all the values in the config file.
   - local_path: This is the path on your local machine where you want your files to go.
   - local_branch_name: The name of the git branch you want git sync to use.
   - remote_host: The IP or domain name of the remote system you want to use.
   - remote_user: Your username on the remote system
   - remote_path: The path on the remote system with the files in it you want to sync with.
   - git_ignore: A list of patterns you want git to ignore, in this context that means these are files that will not get synced.

Current Git Users: Caution
==========================

If you are already using git for version control, be careful. This has been take
into account (somewhat) but has not really been tested yet. In the future we
would like to fully support that.


Running git_sync.py
===================

In Terminal run the following command::

  git_sync path/to/your/config/file.yaml

It should do some setup work. This could take a lot time if this is the initial sync, if there are a lot of changes or if the network connection is slow.

Once it's done start working. Open files. Save files. Create files. Every time you do something that results in a file system event you should see a growl notification that git sync has started and shortly after another one that it is finished.

Once the sync in finished, check on the server, and the changes should have been synced.

License
=======

- [LICENSE](LICENSE) ([MIT License][MIT])

[MIT]: http://opensource.org/licenses/MIT "The MIT License (MIT)"
