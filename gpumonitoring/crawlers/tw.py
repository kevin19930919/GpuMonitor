from .crawler_base import CrawlerBase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from cores.models import Product, Record, CrawlLog
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import asyncio
from concurrent.futures import ThreadPoolExecutor

class IsunfarCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(IsunfarCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "txt_prod_price"))
            )
            
    def find_all_product_items(self, soup):
        return soup.find_all("div", class_="proditem_body")

    def find_product_title_node(self, product_item):
        return product_item.find("div", class_="prod_title")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="txt_prod_price")
    
    def parse_product_detail_url(self, product_title_node):
        return product_title_node.find("a")["href"]


class SinyaCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(SinyaCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "showProdPriceArea"))
            )
            
    def find_all_product_items(self, soup):
        return soup.find_all("div", class_="showProdBox")

    def find_product_title_node(self, product_item):
        return product_item.find("div", class_="showProdName")

    def find_product_price_node(self, product_item):
        return product_item.find("div", class_="showProdPriceArea").find("span")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.parent["href"]


class RuifrostCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(RuifrostCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def search(self, _browser, _product):
        _browser.get(self._search_url)
        time.sleep(1)
        # 尋找欄位輸入關鍵字
        textbox = _browser.find_element(By.ID, "keyword")
        textbox.send_keys(_product.product_name.lower().strip())
        _browser.find_element(By.NAME, "imageField").click()
        time.sleep(1)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
            
    def find_all_product_items(self, soup):
        return soup.find_all("div", class_="goodsMod goodsModH220")

    def find_product_title_node(self, product_item):
        return product_item.find("p").find("a")

    def find_product_price_node(self, product_item):
        return product_item.find("font")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node["href"]

    def parse_product_price(self, product_price_node):
        try:
            return float(product_price_node.text.replace("會員價：", "").replace(" 元", "").replace(",", "").replace("$", ""))
        except:
            return -1

# 需要使用 EC 價格檢查
class MomoshopCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(MomoshopCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
            
    def find_all_product_items(self, soup):
        return soup.find("div", class_="listArea").find_all("li")

    def find_product_title_node(self, product_item):
        return product_item.find("h3", class_="prdName")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="price")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.parent["href"]

    def parse_product_price(self, product_price_node):
        return float(product_price_node.text.replace(",", "").replace("$", ""))

    
    ##########################################################################################
    # 回傳標準產品價格，主要目的是 Momo & Pchome 要使用 EC 價格，但一般網站要用標準價格
    ##########################################################################################
    def get_standard_price(self, _product):
        return _product.product_standard_price_for_ecommerce
    
# 需要使用 EC 價格檢查
class PchomeCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(PchomeCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
    
    def search(self, _browser, _product):
        _browser.get(self._search_url.replace("{KEYWORD}", _product.product_name.lower().strip().replace(" ", "%20and%20")))
        time.sleep(2)
            
    def find_all_product_items(self, soup):
        return soup.find_all("dl", class_="col3f")

    def find_product_title_node(self, product_item):
        return product_item.find("h5", class_="prod_name")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="price")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.find("a")["href"]

    def parse_product_price(self, product_price_node):
        return float(product_price_node.text.replace(",", "").replace("$", ""))

    ##########################################################################################
    # 回傳標準產品價格，主要目的是 Momo & Pchome 要使用 EC 價格，但一般網站要用標準價格
    ##########################################################################################
    def get_standard_price(self, _product):
        return _product.product_standard_price_for_ecommerce

class EclifeCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(EclifeCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def check_if_page_load_completely(self, _browser):
        # element = WebDriverWait(_browser, 3).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "col-xs-4 col-lg-3"))
        #     )
        pass
    
    def find_all_product_items(self, soup):
        return soup.find_all("div", class_="col-xs-4 col-lg-3")

    def find_product_title_node(self, product_item):
        return product_item.find("h2", class_="pName")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="sPrice")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.parent["href"]

    def parse_product_price(self, product_price_node):
        return float(product_price_node.text.replace(",", "").replace("$", "").replace("\n", "").strip())


##########################################################################################
# 此網站特別不同，完全客製化
##########################################################################################
class DeyuanpcCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(DeyuanpcCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def retrieve(self, _browser):
        # 針對各產品各自搜尋
        result = list()
        error_messages = list()

        try:
            _browser.get(self._search_url)
            time.sleep(3)

            html = _browser.page_source # 獲取頁面原始碼，所有的
            # 使用BS進行分析
            soup = BeautifulSoup(html, features="html.parser")

            options = soup.find_all("option")

            for option in options:
                option_items = option.text.replace("【", "").replace("】", "").replace("\n", "").strip().replace("元", "").split("$")
                if len(option_items) <= 1:
                    continue
                product_title = option_items[0]
                product_price = option_items[1]
                for _product in self._products:
                    if _product.verify(product_title) and _product.product_name.lower() in product_title.lower():
                        _record = Record(website=self._website_name, location=self._location_name, 
                        product=_product, title=product_title, price=float(product_price), standard_price=self.get_standard_price(_product), 
                        url=self._website_prefix, create_time=datetime.now(), 
                        is_verified=1 if float(product_price) >= self.get_standard_price(_product) or float(product_price) == -1 else 0,total_number_of_product=1)

                        print(_record.url)
                        print(_record.title)
                        print(_record.price)

                        result.append(_record)
        except Exception as _exception:
            _log = CrawlLog.objects.create(log_time=datetime.now(), log_level="Error", website=self._website_name, location=self._location_name, 
            message=str(_exception) + " when search " + self._search_url)
            error_messages.append(_log)
        

        return result ,error_messages


class AutobuyCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(AutobuyCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def search(self, _browser, _product):
        _browser.get(self._search_url)
        time.sleep(1)
        # 尋找欄位輸入關鍵字
        textbox = _browser.find_element(By.NAME, "search")
        textbox.clear()
        textbox.send_keys(_product.product_name.lower().strip())
        _browser.find_element(By.CLASS_NAME, "submit").click()
        time.sleep(1)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "products_shelf"))
            )
            
    def find_all_product_items(self, soup):
        return soup.find("ul", class_="products_shelf").find_all("li")

    def find_product_title_node(self, product_item):
        return product_item.find("a")

    def find_product_price_node(self, product_item):
        return product_item.find("p", class_="prod_price").find("strong")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node["href"]

# Yahoo 商城
class YahooMallCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(YahooMallCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gridList"))
            )
			
    # Yahoo 有些圖片可左右選擇，該 class_name 會有所不同，故不能指定特定值，必須是 BaseGridItem__grid 開頭
    def find_all_product_items(self, soup):
        return soup.find_all("ul", class_="gridList")[-1].find_all("li", class_=lambda value: value and value.startswith("BaseGridItem__grid"))

    def find_product_title_node(self, product_item):
        return product_item.find("span", class_="BaseGridItem__title___2HWui")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="BaseGridItem__itemInfo___3E5Bx").find("em")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.parent.parent["href"]

    

# Yahoo 購物中心
# 需要使用 EC 價格
class YahooBuyCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(YahooBuyCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gridList"))
            )
			
    # Yahoo 有些圖片可左右選擇，該 class_name 會有所不同，故不能指定特定值，必須是 BaseGridItem__grid 開頭
    def find_all_product_items(self, soup):
        return soup.find_all("ul", class_="gridList")[-1].find_all("li", class_=lambda value: value and value.startswith("BaseGridItem__grid"))

    def find_product_title_node(self, product_item):
        return product_item.find("span", class_="BaseGridItem__title___2HWui")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="BaseGridItem__itemInfo___3E5Bx").find("em")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.parent.parent["href"]

    
    ##########################################################################################
    # 需要使用 EC 價格
    ##########################################################################################
    def get_standard_price(self, _product):
        return _product.product_standard_price_for_ecommerce

class YahooBidCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(YahooBidCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gridList"))
            )
			
    # Yahoo 有些圖片可左右選擇，該 class_name 會有所不同，故不能指定特定值，必須是 BaseGridItem__grid 開頭
    def find_all_product_items(self, soup):
        return soup.find("ul", class_="gridList").find_all("li", class_=lambda value: value and value.startswith("BaseGridItem__grid"))

    def find_product_title_node(self, product_item):
        return product_item.find("span", class_="BaseGridItem__title___2HWui")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="BaseGridItem__price___31jkj").find("em")

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.parent.parent["href"]


class PcstoreCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(PcstoreCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)
    
    def search(self, _browser, _product):
        _browser.get(self._search_url)
        time.sleep(1)
        # 尋找欄位輸入關鍵字
        textbox = _browser.find_element(By.ID, "id_store_k_word")
        textbox.clear()
        textbox.send_keys(_product.product_name.lower().strip())
        _browser.find_element_by_xpath("//img[contains(@src,'https://img.pcstore.com.tw/web_img/supimg/bn_search02.gif')]").click()
        time.sleep(1)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list_proName"))
            )
            
	
    def find_all_product_items(self, soup):
        return soup.find_all("td", class_="list_proName")

    def find_product_title_node(self, product_item):
        return product_item

    def find_product_price_node(self, product_item):
        return product_item.parent.find("span", class_="price_sale")

    def parse_product_title(self, product_title_node):
        return product_title_node.text.replace("\n", "").replace("\t", "").strip()

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.find("a")["href"]


class SellerPcstoreCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(SellerPcstoreCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pdList_1"))
            )
            
	
    def find_all_product_items(self, soup):
        return soup.find_all("div", class_="pdbox")

    def find_product_title_node(self, product_item):
        return product_item.find("div", class_="name")

    def find_product_price_node(self, product_item):
        return product_item.find("div", class_="price")

    def parse_product_title(self, product_title_node):
        return product_title_node.text.replace("\n", "").replace("\t", "").strip()

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.find("a")["href"]

##########################################################################################
# 此網站特別不同，完全客製化
##########################################################################################
class CoolpcCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(CoolpcCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def retrieve(self, _browser):
        # 針對各產品各自搜尋
        result = list()
        error_messages = list()
        try:
            _browser.get(self._search_url)
            time.sleep(3)

            html = _browser.page_source # 獲取頁面原始碼，所有的
            # 使用BS進行分析
            soup = BeautifulSoup(html, features="html.parser")

            options = soup.find_all("option")

            for option in options:
                option_items = option.text.replace("◆ ", "").replace("★", "").replace("\n", "").strip().replace("元", "").split("$")
                if len(option_items) <= 1:
                    continue
                product_title = option_items[0]
                product_price = option_items[1]
                for _product in self._products:
                    if _product.verify(product_title) and _product.product_name.lower() in product_title.lower():
                        _record = Record(website=self._website_name, location=self._location_name, 
                        product=_product, title=product_title, price=float(product_price), standard_price=self.get_standard_price(_product), 
                        url=self._website_prefix, create_time=datetime.now(), 
                        is_verified=1 if float(product_price) >= self.get_standard_price(_product) else 0,total_number_of_product=1)

                        print(_record.url)
                        print(_record.title)
                        print(_record.price)

                        result.append(_record)
        except Exception as _exception:
            _log = CrawlLog.objects.create(log_time=datetime.now(), log_level="Error", website=self._website_name, location=self._location_name, 
            message=str(_exception) + " when search " + self._search_url)
            error_messages.append(_log)

        return result, error_messages

# Shopee & Shopee Mall are the same crawlers
class ShopeeCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(ShopeeCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "shopee-search-item-result"))
            )

    def find_all_product_items(self, soup):    
        # 蝦皮若沒有搜尋到，會預設顯示其他產品，造成誤判，必須判斷
        if "找不到" in soup.find("h1", class_="shopee-search-result-header").text:
            return []
        else:
            return soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")

    def find_product_title_node(self, product_item):
        return product_item.find("div", class_="_3GAFiR")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="_3c5u7X")

    def parse_product_title(self, product_title_node):
        return product_title_node.text.replace("\n", "").replace("\t", "").strip()

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.parent.parent.parent["href"]


class TaobaoCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(TaobaoCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "c1_t2i"))
            )

    def find_all_product_items(self, soup):
        return soup.find_all("div", class_="c2prKC")

    def find_product_title_node(self, product_item):
        return product_item.find("div", class_="c16H9d")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="c13VH6")

    def parse_product_title(self, product_title_node):
        return product_title_node.text.replace("\n", "").replace("\t", "").strip()

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.find("a")["href"]


class RutenCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(RutenCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flex"))
            )

    def find_all_product_items(self, soup):
        return soup.find_all("div", class_="product-item")

    def find_product_title_node(self, product_item):
        return product_item.find("div", class_="rt-goods-list-item-name")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="rt-text-price rt-text-bold text-price-dollar")

    def parse_product_title(self, product_title_node):
        return product_title_node.text.replace("\n", "").replace("\t", "").strip()

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.find("a")["href"]


class MyfoneCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(MyfoneCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "subCategory"))
            )

    def find_all_product_items(self, soup):
        product_items = soup.find_all("li", class_="categoryPdcSmall")
        product_items = [product_item for product_item in product_items if product_item.text.replace("\n", "").replace("\t", "").strip() != ""]
        return product_items

    def find_product_title_node(self, product_item):
        return product_item.find("p", class_="title")

    def find_product_price_node(self, product_item):
        return product_item.find("p", class_="price")

    def parse_product_title(self, product_title_node):
        return product_title_node.text.replace("\n", "").replace("\t", "").strip()

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent["href"]

    
# 需要使用 EC 價格檢查
class ETMallCrawler(CrawlerBase):
    def __init__(self, search_url, website_prefix, website_name, location_name, products, ignore_urls):
        super(ETMallCrawler, self).__init__(search_url, website_prefix, website_name, location_name, products, ignore_urls)

    def check_if_page_load_completely(self, _browser):
        element = WebDriverWait(_browser, 3).until(
                EC.presence_of_element_located((By.ID, "searchResult"))
            )

    # 網站如果查不到產品，會自動查到其他不相關的產品
    # 必須濾除
    # 濾除規則是出現 n-bg--gr2-dp-light n-m-bottom--xs m-top-sm padding-s
    # 另外為了控制查到不對的產品，要重新 fill out 不相關的產品
    def find_all_product_items(self, soup):        
        no_item_label = soup.find_all("div", class_="n-bg--gr2-dp-light n-m-bottom--xs m-top-sm padding-sm")
        # 如果有出現查不到產品，會自動查到其他不相關的產品，要停止
        if len(no_item_label) > 0:
            no_item_label.clear()
            return no_item_label

        search_text = soup.find("input", id="txtSearchKeyword")["value"]
        search_texts = search_text.split(" ")

        
        search_result = soup.find("div", id="searchResult")
        product_items = search_result.find_all("div", class_="n-card__box")
        product_items_all = soup.find_all("div", class_="n-card__box")

        remove_list = list()
        for _product in product_items:
            _product_title = self.find_product_title_node(_product)

            if _product_title is None:
                remove_list.append(_product)
                continue

            _title = self.parse_product_title(_product_title)

            for _text in search_texts:
                if _text.lower() not in _title.lower():
                    remove_list.append(_product)
                    break

        for _product in remove_list:
            product_items.remove(_product)

        return product_items

    def find_product_title_node(self, product_item):
        return product_item.find("p", class_="n-name")

    def find_product_price_node(self, product_item):
        return product_item.find("span", class_="n-price--16")

    def parse_product_title(self, product_title_node):
        return product_title_node.text.replace("\n", "").replace("\t", "").strip()

    def parse_product_detail_url(self, product_title_node):
        return product_title_node.parent.find("a")["href"]

    ##########################################################################################
    # 回傳標準產品價格，主要目的是 Momo & Pchome 要使用 EC 價格，但一般網站要用標準價格
    ##########################################################################################
    def get_standard_price(self, _product):
        return _product.product_standard_price_for_ecommerce

def __create_browser():    
    # 使用 Chrome 的 WebDriver
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    return browser

def _execute_crawler(browser, crawler_instance):
    result, error_messages = crawler_instance.retrieve(browser)
    browser.close()
    return result, error_messages

async def async_post(pool, loop, browser, crawler_instance):
    result_tuple = await loop.run_in_executor(pool, _execute_crawler, browser, crawler_instance)
    return result_tuple

async def run_executor(browser_list, crawler_instance_list):
    loop = asyncio.get_event_loop()
    tasks = []
    with ThreadPoolExecutor() as pool:
        for i in range(len(browser_list)):
            tasks.append(loop.create_task(async_post(pool, loop,browser_list[i] , crawler_instance_list[i])))
        result_tuples = await asyncio.gather(*tasks)
    return result_tuples  

def construct_crawler_instance(instance_list, instance):
    instance_list.append(instance)
####################################################################################
# Crawl Taiwan Website for GPU Price
####################################################################################
def retrieve_taiwan_gpu_website(products, ignore_urls):
    all_result = list()
    all_error_messages = list()
    
    crawler_instance_list = []
    construct_crawler_instance(crawler_instance_list, IsunfarCrawler("https://www.isunfar.com.tw/product/search.aspx?b=0&keyword={KEYWORD}#/bcNo=0&ept=0", "https://www.isunfar.com.tw", "isunfar", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, SinyaCrawler("https://www.sinya.com.tw/show/?keyword={KEYWORD}", "https://www.sinya.com.tw", "Sinya", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, RuifrostCrawler("http://www.ruifrost.com/rui/index.php", "http://www.ruifrost.com/rui/", "Ruifrost", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, MomoshopCrawler("https://www.momoshop.com.tw/search/searchShop.jsp?keyword={KEYWORD}&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType", "https://www.momoshop.com.tw", "Momo", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, PchomeCrawler("https://ecshweb.pchome.com.tw/search/v3.3/?q={KEYWORD}", "https:", "PCHome", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, EclifeCrawler("https://www.eclife.com.tw/Search/{KEYWORD}.html", "https://www.eclife.com.tw", "Eclife", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, DeyuanpcCrawler("http://deyuan-pc.com.tw/evaluate/", "http://deyuan-pc.com.tw/evaluate/", "Deyuan-PC", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, AutobuyCrawler("http://www.autobuy.tw/index.php", "https://www.autobuy.tw/", "Autobuy", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, YahooMallCrawler("https://tw.search.mall.yahoo.com/search/mall/product?kw={KEYWORD}&p={KEYWORD}&cid=0&clv=0", "", "YahooMall", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, YahooBuyCrawler("https://tw.buy.yahoo.com/search/product?p={KEYWORD}", "", "YahooBuy", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, PcstoreCrawler("https://www.pcstore.com.tw/ispc", "https://www.pcstore.com.tw", "PCStore", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, SellerPcstoreCrawler("https://seller.pcstore.com.tw/search/prodList.htm#psearch&sort=0&page=1&keyword={KEYWORD}&skopt=1&opt=0", "", "SellerPCStore", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, CoolpcCrawler("https://www.coolpc.com.tw/evaluate.php", "https://www.coolpc.com.tw/evaluate.php", "CoolPC", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, YahooBidCrawler("https://tw.bid.yahoo.com/search/auction/product?kw={KEYWORD}&p={KEYWORD}&cid=0&clv=0", "", "YahooBid", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, ShopeeCrawler("https://shopee.tw/search?keyword={KEYWORD}", "https://shopee.tw", "Shopee", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, RutenCrawler("https://find.ruten.com.tw/s/?bidway=all&q={KEYWORD}", "", "Ruten", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, MyfoneCrawler("https://search.myfone.com.tw/searchResult.php?sort_id=&keyword={KEYWORD}", "", "Myfone", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, ETMallCrawler("https://www.etmall.com.tw/Search?keyword={KEYWORD}", "https://www.etmall.com.tw", "ETMall", "Taiwan", products, ignore_urls))
    
    browser_list = []
    for i in range(len(crawler_instance_list)):
        browser = __create_browser()
        browser_list.append(browser)
    
    result_tuples = asyncio.run(run_executor(browser_list, crawler_instance_list))   
    for retrieve_result, error_messages in result_tuples:
        all_result.extend(retrieve_result)
        all_error_messages.extend(error_messages)

    return all_result, all_error_messages

def retrieve_taiwan_tire_website(products, ignore_urls):
    all_result = list()
    all_error_messages = list()
    
    crawler_instance_list = []
    construct_crawler_instance(crawler_instance_list, MomoshopCrawler("https://www.momoshop.com.tw/search/searchShop.jsp?keyword={KEYWORD}&searchType=1&curPage=1&_isFuzzy=0&showType=chessboardType", "https://www.momoshop.com.tw", "Momo", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, PchomeCrawler("https://ecshweb.pchome.com.tw/search/v3.3/?q={KEYWORD}", "https:", "PCHome", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, YahooMallCrawler("https://tw.search.mall.yahoo.com/search/mall/product?kw={KEYWORD}&p={KEYWORD}&cid=0&clv=0", "", "YahooMall", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, YahooBuyCrawler("https://tw.buy.yahoo.com/search/product?p={KEYWORD}", "", "YahooBuy", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, YahooBidCrawler("https://tw.bid.yahoo.com/search/auction/product?kw={KEYWORD}&p={KEYWORD}&cid=0&clv=0", "", "YahooBid", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, ShopeeCrawler("https://shopee.tw/search?keyword={KEYWORD}", "https://shopee.tw", "Shopee", "Taiwan", products, ignore_urls))
    construct_crawler_instance(crawler_instance_list, RutenCrawler("https://find.ruten.com.tw/s/?bidway=all&q={KEYWORD}", "", "Ruten", "Taiwan", products, ignore_urls))

    browser_list = []
    for i in range(len(crawler_instance_list)):
        browser = __create_browser()
        browser_list.append(browser)
    
    result_tuples = asyncio.run(run_executor(browser_list, crawler_instance_list))   
    for retrieve_result, error_messages in result_tuples:
        all_result.extend(retrieve_result)
        all_error_messages.extend(error_messages)

    return all_result, all_error_messages