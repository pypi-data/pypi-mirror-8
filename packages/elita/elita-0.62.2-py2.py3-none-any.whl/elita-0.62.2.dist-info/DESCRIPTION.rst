Elita
=====

Elita is an engine/framework for continuous deployment (Deployment as a Service) and API-driven infrastructure utilizing git
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

0.62.2
    - Clean up changelog

0.62.1

    - Add build name to deployment name/ID
    - Fix user object (and probably other) PATH endpoints
    - Deployment list now is sorted by creation datetime (descending) and includes creation datetime in output (GET /app/{appname}/deployments)
    - Doc fixes

0.62.0

    - Add deployment hook points
    - Add commits object to deployment object



