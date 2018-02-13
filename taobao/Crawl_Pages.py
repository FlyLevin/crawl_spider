#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/user/crawl')
from log_ctl import g_log
from db_tool import *
from taobao.Pages import *

PRODUCT_PANEL = 'grid-panel'


def start_crawl(taobao, pages):
    '''
    taobao is the page object, and pages are the arr from start page into end page
    [1, 33] means go through 1 to 33 search pages
    '''
    taobao.OpenPage(Search_URL)
    taobao.SearchItems(u'手机')
    try:
        conn = create_new_connect(db='taobao')
        if conn == None:
            return False
        cur = create_new_cursor(conn)
        if cur == None:
            return False
        for i in range(pages[0], pages[1]):
            get_every_page(taobao, i, conn, cur)
    except Exception as e:
        g_log.error(e)
        return False
    finally:
        close_cursor(cur)
        close_conn(conn)

def get_every_page(page_item, page_loc, db_conn, db_cursor):
    '''
    this function will goto the page_loc first, then fetch all the information into local db
    '''
    try:
        page_item.GoToSearchPage(page_loc)
        page_item.GoThroughPage()
        products = page_item.driver.find_elements_by_class_name(PRODUCT_PANEL)
        for product_item in products:
            product_name = product_currency = product_price= product_link =product_num =None
            try:
                full_name = product_item.find_element_by_xpath('.//div[2]/div[1]/a').text.strip()
                first_feature = product_item.find_element_by_xpath('div[2]/div[1]/a/span/span[1]').text.strip()
                product_name = full_name[0:full_name.index(first_feature)].strip()
                product_currency = product_item.find_element_by_xpath('.//div[2]/div[1]/span[2]/span').text.strip()
                product_price = product_item.find_element_by_xpath('.//div[2]/div[1]/span[2]/strong').text.strip()
                product_link = product_item.find_element_by_class_name('product-title').get_attribute('href')
                product_num = product_item.find_element_by_xpath('.//div[2]/div[2]/div[2]/span/span').text.strip()
            except Exception as e:
                if product_name == None:
                    g_log.error("Get Product Name Fail")
                    continue
                if product_currency == None:
                    g_log.error("Get Product Currency Fail")
                    product_currency = u'¥'
                if product_price == None:
                    g_log.error("Get price Fail")
                    product_price=0
                if product_link == None:
                    g_log.error("Get link Fail")
                    product_link = ''
                if product_num == None:
                    g_log.error("Get monthly sell num fail")
                    product_num = 0

            g_log.debug("Now fetched product info are %s, %s, %s, link: %s, %s"% (product_name,product_currency,product_price,product_link, product_num))
            g_log.debug('Now add cellphones into DB')
            db_cursor.execute('replace into cellphones (name, search_link, currency, price, sell_num) values (\"%s\", \"%s\", \"%s\", \"%d\", \"%s\")' %(product_name,product_link,product_currency,int(product_price), product_num))
            db_cursor.connection.commit()
            try:
                db_cursor.execute('select id from cellphones where name=\"%s\"' % product_name)
                product_id = db_cursor.fetchone()[0]
                g_log.debug('Now add features into DB %d' % product_id)
                product_feature = []
                features = product_item.find_elements_by_class_name("feature-item")
                for item in features:
                    product_feature.append(item.text)
                    db_cursor.execute('replace into phone_features (cellphone_id, feature_item) values (\"%d\", \"%s\")' % (int(product_id), product_feature[-1]))
                g_log.debug(product_feature)
                db_cursor.connection.commit()
            except Exception as e:
                g_log.error(e)
    except Exception as e:
        g_log.error(e)
        return False


















