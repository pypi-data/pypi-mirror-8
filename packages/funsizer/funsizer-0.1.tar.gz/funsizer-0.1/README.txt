funsizer
========
funsizer is the client side for funsize project ( https://wiki.mozilla.org/ReleaseEngineering/Funsize )
It aims to automate the triggering and the retrieval of the partial MAR files.

Installation
============
Run `python setup.py install` to install the script as command-line tool.

Usage
=====
Run `funsizer.py -u *URL* -a *auth file* -b *branch name* *path to file*` to upload a file to the blobber server at *URL*.
Run `funsizer.py [--timeout T]
                 [--window-timeout wT]
                 [--server-url URL]
                 --from-url from-URL
                 --to-url to-URL
                 --from-has from-HASH
                 --to-has to-HASH
                 --channel CHANNEL
                 --version VERSION
                 --output OUTPUT
Where
=> T is timeout (in seconds) to wait for results
=> window-timeout is windows timeout sleep between client-to-server calls
=> server-url is the host where to send the files (defaults to localhost)
=> from-url is the complete mar url for `from` version'
=> to-url is the complete mar url for `to` version'
=> from-hash is the hash for `from` version mar'
=> to-hash is the hash for `to` version mar'
=> channel is the channel for the requested partial mar'
=> version is the version of the latter mar'
=> output is the file where to write the resulted partial mar'
