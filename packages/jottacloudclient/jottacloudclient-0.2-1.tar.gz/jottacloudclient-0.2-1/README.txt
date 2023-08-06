JOTTA CLOUD CLIENT
==================

A cli friendly sync client for `JottaCloud <http://jottacloud.com>`__.

It will sync your directory tree with JottaCloud, just like the official
client.

**Note. This a third-party, not an official client.**

Is it safe?
-----------

Being based on a reverse engineering of the protocol, things may break
in unexpected ways. Don't rely on this as your sole backup unless you
manually verify that the data is correctly transferred.

How to use it
-------------

Run ``jottacloudclientscanner.py`` at some interval:

::

    python jottacloudclientscanner.py <top dir of your local tree> <the mount point on jottacloud>

The program needs to know your password to JottaCloud. There are two
ways to do this.

.netrc
~~~~~~

Create a ``$HOME/.netrc`` file with this entry:

::

    machine jottacloud
            login <yourusername>
            password <yourpassword>

Make sure noone else can see it: ``chmod 0600 $HOME/.netrc``.

environment variables
~~~~~~~~~~~~~~~~~~~~~

Add ``JOTTACLOUD_USERNAME`` AND ``JOTTACLOUD_PASSWORD`` as variables in
the running environment:

::

    export JOTTACLOUD_USERNAME=<username> JOTTACLOUD_PASSWORD=<password>

But it's not finished!
======================

But it's not very advanced!
===========================

Geez, you should've added *super bright idea* already!
======================================================

Want to help out? Read the HACKING document and get cracking!

Send pull requests to https://gitorious.org/jottafs/jottacloudclient/ or
patches to havard@gulldahl.no
