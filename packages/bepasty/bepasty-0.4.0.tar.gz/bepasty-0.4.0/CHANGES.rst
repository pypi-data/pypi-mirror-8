ChangeLog
=========


Release 0.4.0
-------------

New features:

* shorter, easy-to-read URLs / filenames (old uuid4 style URLs still supported,
  but not generated any more for new items)
* "list" permission separated from "admin" permission.

  - list: be able to list (discover) all pastebins
  - admin: be able to lock/unlock files, do actions even if upload is not
    completed or item is locked

  Make sure you update your PERMISSIONS configuration (you likely want to give
  "list" to the site administrator).

  By giving "list" (and/or "delete") permission to more users, you could
  operate your bepasty site in a rather public way (users seeing stuff from
  other users, maybe even being able to delete stuff they see).

Fixes:

* give configured limits to JS also, so stuff has not to be kept in sync manually, fixes #109
* highlighted text file views: set fixed width to line number column, fixes #108
* fixed crash for inline and download views when item was already deleted

Other changes:

* support Python 3.3+ additionally to 2.6+
* improved documentation, esp. about REST api
* improve sample configs


Release 0.3.0
-------------

New features:

* support http basic auth header (it just reads the password from there, the
  user name is ignored). this is useful for scripting, e.g. you can do now:
  $ curl -F 'file=@somefile;type=text/plain' http://user:password@localhost:5000/+upload
* you can give the filename for the list items now
* do not use paste.txt as default filename, but <uuid>.txt or <uuid>.bin
  (this is less pretty, but avoids collisions if you download multiple files)
* allow uploading of multiple files via the fileselector of the browser
* display download (view) timestamp
* sorting of file lists
* use iso-8859-1 if decoding with utf-8 fails
* let admin directly delete locked files, without having to unlock first
* new bepasty-object cli command
* added REST api for bepasty-client-cli
* MAX_RENDER_SIZE can be used to set up maximum sizes for items of misc. types,
  so bepasty e.g. won't try to render a 1 GB text file with highlighting.
* offer a "max. lifetime" when creating a pastebin
* if you link to some specific text line, it will highlight that line now
* add filename to the pastebin url (as anchor)

Removed features:

* removed ceph-storage implementation due to bugs, missing features and general
  lack of maintenance. it is still in the repo in branch ceph-storage, waiting
  to be merged back after these issues have been fixed:
  https://github.com/bepasty/bepasty-server/issues/13
  https://github.com/bepasty/bepasty-server/issues/38

Fixes:

* security fix: when showing potentially dangerous text/* types, force the
  content-type to be text/plain and also turn the browser's sniffer off.
* security fix: prevent disclosure of locked item's metadata
* use POST for delete/lock actions
* application/x-pdf content-type items are offer for in-browser rendering, too
* fix typo in cli command bepasty-object set --incomplete (not: uncomplete)
* quite some UI / UX and other bug fixes
* filesystem storage: check if the configured directory is actually writeable

Other changes:

* using xstatic packages now for all 3rd party static files
* docs updated / enhanced


No release 0.2.0
----------------

We made quite quick progress due to many contributions from EuroPython 2014
sprint participants, so there was no 0.2.0 release and we directly jumped to
0.3.0.


Release 0.1.0
-------------

New features:

* add a textarea so one now actually can paste (not just upload)
* simple login/logout and permissions system - see PERMISSIONS in config.py.
* add lock/unlock functionality to web UI (admin)
* add "List all items" on web UI (admin)
* add link to online documentation
* support inline viewing of PDFs
* support Python 2.6
* after upload of multiple files, offer creation of list item
* file uploads can be aborted (partially uploaded file will get deleted)
* store upload timestamp into metadata
* Compute hash of chunked uploads in a background thread directly after upload
  has finished.
* new migrate cli subcommand to upgrade stored metadata (see --help for details)
* new purge cli subcommand (see --help for details).
  you can use this to purge by age (since upload), inactivity (since last
  download), size or (mime)type.
  BEWARE: giving no criteria (like age, size, ...) means: purge all.
  Giving multiple criteria means they all must apply for files to get
  purged (AND - if you need OR, just run the command multiple times).
* new consistency cli subcommand (see --help for details).
  you can check consistency of hash/size in metadata against what you have
  in storage. Optionally, you can compute hashes (if an empty hash was stored)
  or fix the metadata with the computed hash/size values.
  also, you can remove files with inconsistent hash / size.

Fixes:

* for chunked upload, a wrong hash was computed. Fixed.
* misc. cosmetic UI fixes / misc. minor bug fixes
* add project docs
* use monospace font for textarea
* now correctly positions to linenumber anchors


Release 0.0.1
-------------

* first pypi release. release early, release often! :)
