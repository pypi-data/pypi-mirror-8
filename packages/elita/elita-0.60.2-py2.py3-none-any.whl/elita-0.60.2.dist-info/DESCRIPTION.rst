Elita
=====

Elita is an engine/framework for continuous deployment and API-driven infrastructure utilizing git
and salt. Elita maps build packages to filesystem locations on an arbitrary number of remote servers and allows deployment
(and more) via RESTful HTTP calls.

(for more, see:  http://elita.readthedocs.org/en/latest/intro.html )

Documentation
=============

*   http://elita.readthedocs.org/en/latest


Installation
============

*   http://elita.readthedocs.org/en/latest/install.html


Quickstart
==========

*   http://elita.readthedocs.org/en/latest/quickstart.html


Mailing List
============

*   https://groups.google.com/d/forum/elita-users


Issues/Bugs
===========

*   https://bitbucket.org/scorebig/elita/issues


Source/Homepage
===============

*   https://bitbucket.org/scorebig/elita


Support
=======

Problems?

Email: ben@keroack.com
Google Hangouts: ben@keroack.com (usually available 9am-7pm Pacific)

0.60.2
- Fix startup script

0.60.1
- Add glob2 to install dependencies (fixes pip install)
- Fix exception when not all servers return for git index removal
- Add salt connectivity check to deployment procedure
- Execute gunicorn instead of pserve in start script
- Fix erroneous 'no files' log message in PackageMapper
- (internal) clean up deployment code a bit

0.60.0
- Package Map feature: Create build packages automatically on upload from a set of glob patterns (see docs)
- Delete stale git index locks (if present) during deployment
- (internal) fix for potential multiprocessing deadlock and better queue usage
- (internal) New decorator-based parameter validation

0.59.3
- Fix exceptions in application census
- Remove application census from top-level application view
- Small fix to Deployment model
- Add ordered gitdeploy information to documentation for groups
- Change repo link, homepage in README
- Fix docs version, copyright

0.59.2
- Add documentation links to README

0.59.1
- Fix issue where gitdeploy ordering was not respected with deployments consisting only of nonrolling groups
- Consolidate all nonrolling groups into first batch
- Fix minor bug with deployment result job logging

0.59
- First public release



