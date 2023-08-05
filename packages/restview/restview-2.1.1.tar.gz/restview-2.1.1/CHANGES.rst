Changelog
=========

2.1.1 (2014-09-28)
------------------

- Fix TypeError on Python 3 when reporting ReST errors (typically in strict
  mode).
  Fixes https://github.com/mgedmin/restview/issues/21.

- Fix TypeError on Python 3 when using ``--pypi-strict``.


2.1.0 (2014-09-02)
------------------

- ``--pypi-strict`` mode to catch additional problems that break rendering
  on the Python Packaging Index.  ``--long-description`` enables this
  automatically.
  Fixes https://github.com/mgedmin/restview/issues/18.

- Added installation section to the README.
  Fixes https://github.com/mgedmin/restview/issues/19.


2.0.5 (2014-06-09)
------------------

- Avoid Unicode errors on Python 3 when the ReStructuredText file is in an
  encoding that doesn't match the locale.
  Fixes https://github.com/mgedmin/restview/issues/16.

- Avoid Unicode errors on Python 3when there are filenames in an encoding that
  doesn't match the locale.
  Fixes https://github.com/mgedmin/restview/issues/17.


2.0.4 (2014-04-28)
------------------

- Show a clear error when external command fails.
  Fixes https://github.com/mgedmin/restview/issues/14.

- Stop mangling document titles.
  Fixes https://github.com/mgedmin/restview/issues/15.


2.0.3 (2014-02-01)
------------------

- Distinguish document title from section titles with a larger font.
  Fixes https://github.com/mgedmin/restview/issues/12.

- Minor tweaks and fixes to make restview work better on Windows (e.g. all
  tests now pass).


2.0.2 (2013-10-02)
------------------

- Suppress errors when file disappears while restview is polling for changes.
  Fixes https://github.com/mgedmin/restview/issues/11.

- Added a favicon.  Fixes https://github.com/mgedmin/restview/issues/8.


2.0.1 (2013-05-01)
------------------

- Always require Pygments.  Fixes https://github.com/mgedmin/restview/issues/9.


2.0 (2013-04-04)
----------------

- Python 3 support (LP#1093098).  Patch by Steven Myint (git@stevenmyint.com).

- Moved to Github.

- 100% test coverage.

- Automatically reload the web page when the source file changes (LP#965746).
  Patch by speq (sp@bsdx.org), with modifications by Eric Knibbe and Marius
  Gedminas.

- New option: restview --long-description (shows the output of python setup.py
  --long-description).

- New option: restview --strict. Patch by Steven Myint (git@stevenmyint.com).

- Improve auto-linkification of local file names:

  * allow subdirectories
  * recognize .rst extensions

- Many improvements by Eric Knibbe:

  * ``restview dirname`` now ignores hidden subdirectories.
  * files in directory listings are sorted case-insensitively.
  * allow serving gif and jpg images.
  * CSS rules for rubric, sidebars, and many other things.
  * syntax highlighting for code blocks.
  * improved HTTP error messages.
  * HTTP headers to prevent browser caching of dynamic content.


1.2.2 (2010-09-14)
------------------

- setup.py no longer requires docutils (LP#637423).


1.2.1 (2010-09-12)
------------------

- Handle spaces and other special characters in URLs (LP#616335).

- Don't linkify filenames inside external references (LP#634827).


1.2 (2010-08-06)
----------------

- "SEVERE" docutils errors now display a message and unformatted file in
  the browser, instead of a traceback on the console.
- New command-line option, -e COMMAND.
- Added styles for admonitions; many other important styles are still missing.


1.1.3 (2009-10-25)
------------------

- Spell 'extras_require' correctly in setup.py (LP#459840).
- Add a MANIFEST.in for complete source distributions (LP#459845).


1.1.2 (2009-10-14)
------------------

- Fix for 'localhost' name resolution error on Mac OS X.


1.1.1 (2009-07-13)
------------------

- Launches the web server in the background.


1.1.0 (2008-08-26)
------------------

- Accepts any number of files and directories on the command line.


1.0.1 (2008-07-26)
------------------

- New option: --css.  Accepts a filename or a HTTP/HTTPS URL.


1.0.0 (2008-07-26)
------------------

- Bumped version number to reflect the stability.
- Minor CSS tweaks.


0.0.5 (2007-09-29)
------------------

- Create links to other local files referenced by name.
- Use pygments (if available) to syntax-highlight doctest blocks.
- Handle JPEG images.


0.0.4 (2007-09-28)
------------------

- Remove the unstable Gtk+ version.


0.0.3 (2007-09-28)
------------------

- Use setuptools for packaging.


0.0.2 (2007-01-21)
------------------

- Browser-based version.
- Command line options -l, -b (thanks to Charlie Shepherd).
- CSS tweaks.
- Unicode bugfix.
- Can browse directory trees.
- Can serve images.


0.0.1 (2005-12-06)
------------------

- PyGtk+ version with GtkMozEmbed.  Not very stable.

