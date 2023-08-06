nlgserv is a simple server that accepts JSON representations of sentences and generated English sentences from those.

It uses SimpleNLG (under the [MPL 2.0 licence](https://www.mozilla.org/MPL/)) available [on code.google.com](https://code.google.com/p/simplenlg/) for natural language generation.

In order to use SimpleNLG (which is implemented in Java), [Jython 2.7beta3](http://www.jython.org) is also bundled, under the terms of the [PSF v.2](http://www.jython.org/license.html).

Additionally, it uses Bottle v0.12.7 (under the [MIT licence](https://github.com/defnull/bottle/blob/0.12.7/LICENSE) available [on github.com](https://github.com/defnull/bottle/tree/0.12.7) for handling HTTP requests.

Build status
------------

[![Build Status](https://travis-ci.org/mnestis/nlgserv.svg?branch=master)](https://travis-ci.org/mnestis/nlgserv)
[![Latest Version](https://pypip.in/version/nlgserv/badge.png)](https://pypi.python.org/pypi/nlgserv/)