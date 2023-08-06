Changelog
=========


1.3 (2014-11-18)
----------------

- Fixed bug: ``%S`` instead of ``%s`` (lowercase) in a log message. You'd get
  a ``ValueError: unsupported format character in recipe.py`` if you got hit
  by the bug (which only happens in a corner case).


1.2 (2014-03-19)
----------------

- Using ``os.path.lexists()`` instead of ``os.path.exists()``, this one
  returns True also if there's a symlink that leads nowhere. ``exists()``
  follows the symlink so returns False for broken symlinks. In our case that
  means that the broken symlink isn't removed so that the subsequent creation
  of a new symlink fails as the filename is already in use. Fixes #3.


1.1 (2014-03-19)
----------------

- Added Python 2.6 compatibility.

- Compensating for packages with underscore characters like ``MySQL_python``.
  (Both fixes by benwah, thanks!)


1.0.1 (2013-09-17)
------------------

- Quick fix bug where buildout rmtree can't remove egg info/link files.


1.0 (2013-09-11)
----------------

- Re-released as 1.0 as it is stable now.


0.4 (2013-09-10)
----------------

- Back to symlinking instead of copying: some egg-info files are
  actually directories. Downside: Windows is out of the door again.


0.3 (2013-09-10)
----------------

- We report files that we've added to buildout now so that buildout
  automatically cleans them up for us. No more pollution in our
  develop-eggs directory!

- Symlinking folders of non-egg distributions that we found in a
  system directory turned out to be a bad idea. Some distributions
  install files instead of directories (GDAL ends up as ``gdal.py``,
  for instance). We now only copy the "egg-info" files, which turns
  out to be enough for setuptools to find the distributions.

- Copying (see above) instead of symlinking means it also works on
  windows again.


0.2 (2013-09-10)
----------------

- Fix in README for running sysegg standalone.

- Distributions that aren't eggs but directories directly inside a
  ``sys.path`` directory would have the actual system folder as their
  location. This used to mean that everything in that system folder
  can erroneously be used as a system egg. Not anymore, as those
  directories are now symlinked directly instead of being used through
  a too-generic ``.egg-link`` file.

- This recipe uses symlinks for the above fix, which means it doesn't
  work on windows anymore.


0.1 (2013-02-05)
----------------

- Patch code to allow for force-sysegg=false

- Add original code from osc.recipe.sysegg.

- Add buildout and setup.py.

- Added readme, changes and MIT license.
