'''
Copyright (c) 2014 Juju. Inc

Code Licensed under MIT License. See LICENSE file.
'''
import urlparse
import time
import logging
import re
import inspect
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from functools import wraps
from types import MethodType
from threading import Lock
from ..webunittest import unittest
from ..settings.solve_settings import solve_settings
from ..Logger import Logger
from ..base import SmoothTestBase

_with_screenshot = '_with_screenshot'
_zero_screenshot = '_zero_screenshot'


def zero_screenshot(method):
    setattr(method, _zero_screenshot, True)
    return method


def screenshot(method):
    setattr(method, _with_screenshot, True)
    return method


def no_screenshot(method):
    setattr(method, _with_screenshot, False)
    return method


class WebdriverUtils(object):
    _implicit_wait = 30
    #Height, Width tuple
    _window_size = (800, 600)
    _shot_sizes = [(400,300), (800,600), (1024, 768)]
    _driver = None
    
    def __init__(self, base_url, logger, **kwargs):
        self._init_webdriver(base_url, **kwargs)
        self.log = logger or Logger(self.__class__.__name__)

    def _init_webdriver(self, base_url, browser='PhantomJS', webdriver=None, 
                        screenshot_level=logging.WARN):
        if webdriver:
            self._driver = webdriver
        else:
            self._init_driver(browser)
        #self.get_driver().implicitly_wait(self._implicit_wait)
        #self.get_driver().set_window_size(*self._window_size)
        self._base_url = base_url
        self._wait_timeout = 2
        if screenshot_level <= logging.ERROR:
            self._decorate_exc_sshot()
        
    def _decorate_exc_sshot(self, meth_filter=None):
        self._exc_sshot_count = 0
        fltr = lambda n, method:  (getattr(method, _with_screenshot, False)
                                   or n.startswith('test'))
        meth_filter = meth_filter or fltr
        self._sshot_lock = Lock()
        for name, method in inspect.getmembers(self):
            if not (isinstance(method, MethodType)
            and getattr(method, _with_screenshot, True)):
                continue
            if getattr(method, _zero_screenshot, False):
                method = self._decorate(name, method, zero_screeshot=True)
                setattr(self, name, method)
            elif(name != 'screenshot' 
                and meth_filter(name, method)):
                method = self._decorate(name, method)
                setattr(self, name, method) 
                
    def _decorate(self, name, method, zero_screeshot=False):
        if not zero_screeshot:
            @wraps(method)
            def dec(*args, **kwargs):
                try:
                    return method(*args, **kwargs)
                except Exception as e:
                    if self._sshot_lock.acquire(False):
                        self._exception_screenshot(name, e)
                        self._sshot_lock.release()
                    raise
        else:
            @wraps(method)
            def dec(*args, **kwargs):
                #block any further exception screenshot, until
                #we return from this call
                locked = self._sshot_lock.acquire(False)
                try:
                    return method(*args, **kwargs)
                finally:
                    if locked:
                        self._sshot_lock.release()
        return dec

    def _quit_webdriver(self):
        self._driver.quit()
        self._driver = None

    def _init_driver(self, browser):
        if not self._driver:
            #Firefox, Chrome, PhantomJS
            self._driver = new_driver(browser)

    def get_driver(self):
        assert self._driver, 'driver was not initialized'
        return self._driver
    
    def _string_to_filename(self, str_, max_size=150):
        '''
        For example:
          'My Super Company' into 'my_super_company'
        It will became like a python variable name, although it will accept 
          starting with a number
        2-Will collect alphanumeric characters and ignore the rest
        3-Will join collected groups of alphanumeric characters with "_"
        :param str_:
        '''
        str_ = str_.strip()
        words = re.findall(r'[a-zA-Z0-9][a-zA-Z0-9]*', str_)
        str_ = '_'.join(words)
        if max_size:
            return str_[:max_size]
        else:
            return str_

    def _exception_screenshot(self, name, exc):
        self._exc_sshot_count += 1
        dr = self.get_driver()
        exc = self._string_to_filename(repr(exc))
        count = self._exc_sshot_count
        test = self.__class__.__name__
        filename = '{count:03d}.{test}.{name}.{exc}.png'.format(**locals())
        self.log.e('Saving exception screenshot to: %r' % filename)
        dr.save_screenshot(filename)

    _quick_sshot_count = 0
    def _quick_screenshot(self):
        self._quick_sshot_count += 1
        filename = '{count:03d}.quick_screenshot.png'.format(**locals())
        self.log.i('Saving exception screenshot to: %r' % filename)
        self.get_driver().save_screenshot(filename)        

    def screenshot(self, *args, **kwargs):
        self.log.w('WebdriverUtils.screenshot not yet implemented.')
    
    def assert_screenshot(self, name, valid=None):
        self.log.w('WebdriverUtils.assert_screenshot not yet implemented.')

    def current_path(self):
        return urlparse.urlparse(self.get_driver().current_url).path

    def get_page(self, path, base=None, check_load=False, condition=None):
        #default value
        base = base if base else self._base_url
        driver = self.get_driver()
        url = urlparse.urljoin(self._base_url, path)
        if url.startswith('https') and isinstance(driver, webdriver.PhantomJS):
            self.log.d('PhantomJS fails with https if you don\'t pass '
                       'service_args=[\'--ignore-ssl-errors=true\']' 
                       ' Trying to fetch {url!r}'.format(url=url))
        self.log.d('Fetching page at {url!r}'.format(url=url))
        driver.get(url)
        #Errors
        msg = 'Couldn\'t load page at {url!r}'.format(url=url)
        if check_load and not self.wait_condition(condition):
            raise LookupError(msg)
        if isinstance(driver, webdriver.PhantomJS) and driver.current_url == u'about:blank':
            raise LookupError(msg + '. Url is u"about:blank"')
        if url != driver.current_url:
            self.log.d('Fetching {url!r} and we got {driver.current_url!r}.'
                       .format(**locals()))
        return driver

    _max_wait = 2
    _default_condition = 'return "complete" == document.readyState;'
    def wait_condition(self, condition=None, max_wait=None, print_msg=True):
        '''
        Active wait (polling) function, for a specific condition inside a page.
        '''
        condition = condition if condition else self._default_condition
        if isinstance(condition, basestring):
            #Its a javascript script
            def condition_func(driver):
                return driver.execute_script(condition)
            condtn = condition_func
        else:
            condtn = condition
        #first start waiting a tenth of the max time
        parts = 10
        max_wait = max_wait or self._max_wait
        top = int(parts * max_wait)
        for i in range(1, top+1):
            loaded = condtn(self.get_driver())
            if loaded:
                self.log.d('Condition "%s" is True.' % condition)
                break
            self.log.d('Waiting condition "%s" to be True.' % condition)
            time.sleep(float(i)/parts)
        if not loaded and print_msg:
            msg = ('Page took too long to load. Increase max_wait (secs) class'
                   ' attr. Or override _wait_script method.')
            self.log.d(msg)
        return loaded
    
    def _get_xpath_script(self, xpath, ret='node', single=True):
        common_func = '''
function extract_elem(elem){
    var elem = elem
    //elem.noteType == 1 > web element
    if(elem.nodeType == 2){
      //attribute
      elem = elem.value;
    }
    if(elem.nodeType == 3){
      //text()
      elem = elem.wholeText;
    }
    return elem;
}
        '''
        if single:
            script = '''
var xpath = %(xpath)r;
//XPathResult.FIRST_ORDERED_NODE_TYPE = 9
var e = document.evaluate(xpath, document, null,9, null).singleNodeValue;
return extract_elem(e);
            '''
        else:
            script = '''
var xpath = %(xpath)r;
//XPathResult.ORDERED_NODE_ITERATOR_TYPE = 5
var es = document.evaluate(xpath, document, null, 5, null);
var r = es.iterateNext();
var eslist = [];
while(r){
    eslist.push(extract_elem(r));
    r = es.iterateNext();
}
return eslist;
        '''
        ret_dict = dict(
                        node='return e',
                        text='return e.textContent',
                        click='e.click()',
                        )
        return common_func + script % locals()

    def select_xpath(self, xpath, single=True):
        dr = self.get_driver()
        try:
            e = dr.execute_script(self._get_xpath_script(xpath, single))
        except WebDriverException as e:
            msg = ('WebDriverException: Could not select xpath {xpath!r} '
                'for page {dr.current_url!r}\n Error:\n {e}'.format(**locals()))
            raise LookupError(msg)
        return e

    def has_xpath(self, xpath):
        try:
            self.select_xpath(xpath)
            return True
        except LookupError:
            return False

    def extract_xpath(self, xpath, single=True):
        result = self.select_xpath(xpath, single)
        if isinstance(result, WebElement):
            result = result.text
        assert isinstance(result, basestring)
        return result

    def fill_input(self, xpath, value):
        e = self.select_xpath(xpath)
        e.clear()
        e.send_keys(value)

    def click(self, xpath):
        e = self.select_xpath(xpath)
        e.click()

    def fill(self, xpath, value):
        self.fill_input(xpath, value)
        self.screenshot('fill', xpath, value)
        
    def wait(self, timeout=None):
        time.sleep(timeout or self._wait_timeout)


def new_driver(browser, *args, **kwargs):
    if browser == 'PhantomJS':
        kwargs.update(service_args=['--ignore-ssl-errors=true'])
    return getattr(webdriver, browser)(*args, **kwargs)


class TestBase(WebdriverUtils):
    _global_webdriver = None
    @staticmethod
    def set_webdriver(webdriver):
        TestBase._global_webdriver = webdriver
    
    @staticmethod
    def _new_webdriver(settings):
        #TODO: passing a webdriver factory, so we can cycle them
        #locking and releasing them
        browser = settings.webdriver_browser
        if settings.webdriver_pooling:
            if not TestBase._global_webdriver:
                TestBase._global_webdriver = new_driver(browser)
            driver = TestBase._global_webdriver
        else:
            driver = new_driver(browser)
        return driver

    def _init_webserver_webdriver(self, settings=None, webdriver=None):
        self._settings = settings if settings else solve_settings()
        base_url = self._settings.web_server_url
        browser = self._settings.webdriver_browser
        webdriver = webdriver if webdriver else TestBase._new_webdriver(self._settings)
        self._set_webdriver_log_level(self._settings.webdriver_log_level)
        self._init_webdriver(base_url, browser, webdriver, self._settings.screenshot_level)

    def _set_webdriver_log_level(self, log_level):
        from selenium.webdriver.remote.remote_connection import LOGGER
        LOGGER.setLevel(log_level)

    def _shutdown_webserver_webdriver(self):
        if (not self._settings.webdriver_keep_open and
            not self._settings.webdriver_pooling):
            self._quit_webdriver()


class TestCase(unittest.TestCase, TestBase, SmoothTestBase):
    @staticmethod
    def disable_method(cls, meth, log_func=lambda msg:None):
        if not isinstance(meth, basestring):
            if not hasattr(meth, 'func_name'):
                meth = meth.im_func
            meth = meth.func_name
        func = getattr(cls, meth)
        func_types = [staticmethod, classmethod]
        for ftype in func_types:
            if isinstance(cls.__dict__[meth], ftype):
                @ftype
                @wraps(func)
                def no_op(*_,  **__):
                    log_func('Ignoring call to {cls.__name__}.{meth}'
                              .format(cls=cls, meth=meth))
                setattr(cls, meth, no_op)
                return no_op

    def assert_text(self, xpath, value):
        extracted = self.extract_xpath(xpath)
        msg = (u'Expecting {value!r}, got {extracted!r} at {xpath!r}.'.
               format(**locals()))
        self.assertEqual(extracted, value, msg)
        self.screenshot('assert_text', xpath, value)


def smoke_test_module():
    #Beware, phantom doesn't like https!
    class WDU(WebdriverUtils):
        def __init__(self, base):
            self._decorate_exc_sshot()
            self.log = Logger(self.__class__.__name__)
            
        def get_driver(self, *args, **kwargs):
            class Driver(object):
                def save_screenshot(self, path):
                    print('Saves to: %r' % path)
            return Driver()

        @zero_screenshot
        def extract_xpath(self, xpath, ret='text'):
            self.select_xpath(xpath, ret)
        
        @screenshot
        def _example(self, bar):
            try:
                self.select_xpath(bar)
            finally:
                raise LookupError('With screenshot')

        def _example2(self, bar):
            raise LookupError('Without screenshot')        
        

        def _example3(self, bar):
            try:
                self.select_xpath(bar)
            finally:
                raise LookupError('Without screenshot')        

        @no_screenshot
        def example4(self, bar):
            try:
                self.select_xpath(bar)
            finally:
                raise LookupError('Without screenshot')        

        
    wdu = WDU('http://www.juju.com/', 
             #browser='Chrome'
             )
    #wdu.get_page('/')
    import traceback
    for m in [
            wdu.select_xpath, #select_xpath
            wdu.extract_xpath, 
            wdu._example,  #select_xpath + _example
            wdu._example2, 
            wdu._example3, #select_xpath
            wdu.example4, #select_xpath
              ]:            
        try:
            m('bar')
        except Exception as e:
            pass
            #traceback.print_exc()


if __name__ == "__main__":
    smoke_test_module()
