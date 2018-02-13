#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/user/crawl')
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from log_ctl import g_log
import time


TAOBAO_URL = 'http://taobao.com'
Search_URL = 'https://s.taobao.com/search?q=%e6%89%8b%e6%9c%ba'
TIME_OUT = 16
Window_width = '1200'
Window_length = '5310'

class BasePage(object):
    """ Base class to initialize the base page that will be called from all the pages
        Default is phantomjs
    """
    

    def __init__(self, driver=None, proxy=None):
        if driver == None:
#            self.driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
            cap = webdriver.DesiredCapabilities.PHANTOMJS
#            cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
            cap["phantomjs.page.settings.resourceTimeout"] = TIME_OUT*1000
            g_log.debug(cap)
            if proxy==None:
                self.driver = webdriver.PhantomJS(desired_capabilities=cap)
            else:
                # proxy should be either http or https, and with ip:port information
                g_log.debug(proxy[0]+'   '+proxy[1])
                self.driver = webdriver.PhantomJS(service_args=['--proxy='+proxy[0], '--proxy-type='+proxy[1]], desired_capabilities=cap)
        else:
            self.driver = driver
            self.driver.set_page_load_timeout(TIME_OUT)

class TaoBaoMainPage(BasePage):

    def __init__(self, driver=None, proxy=None):
        super().__init__(driver, proxy)
        self.element = None

    def waitForLoad(self):
        # if javascript and jQuery is completely loaded, return True
        g_log.debug("wait for the page is loaded.")
        time.sleep(TIME_OUT)
        page_state_js = self.driver.execute_script('return document.readyState;')
        try:
            page_state_jq = int(self.driver.execute_script('return jQuery.active;'))
        except Exception as e:
            g_log.error("get jquery state error: %s" % e)
            page_state_jq = 0
        if page_state_jq == 0 and page_state_js == 'complete':
            return True
        else:
            return False

    def OpenPage(self, url = TAOBAO_URL):
        
        try:
            self.driver.get(url)
            self.driver.set_window_size(Window_width, Window_length)
            while not self.waitForLoad():
                time.sleep(TIME_OUT)
            element = True
        except Exception as e:
            g_log.error(e)
            element = None
        finally:
            self.element = element
        

    def SearchItems(self, words):
        if self.element == None:
            g_log.warn("The main page has not opened when try to search items")
            return False
        else:
            try:
                # search bar is with id 'q'
                g_log.debug('Now get the search bar')
                input_form = self.driver.find_element_by_xpath('//*[@id="q"]')
                input_form.clear()
                input_form.send_keys(words)
                g_log.debug('Now get the search button')
                search_btn = self.driver.find_element_by_class_name('icon-btn-search')
                search_btn.click()
                self.waitForLoad()
                return True
            except Exception as e:
                g_log.error(e)
                return False

    def GoToSearchPage(self, page_id):
        try:
            if page_id < 1:
                g_log.error('page id is not correct %d' % page_id)
                return False
            g_log.debug('Now get the page Input bar')
            input_form = self.driver.find_element_by_class_name('J_Input')
            input_form.clear()
            input_form.send_keys(int(page_id))
            g_log.debug('Now Click the submit button')
            submit_btn = self.driver.find_element_by_class_name('J_Submit')
            submit_btn.click()
            self.waitForLoad()
            return True
        except Exception as e:
                g_log.error(e)
                return False
            


    def GoThroughPage(self):
        try:
            g_log.debug('Now get all the hidden items in page')
            # in taobao page it mark the blank row with class blank-row
            blank_items = self.driver.find_elements_by_class_name('blank-row')
            for item in blank_items:
                self.driver.execute_script("arguments[0].scrollIntoView();", item)
                time.sleep(1)
            return True
        except Exception as e:
            g_log.error(e)
            return False

    def SaveScreenshot(self, name=None):
        if name==None:
            self.driver.save_screenshot('./screenshot.png')
        else:
            self.driver.save_screenshot('./'+name+'.png')

    def SavePage(self, name=None):
        try:
            if name == None:
                file_ = open('page.html', 'w')
            else:
                file_ = open(name+'.html', 'w')
            page = self.driver.page_source
            file_.write(page)
            file_.close()
        except Exception as e:
            g_log.error(e)
            return False

    def ClosePage(self):
        self.driver.close()

def main():
    taobao = TaoBaoMainPage()
    taobao.OpenPage(Search_URL)
    taobao.SearchItems(u'手机')
    taobao.SaveScreenshot()
    taobao.ClosePage()
    

if __name__ == "__main__":
    main()















