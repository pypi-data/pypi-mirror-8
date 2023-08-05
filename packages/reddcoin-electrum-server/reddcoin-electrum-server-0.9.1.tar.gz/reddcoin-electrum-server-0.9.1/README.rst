Official Reddcoin Electrum Server
---------------------------------

-  Licence: GNU GPL v3
-  Author: Thomas Voegtlin (ThomasV on the bitcointalk forum)
-  Author: Larry Ren (laudney) forked for Reddcoin
-  Language: Python
-  Homepage: https://wallet.reddcoin.com

Features
--------

-  The server indexes UTXOs by address, in a Patricia tree structure
   described by Alan Reiner (see the 'ultimate blockchain compression'
   thread in the Bitcointalk forum)

-  The server requires reddcoind, leveldb and plyvel

-  The server code is open source. Anyone can run a server, removing
   single points of failure concerns.

-  The server knows which set of Reddcoin addresses belong to the same
   wallet, which might raise concerns about anonymity. However, it
   should be possible to write clients capable of using several servers.

Installation
------------

1. To install and run a server, see INSTALL. For greater detail on the
   installation process, see HOWTO.md.

2. To start and stop the server, use the 'electrum-server' script

License
-------

Source code is made available under the terms of the `GNU Affero General
Public License <http://www.gnu.org/licenses/agpl.html>`__, version 3.
See the included ``LICENSE`` for more details.
