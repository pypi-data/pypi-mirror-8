"""Splinter plugin for pytest.

Provides easy interface for the browser from your tests providing the `browser` fixture
which is an object of splinter Browser class.
"""
import copy  # pragma: no cover
import functools  # pragma: no cover
import mimetypes  # pragma: no cover

import pytest  # pragma: no cover
import py  # pragma: no cover
import splinter  # pragma: no cover

from selenium.webdriver.support import wait

from .webdriver_patches import patch_webdriver  # pragma: no cover
from .splinter_patches import patch_webdriverelement  # pragma: no cover


class Browser(object):

    """Emulate splinter's Browser."""

    def __init__(self, *args, **kwargs):
        self.visit_condition = kwargs.pop('visit_condition')
        self.visit_condition_timeout = kwargs.pop('visit_condition_timeout')
        self.browser = splinter.Browser(*args, **kwargs)

    def __getattr__(self, name):
        """Proxy all splinter's browser attributes, except ones implemented in this class."""
        return getattr(self.browser, name)

    def visit(self, url):
        """Override splinter's visit to avoid unnecessary checks and add wait_until instead."""
        self.driver.get(url)
        self.wait_for_condition(self.visit_condition, timeout=self.visit_condition_timeout)

    def wait_for_condition(self, condition=None, timeout=None, poll_frequency=0.5, ignored_exceptions=None):
        """Wait for given javascript condition."""
        condition = functools.partial(condition or self.visit_condition, self)

        timeout = timeout or self.visit_condition_timeout

        return wait.WebDriverWait(
            self.driver, timeout, poll_frequency=poll_frequency, ignored_exceptions=ignored_exceptions).until(
            lambda browser: condition())


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_close_browser():
    """Close browser fixture."""
    return True


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_webdriver(request):
    """Webdriver fixture."""
    return request.config.option.splinter_webdriver


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_remote_url(request):
    """Remote webdriver url.

    :return: URL of remote webdriver.
    """
    return request.config.option.splinter_remote_url


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_selenium_socket_timeout(request):
    """Internal Selenium socket timeout (communication between webdriver and the browser).

    :return: Seconds.
    """
    return request.config.option.splinter_webdriver_socket_timeout


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_selenium_implicit_wait(request):
    """Selenium implicit wait timeout.

    :return: Seconds.
    """
    return request.config.option.splinter_webdriver_implicit_wait


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_selenium_speed(request):
    """Selenium speed.

    :return: Seconds.
    """
    return request.config.option.splinter_webdriver_speed


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_browser_load_condition():
    """The condition that has to be `True` to assume that the page is fully loaded.

    One example is to wait for jQuery, then the condition could be::

        @pytest.fixture
        def splinter_browser_load_condition():

            def condition(browser):
                return browser.evaluate_script('typeof $ === "undefined" || !$.active')

            return condition
    """
    return lambda browser: True


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_browser_load_timeout():
    """The timeout in seconds in which the page is expected to be fully loaded."""
    return 10


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_file_download_dir(request):
    """Browser file download directory."""
    name = request.node.name
    name = py.std.re.sub("[\W]", "_", name)
    x = request.config._tmpdirhandler.mktemp(name, numbered=True)

    def finalize():
        x.remove()
    request.addfinalizer(finalize)
    return x.strpath


@pytest.fixture(scope='session')  # pragma: no cover
def splinter_download_file_types():
    """Browser file types to download. Comma-separated."""
    return ','.join(mimetypes.types_map.values())


@pytest.fixture(scope='session')
def splinter_firefox_profile_preferences():
    """Firefox profile preferences."""
    return {
        'browser.cache.memory.enable': False,
        'browser.sessionhistory.max_total_viewers': 0,
        'network.http.pipelining': True,
        'network.http.pipelining.maxrequests': 8
    }


@pytest.fixture(scope='session')
def splinter_driver_kwargs():
    """Webdriver kwargs."""
    return {}


@pytest.fixture(scope='session')
def splinter_window_size():
    """Browser window size. (width, height)."""
    return (1366, 768)


@pytest.fixture(scope='session')
def splinter_session_scoped_browser(request):
    """Flag to keep single browser per test session."""
    return request.config.option.splinter_session_scoped_browser


@pytest.fixture(scope='session')
def browser_pool(request, splinter_close_browser):
    """Browser 'pool' to emulate session scope but with possibility to recreate browser."""
    pool = {}

    def fin():
        for browser in pool.values():
            try:
                browser.quit()
            except (IOError, OSError):
                pass

    if splinter_close_browser:
        request.addfinalizer(fin)

    return pool


@pytest.fixture(scope='session')
def browser_patches(splinter_selenium_socket_timeout):
    """Browser monkey patches."""
    patch_webdriver(splinter_selenium_socket_timeout)
    patch_webdriverelement()


@pytest.fixture
def browser_instance_getter(
    request,
    browser_patches,
    splinter_selenium_socket_timeout,
    splinter_selenium_implicit_wait,
    splinter_selenium_speed,
    splinter_webdriver,
    splinter_remote_url,
    splinter_browser_load_condition,
    splinter_browser_load_timeout,
    splinter_file_download_dir,
    splinter_download_file_types,
    splinter_firefox_profile_preferences,
    splinter_driver_kwargs,
    splinter_window_size,
    browser_pool,
):
    """Splinter browser instance getter. To be used for getting of plugin.Browser's instances.

    :return: function(parent). Each time this function will return new instance of plugin.Browser class.
    """
    kwargs = {}

    if splinter_webdriver == 'firefox':
        kwargs['profile_preferences'] = dict({
            'browser.download.folderList': 2,
            'browser.download.manager.showWhenStarting': False,
            'browser.download.dir': splinter_file_download_dir,
            'browser.helperApps.neverAsk.saveToDisk': splinter_download_file_types,
            'browser.helperApps.alwaysAsk.force': False,
        }, **splinter_firefox_profile_preferences)
    elif splinter_webdriver == 'remote':
        kwargs['url'] = splinter_remote_url
    if splinter_driver_kwargs:
        kwargs.update(splinter_driver_kwargs)

    def get_browser():
        return Browser(
            splinter_webdriver, visit_condition=splinter_browser_load_condition,
            visit_condition_timeout=splinter_browser_load_timeout, **copy.deepcopy(kwargs)
        )

    def prepare_browser(parent):
        browser_key = id(parent)
        browser = browser_pool.get(browser_key)
        if not splinter_session_scoped_browser:
            browser = get_browser()
            if splinter_close_browser:
                request.addfinalizer(browser.quit)
        elif not browser:
            browser = browser_pool[browser_key] = get_browser()
        else:
            try:
                browser.driver.implicitly_wait(splinter_selenium_implicit_wait)
                browser.driver.set_speed(splinter_selenium_speed)
                if splinter_window_size:
                    browser.driver.set_window_size(*splinter_window_size)
                browser.driver.delete_all_cookies()
            except IOError:
                # we lost browser, try to restore the justice
                try:
                    browser.quit()
                except Exception:
                    pass
                browser = browser_pool[browser_key] = get_browser()

        browser.visit_condition = splinter_browser_load_condition
        browser.visit_condition_timeout = splinter_browser_load_timeout
        browser.driver.get('about:blank')
        return browser

    return prepare_browser


@pytest.fixture
def browser(browser_instance_getter):
    """Browser fixture."""
    return browser_instance_getter(browser)


def pytest_addoption(parser):  # pragma: no cover
    """Pytest hook to add custom command line option(s)."""
    parser.addoption(
        "--splinter-webdriver",
        help="pytest-splinter webdriver", type="choice", choices=list(splinter.browser._DRIVERS.keys()),
        dest='splinter_webdriver', default='firefox')

    parser.addoption(
        "--splinter-remote-url",
        help="pytest-splinter remote webdriver url ", dest='splinter_remote_url', default=None)

    parser.addoption(
        "--splinter-implicit-wait",
        help="pytest-splinter selenium implicit wait, seconds", type="int",
        dest='splinter_webdriver_implicit_wait', default=1)

    parser.addoption(
        "--splinter-speed",
        help="pytest-splinter selenium speed, seconds", type="int",
        dest='splinter_webdriver_speed', default=0)

    parser.addoption(
        "--splinter-socket-timeout",
        help="pytest-splinter socket timeout, seconds", type="int",
        dest='splinter_webdriver_socket_timeout', default=120)

    parser.addoption(
        "--splinter-session-scoped-browser",
        help="pytest-splinter should use single browser instance per test session", action="store_true",
        dest='splinter_session_scoped_browser', default=True)
