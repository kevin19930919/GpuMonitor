from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from cores.models import Product, Record, CrawlLog
import time
from bs4 import BeautifulSoup
import abc

class CrawlerBase:
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        self._search_url = search_url
        self._website_prefix = website_prefix
        self._website_name = website_name
        self._location_name = location_name
        self._products = products
        self._ignore_urls = ignore_urls

    
    ##########################################################################################
    # 網站搜尋功能
    ##########################################################################################
    def search(self, _browser, _product):
        _browser.get(self._search_url.replace("{KEYWORD}", _product.product_name.lower().strip().replace(" ", "%20")))
        time.sleep(2)

    ##########################################################################################
    # 檢查網頁是否載入完成
    ##########################################################################################
    @abc.abstractmethod
    def check_if_page_load_completely(self, _browser):
        return NotImplemented

    
    ##########################################################################################
    # 找出所有產品項目 (product_items)
    ##########################################################################################
    @abc.abstractmethod
    def find_all_product_items(self, soup):
        return NotImplemented

    ##########################################################################################
    # 找出產品標題的 element，child_node 是產品項目 (product_item)
    ##########################################################################################
    def find_product_title_node(self, product_item):
        return product_item


    ##########################################################################################
    # 找出產品價格的 element，child_node 是產品項目 (product_item)
    ##########################################################################################
    def find_product_price_node(self, product_item):
        return product_item

    
    ##########################################################################################
    # 找出產品產品細項的 URL，須注意 child_node 是產品 title node (product_title_node)
    ##########################################################################################
    def parse_product_detail_url(self, product_title_node):
        return product_title_node.find("a")["href"]

    
    ##########################################################################################
    # 找出產品名稱的文字，須注意 child_node 是產品 title node (product_title_node)
    ##########################################################################################
    def parse_product_title(self, product_title_node):
        return product_title_node.text

    ##########################################################################################
    # 找出產品價格的文字，須注意 child_node 是產品 title node (product_price_node)
    ##########################################################################################
    def parse_product_price(self, product_price_node):
        return float(product_price_node.text.replace(",", "").replace("$", ""))

    
    ##########################################################################################
    # 回傳標準產品價格，主要目的是 Momo & Pchome 要使用 EC 價格，但一般網站要用標準價格
    ##########################################################################################
    def get_standard_price(self, _product):
        return _product.product_standard_price


    ##########################################################################################
    # 進行查詢
    # 如果抓取各產品資訊過程發生錯誤，記錄下 log
    ##########################################################################################
    #TODO
    #there is a return_logs=[] as input
    def retrieve(self, _browser):
        # 針對各產品各自搜尋
        result = list()
        error_messages = list()
        
        for _product in self._products:
            try:
                # 開啟 Google 首頁
                print("Search " + _product.product_name + " @" + self._website_name + "...")
                self.search(_browser, _product)
                got_element = False
                try:
                    self.check_if_page_load_completely(_browser)
                    got_element = True
                except:
                    got_element = False

                if not got_element:
                    _log = CrawlLog.objects.create(log_time=datetime.now(), log_level="Info", website=self._website_name, location=self._location_name, 
                    message="No Result with Searching " + _product.product_name.lower().strip() + " @" + self._search_url.replace("{KEYWORD}", _product.product_name.lower().strip().replace(" ", "%20")))
                    error_messages.append(_log)
                    continue

                html = _browser.page_source # 獲取頁面原始碼，所有的
                # 使用BS進行分析
                soup = BeautifulSoup(html, features="html.parser")

                all_child_nodes = self.find_all_product_items(soup)

                if len(all_child_nodes) == 0:                    
                    _log = CrawlLog.objects.create(log_time=datetime.now(), log_level="Info", website=self._website_name, location=self._location_name, 
                    message="No Result but load complete with Searching " + _product.product_name.lower().strip() + " @" + self._search_url.replace("{KEYWORD}", _product.product_name.lower().strip().replace(" ", "%20")))
                    error_messages.append(_log)

                counter = 0
                for child_node in all_child_nodes:
                    counter = counter + 1
                    target = self.find_product_title_node(child_node)
                    price_tag = self.find_product_price_node(child_node)

                    if target is None or price_tag is None:
                        print(str(child_node))
                        _log = CrawlLog.objects.create(log_time=datetime.now(), log_level="Error", website=self._website_name, location=self._location_name, 
                        message="Title or Price tag cannot be retrieved when search " + _product.product_name.lower().strip() + " @" + self._search_url.replace("{KEYWORD}", _product.product_name.lower().strip().replace(" ", "%20")))
                        error_messages.append(_log)
                        continue
                        
                    # 進行檢查
                    if _product.verify(self.parse_product_title(target)):
                        _record = Record(website=self._website_name, location=self._location_name, 
                        product=_product, title=self.parse_product_title(target), price=self.parse_product_price(price_tag), standard_price=self.get_standard_price(_product),
                        url=self._website_prefix + self.parse_product_detail_url(target), create_time=datetime.now(), 
                        is_verified=1 if self.parse_product_price(price_tag) >= self.get_standard_price(_product) or self.parse_product_price(price_tag) == -1 else 0,total_number_of_product=len(all_child_nodes))

                        print(_record.url)
                        print(_record.title)
                        print(_record.price)

                        # 如果 url 在排除清單，則不加入
                        if _record.url not in self._ignore_urls:
                            result.append(_record)   
            except Exception as _exception:
                _log = CrawlLog.objects.create(log_time=datetime.now(), log_level="Error", website=self._website_name, location=self._location_name, 
                message=str(_exception) + " when search " + _product.product_name.lower().strip() + " @" + self._search_url.replace("{KEYWORD}", _product.product_name.lower().strip().replace(" ", "%20")))
                error_messages.append(_log)

        return result, error_messages

