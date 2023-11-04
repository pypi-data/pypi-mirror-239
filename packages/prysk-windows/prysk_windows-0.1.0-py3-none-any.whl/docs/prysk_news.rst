Unreleased
-----------------------------------------------------

Internal
_________
* Add github issue templates
* Update lockfile

Version 0.15.1 (May. 1, 2023)
-----------------------------------------------------
* Prevent prysk from crashing on platforms which do not support :code:`os.environb`
* Update dependencies

Version 0.15.0 (April. 26, 2023)
-----------------------------------------------------
* Add support for DOS to Unix line endings (\r\n to \n)
* Updated Contributors (Hall Of Fame!)

Version 0.14.0 (April. 16, 2023)
-----------------------------------------------------
* Add support for $TMPDIR variable substitution in test output
* Update dependencies

Version 0.13.1 (March. 4, 2023)
-----------------------------------------------------
* Fix os.environ restore after leaving context
* Narrow scope of contexts for test run
* Fix pytest-plugin error message
* Fix typo in pytest-plugin documentation
* Add literal character in docs

Version 0.13.0 (Feb. 16, 2023)
-----------------------------------------------------
* Added prysk pytest-plugin

Version 0.12.2 (June. 15, 2022)
-----------------------------------------------------
* Fix prysk test file lookup for relative paths
* Refactor xunit module
* Refactor test module
* Remove run module
* Fix pylint warnings in cli module
* Fix pylint warnings in run module
* Fix pylint warnings in process module
* Refactor _Cli class

Version 0.12.1 (May. 29, 2022)
-----------------------------------------------------
* Fix version output of cli
* Simplify prysk_news/changelog

Version 0.12.0 (May. 29, 2022)
-----------------------------------------------------
* Add color support to cli interface
* Port optparse based cli parser to argparse
* Update dependencies
* Update dev dependencies
* Update dependencies of github actions

Version 0.11.0 (February. 11, 2022)
-----------------------------------------------------
* Reorder publishing steps
* Fix release notes of 0.10.0 release

Version 0.10.0 (February. 11, 2022)
-----------------------------------------------------
* Add version sanity check
* Add support for automated releases
* Add support for retrieving project version from pyproject.toml

Version 0.9.0 (February. 11, 2022)
-----------------------------------------------------
* Add support for automated releases
* Add support for retrieving project version from pyproject.toml

Version 0.9 (Jan. 29, 2022)
---------------------------
* Add basic documentation
* Release new version to account and cope with accidentally
  deleted (untagged prysk version 0.8)

    .. note::
        once a version is published on pipy it can't be
        reused even if it has been deleted
        (see `file name reuse <https://pypi.org/help/#file-name-reuse>`_).

Version 0.8 (Jan. 25, 2022)
---------------------------
* Rename cram to prysk

    .. warning::
        Also semantically relevant names have been renamed,
        e.g. env var CRAMTMP is now PRYSK_TEMP
