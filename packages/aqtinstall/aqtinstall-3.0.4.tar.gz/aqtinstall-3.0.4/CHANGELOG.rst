====================
aqtinstall changeLog
====================

All notable changes to this project will be documented in this file.

`Unreleased`_
=============

`v3.0.4`_ (6, Nov. 2023)
========================

Security
--------
* CVE-2023-32681: Bump requests@2.31.0 (#724)

Chnaged
-------
* Remove a specific mirror from fallback (#688)

`v3.0.3`_ (25, Mar. 2023)
=========================

Fixed
-----
* Test: update tox.ini config (#634)
* CI: Pin checkout at v3 in all workflows(#649)

Changed
-------
* Standalone binary build with PyInstaller directly(#598)

`v3.0.2`_ (26, Oct. 2022)
=========================

* Fix installation of Qt6/WASM arch on windows (#583,#584)
* Docs: allow localization (#588)
* Docs: Add Japanese translation (#595)

`v3.0.1`_ (30, Sep. 2022)
=========================

* Actions: Fix standalone executable upload (#581)
* Actions: Bump versions (#579)
  - pypa/gh-action-pypi-publish@v1
  - actions/setup-python@v4

`v3.0.0`_ (29, Sep. 2022)
=========================

Added
-----
* Automatically install desktop qt when required for android/ios qt installations(#540)

Fixed
-----
* Tolerate empty DownloadArchive tags while parsing XML(#563)
* Fix standalone executable build for windows (#565,#567)

Changed
-------
* Update Security policy
* Update combinations.json(#566)
* CI: now test on MacOS 12(#541)

`v2.2.3`_ (17, Aug. 2022)
=========================

Fixed
-----
* Building standalone executable: aqt.exe (#556,#557)

Added
-----
* Docs: add explanation of ``list-qt --long-modules`` (#555)


`v2.2.2`_ (11, Aug. 2022)
=========================

Added
-----
* Add ``aqt list-qt --long-modules`` (#543,#547)

Fixed
-----
* Fix kwargs passed up AqtException inheritance tree (#550)


`v2.2.1`_ (9, Aug. 2022)
========================

Changed
-------
* ``install-qt`` command respect ``--base`` argument option when
  retrieve metadata XML files by making ``MetadataFactory``
  respect ``baseurl`` set. (#545)

`v2.2.0`_ (2, Aug. 2022)
========================

Added
-----
* Add code of conduct (#535)

Changed
-------
* test: prevent use of flake8@5.0 (#544)
* Improve tox and pytest config(#544)
* Properly retrieve folder names from html pages of all mirrors(#520)
* Log: left align the level name (#539)
* Update combinations (#537)
* Introduce Updates.xml data class and parser (#533)
* archives: do not keep update.xml text in field (#534)
* docs: Bump sphinx@5.0 (#524)

Fixed
-----
* Update readthedocs config (#535)
* Fix readme description of list-qt (#527)

Deprecated
----------
* Deprecate setup.py file (#531)

`v2.1.0`_ (14, Apr. 2022)
=========================

Changed
-------
* Change security policy(#506):
  Supported 2.0.x
  Unsupported 1.2.x and before
* Bump py7zr@0.18.3(#509)
* pyproject.toml configuration
  * project section(#507)
  * setuptools_scm settings(#508)
* Use SHA256 hash from trusted mirror for integrity check (#493)
* Update combinations.xml
  * QtDesignStudio generation2 (#486)
  * IFW version (from 42 to 43) change (#495)
  * Support Qt 6.2.4 (#502)
* Update fallback mirror list (#485)

Fixed
-----
* Fix patching of Qt6.2.2-ios(#510, #503)
* Test: Conditionally install dependencies on Ubuntu (#494)

Added
-----
* doc: warn about unrelated aqt package (#490)
* doc: add explanation of --config flag in CLI docs (#491)
* doc: note about MSYS2/Mingw64 environment

Security
--------
* Use secrets for secure random numbers(#498)
* Use defusedxml to parse Updates.xml file to avoid attack(#498)
* Improve get_hash function(#504)
* Check Update.xml file with SHA256 hash (#493)


`v2.0.6`_ (7, Feb. 2022)
========================

Fixed
-----
* Fix archives flag(#459)
* Accept the case Update.xml in Server has delimiter without space(#479)
* Fix getUrl function to use property http session and retry(#473)

Added
-----
* 32bit release binary(#471)

Changed
-------
* Update combinations.xml
  * Qt 6.2.2, 6.2.3, 6.3.0(#481,#484)

`v2.0.5`_ (11, Dec. 2021)
=========================

Changed
-------
* Reduce memory consumption: garbage collection on install subprocess(#464)
* Cache PowerShell modules on Azure Pipeline(#465)

`v2.0.4`_ (5, Dec. 2021)
=========================

Fixed
=====
* Allow duplicated install on the directory previously installed(#438,#462)
* Memory error on 32bit python on Windows(#436,#462)

Changed
=======
* Change list-src, list-doc and list-example command(#453)

`v2.0.3`_ (25, Nov. 2021)
=========================

Added
-----
* Improve --keep and new --archive-dest options(#458)

Fixed
-----
* Fix cross-platform installation failure (#450)
* CI: update OSes, Windows-2019, macOS-10.15(#444,#456)
* CI: fix failure of uploading coveralls(#446)
* CI: test for QtIFW(#451)

Changed
-------
* combinations matrix json(#452)

`v2.0.2`_ (1, Nov. 2021)
=========================

Added
-----
* Support Qt 6.2.1 (#441)

Fixed
-----
* Degraded install-tool (#442,#443)

Changed
-------
* Add suggestion to use ``--external`` for MemoryError (#439)


`v2.0.1`_ (29, Oct. 2021)
=========================

Added
-----
* Allow retries on checksum error(#420)
* Run on Python 3.10(#424)
* Add more mirrors for fallback(#432)
* Add fallback URL message(#434)

Fixed
-----
* ``--noarchives`` inconsistency(#429)
* Allow multiprocessing error propagation(#419)
* Legacy command behavior, reproduce also old bugs (#414)
* Fix crash on ``crash install-qt <host> <tgt> <spec>`` with no specified arch(#435)

Changed
-------
* Print working directory and version in error message(#418)

Security
--------
* Use HTTPS for mirror site(#430)


`v2.0.0`_ (29, Sep. 2021)
=========================

Added
-----
* Add error messages when user inputs an invalid semantic version(#291)
* Security Policy document(#341)
* CodeQL static code analysis(#341)
* CI: generate combination json in actions (#318,#343)
* Test: add and improve unit tests(#327,#359)
* Docs: getting started section(#351)
* Docs: recommend python3 for old systems(#349)
* Automatically update combinations.json (#343,#344,#345,#386,#390,#395)
* CI: test with Qt6.2 with modules(#346)
* README: link documentation for stable(#329)
* Support WASM on Qt 6.2.0(#384)
* Add Binary distribution for Windows(#393,#397)
* Add list-qt --archives feature(#400)
* Require architecture when listing modules(#401)

Changed
-------
* list subcommand now support tool information(#235)
* list subcommand can show versions, architectures and modules.(#235)
* C: bundle jom.zip in source(#295)
* Add max_retries configuration for connection(#296)
* Change settings.ini to introduce [requests] section(#297)
* Change log format for logging file.
* Extension validation for tool subcommand(#314)
* list subcommand has --tool-long option(#304, #319)
* tool subcommand now install without version spec(#299)
* README example command is now easy to copy-and-paste(#322)
* list subcommand update(#331)
* Improve handle of Ctrl-C keyboard interruption(#337)
* Update combinations.json(#344,#386)
* Turn warnings into errors when building docs(#360)
* Update documentations(#358,#357)
* Test: consolidate lint configuration to pyproject.toml(#356)
* Test: black configuration to max_line_length=125 (#356)
* New subcommand syntax (#354,#355)
* Failed on missing modules(#374)
* Failed on missing tools(#375)
* Remove 'addons' prefix for some modules for Qt6+ (#368)
* Fix inappropriate warnings(#370)
* Update README to fix version 2 (#377)
* list-qt: Specify version by SimpleSpec(#392)
* Add helpful error messages when modules/tools/Qt version does not exist(#402)

Fixed
-----
* Fix helper.getUrl() to handle several response statuses(#292)
* Fix Qt 6.2.0 target path for macOS.(#289)
* Fix WinRT installation patching(#311)
* Fix Qt 5.9.0 installation (#312)
* Link documentations for stable/latest on README
* Check python version when starting command (#352)
* README: remove '$' from example command line(#321)
* README: fix command line example lexer(#322)
* CI: fix release script launch conditions(#298)
* Handle special case for Qt 5.9.0(#364)
* Running python2 -m aqt does not trigger Python version check (#372,#373)
* docs(cli): correct the parameter of "list-tool" in an example(#399)
* Doc: Fix broken mirror link in cli.rst (#403)
* CI: fix release action fails with no files found(#405)



.. _Unreleased: https://github.com/miurahr/aqtinstall/compare/v3.0.4...HEAD
.. _v3.0.4: https://github.com/miurahr/aqtinstall/compare/v3.0.3...v3.0.4
.. _v3.0.3: https://github.com/miurahr/aqtinstall/compare/v3.0.2...v3.0.3
.. _v3.0.2: https://github.com/miurahr/aqtinstall/compare/v3.0.1...v3.0.2
.. _v3.0.1: https://github.com/miurahr/aqtinstall/compare/v3.0.0...v3.0.1
.. _v3.0.0: https://github.com/miurahr/aqtinstall/compare/v2.2.3...v3.0.0
.. _v2.2.3: https://github.com/miurahr/aqtinstall/compare/v2.2.2...v2.2.3
.. _v2.2.2: https://github.com/miurahr/aqtinstall/compare/v2.2.1...v2.2.2
.. _v2.2.1: https://github.com/miurahr/aqtinstall/compare/v2.2.0...v2.2.1
.. _v2.2.0: https://github.com/miurahr/aqtinstall/compare/v2.1.0...v2.2.0
.. _v2.1.0: https://github.com/miurahr/aqtinstall/compare/v2.0.6...v2.1.0
.. _v2.0.6: https://github.com/miurahr/aqtinstall/compare/v2.0.5...v2.0.6
.. _v2.0.5: https://github.com/miurahr/aqtinstall/compare/v2.0.4...v2.0.5
.. _v2.0.4: https://github.com/miurahr/aqtinstall/compare/v2.0.3...v2.0.4
.. _v2.0.3: https://github.com/miurahr/aqtinstall/compare/v2.0.2...v2.0.3
.. _v2.0.2: https://github.com/miurahr/aqtinstall/compare/v2.0.1...v2.0.2
.. _v2.0.1: https://github.com/miurahr/aqtinstall/compare/v2.0.0...v2.0.1
.. _v2.0.0: https://github.com/miurahr/aqtinstall/compare/v1.2.5...v2.0.0
