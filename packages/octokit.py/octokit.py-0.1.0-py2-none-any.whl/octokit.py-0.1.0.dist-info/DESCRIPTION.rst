Copyright (c) 2013 Alexander Shchepetilnikov

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Download-URL: https://github.com/irqed/octokit.py/tree/0.1.0
Description: Octokit.py: GitHub API toolkit
        =========================
        It's a small library written in Python to query GitHub API in a quick and easy way.
        
        [![Build Status](https://travis-ci.org/irqed/octokit.py.svg?branch=master)](https://travis-ci.org/irqed/octokit.py)
        [![Coverage Status](https://coveralls.io/repos/irqed/octokit.py/badge.png?branch=master)](https://coveralls.io/r/irqed/octokit.py?branch=master)
        [![PyPi version](https://pypip.in/v/octokit.py/badge.png)](https://crate.io/packages/octokit.py/)
        [![PyPi downloads](https://pypip.in/d/octokit.py/badge.png)](https://crate.io/packages/octokit.py/)
        
        Features
        --------
        * Clean and easy interface
        * Completely reflects GitHub API V3 (except gists)
        * Dot notation
        * 100% test coverage 
        
        
        Requirements
        --------
        * Python 2.6/2.7 (Python 3 support is blocked by slumber, but should be fixed soon)
        * slumber
        
        Installation
        ------------
        Note: PyPi package isn't updated yet.
        ```
          pip install octokit.py
        ```
        
        Examples
        -------------
        To get a list of user's repositories:
        ```python
        >>> hub = Octokit()
        >>> print hub.users('irqed').repos.get()
        ```
        or
        ```python
        >>> print hub.users.irqed.repos.get()
        ```
        
        To use basic authorization just pass your login and password
        ```python
        >>> hub = Octokit(login='username', password='secret_password')
        >>> print hub.repos.irqed('octokit.py').issues.get()
        ```
        
        To use access token:
        ```python
        >>> hub = Octokit(access_token='so_secret_wow')
        ```
        
        Documentation
        -------------
        
        Alternatives
        -------------
        * [PyGithub](https://github.com/jacquev6/PyGithub)
        * [Pygithub3](https://github.com/copitux/python-github3)
        * [libsaas](https://github.com/ducksboard/libsaas)
        * [github3.py](https://github.com/sigmavirus24/github3.py)
        * [sanction](https://github.com/demianbrecht/sanction)
        * [agithub](https://github.com/jpaugh/agithub)
        * [githubpy](https://github.com/michaelliao/githubpy)
        * [octohub](https://github.com/turnkeylinux/octohub)
        * [Github-Flask](http://github-flask.readthedocs.org/)
        * [torngithub](https://github.com/jkeylu/torngithub)
        
        
        .. :changelog:
        
        Release History
        ---------------
        
        0.0.2 (2014-07-30)
        ++++++++++++++++++
        
        * First implementation
        
        
        0.0.1 (2013-11-16)
        ++++++++++++++++++
        
        * Motivation
        * Conception
        
Platform: UNKNOWN
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: Developers
Classifier: Natural Language :: English
Classifier: Programming Language :: Python
Classifier: Operating System :: OS Independent
Classifier: License :: OSI Approved :: MIT License
Classifier: Topic :: Software Development :: Libraries :: Python Modules
