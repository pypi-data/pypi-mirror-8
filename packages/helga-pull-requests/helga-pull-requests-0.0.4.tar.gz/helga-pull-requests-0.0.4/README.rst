helga-pull-requests
===================

A helga plugin to quickly link to github pull requests. This will match either the pattern
<repo_name>-pr<number> (when PULL_REQUESTS_DEFAULT_ACCOUNT is set) or <account>/<repo_name>-pr<number>.

Settings
--------

**PULL_REQUESTS_DEFAULT_ACCOUNT** A default account to use for empty matches of <repo_name>-pr<number>
**PULL_REQUESTS_GITHUB_HOST** A url to use for github. Defaults to `https://github.com`.

License
-------

Copyright (c) 2014 Shaun Duncan

Licensed under an `MIT`_ license.

.. _`MIT`: https://github.com/shaunduncan/helga-pull-requests/blob/master/LICENSE
