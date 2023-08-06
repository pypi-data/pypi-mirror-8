#JOTTA CLOUD CLIENT#

A cli friendly sync client for [JottaCloud](http://jottacloud.com).

It will sync your directory tree with JottaCloud, just like the official client.

**Note. This a third-party, not an official client.s**

##How to use it##

Run `jottacloudclientscanner.py` at some interval:

    python jottacloudclientscanner.py <top dir of your local tree> <the mount point on jottacloud>


The program expects to find `JOTTACLOUD_USERNAME` AND `JOTTACLOUD_PASSWORD` as variables in the running environment. So you might want to do

    export JOTTACLOUD_USERNAME=<username> JOTTACLOUD_PASSWORD=<password>

#But it's not finished!#
#But it's not very advanced!#
#Geez, you should've added *super bright idea* already!#

Want to help out? Read the HACKING document and get cracking!

Send pull requests to https://gitorious.org/jottafs/jottabox/ or patches to havard@gulldahl.no
