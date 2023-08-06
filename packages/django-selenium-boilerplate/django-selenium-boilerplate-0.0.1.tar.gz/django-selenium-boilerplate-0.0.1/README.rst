Django Selenium Boilerplate
===========================

A simple boilerplate app for selenium testing in Django with ``LiveServerTestCase``.

Installation::

    pip install django-selenium-boilerplate

Usage
------

This app provides a ``SeleniumBase`` class that extends ``LiveServerTestCase``. It sets up selenium, and provides several helper methods for testing.

- ``SeleniumBase.url(route, *args, **kwargs)``: Returns the full live server URL to the given route.  If ``rotue`` starts with "/", it's interpreted as a full path.  Otherwise, it's interpreted as a reversible route name, which is resolved using ``reverse(route, args=args, kwargs=kwargs)``.
- ``SeleniumBase.by_css(selector)``: Shortcut for ``self.selenium.find_element_by_css_selector``.
- ``SeleniumBase.by_csss(selector)``: Shortcut for ``self.selenium.find_elements_by_css_selector``.
- ``SeleniumBase.await_selector(selector, timeout=30)``: Polls for the presence of the given CSS selector, until the timeout.  Returns when at least one element matching that selector is found.
- ``SeleniumBase.select_option(selector, visible_text)``: Shortcut for selecting the ``<option>`` with the given visible text within the ``<select>`` that matches the given CSS selector.

Optional setting:
- ``SELENIUM_FIREFOX_BIN``: Optional path to the firefox binary to use when building the Selenium driver.  Use this to constrain to a particular selenium-supported Firefox release.

Example::

    from selenium_boilerplate import SeleniumBase

    class MyTestCase(SeleniumBase):
        def test_home(self):
            # Look up the route named "home"
            self.selenium.url("home")
            # Pause until the selector "h1" appears
            self.await_selector("h1")
            self.assertEquals(self.by_css("h1").text, "Hello, World")

License
-------

BSD License.

Copyright (c) 2014, Charlie DeTar
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
