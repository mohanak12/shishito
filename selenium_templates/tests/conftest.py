# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Vojtech Burian
@summary: Fixtures for handling custom BrowserStack parameters
"""
import pytest
from library.junithtml import LogHTML


def pytest_addoption(parser):
    parser.addoption("--xbrowser", action="store", default="Chrome",
                     help="BrowserStack browser: Chrome, Firefox, IE, PhantomJS, Opera, Safari")
    parser.addoption("--xbrowserversion", action="store", default="32.0",
                     help="BrowserStack browser version. Value depends on selected browser.")
    parser.addoption("--xos", action="store", default="Windows",
                     help="BrowserStack operating system: Windows, OS X")
    parser.addoption("--xosversion", action="store", default="7",
                     help="BrowserStack operating system version. Depends on selected OS.")
    parser.addoption("--xresolution", action="store", default="1024x768",
                     help="Screen resolution: 1024x768, 1280x960, 1280x1024, 1600x1200, 1920x1080")
    parser.addoption("--xbuildname", action="store", default="Unnamed",
                     help="Test build name")
    group = parser.getgroup("terminal reporting")
    group.addoption('--html', '--junit-html', action="store",
           dest="htmlpath", metavar="path", default=None,
           help="create html style report file at given path.")
    group.addoption('--htmlprefix', '--html-prefix', action="store",
           dest="prefix", metavar="str", default=None,
           help="prepend prefix to classnames in html output")



def pytest_configure(config):
    htmlpath = config.option.htmlpath
    #print(htmlpath)
    prefix = config.option.prefix
    #print(prefix)
    # prevent opening xmllog on slave nodes (xdist)
    if htmlpath and not hasattr(config, 'slaveinput'):
        config._html = LogHTML(htmlpath, prefix)
        config.pluginmanager.register(config._html)

def pytest_unconfigure(config):
    html = getattr(config, '_html', None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)


@pytest.fixture(scope='class')
def xbrowser(request):
    return request.config.getoption("--xbrowser")


@pytest.fixture
def xbrowserversion(request):
    return request.config.getoption("--xbrowserversion")


@pytest.fixture
def xos(request):
    return request.config.getoption("--xos")


@pytest.fixture
def xosversion(request):
    return request.config.getoption("--xosversion")


@pytest.fixture
def xresolution(request):
    return request.config.getoption("--xresolution")


@pytest.fixture
def xbuildname(request):
    return request.config.getoption("--xbuildname")