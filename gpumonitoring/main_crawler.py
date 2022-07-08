##########################################################################################
# Main function of crwaler
##########################################################################################
from audioop import avg
import os
import django
from django.db import connections
from numpy import std
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpumonitoring.settings')
django.setup()

from crawlers.tw import retrieve_taiwan_gpu_website, retrieve_taiwan_tire_website
from cores.models import Product, Record, IgnoreUrl, StatisticsRecord
from mail_sender import send_mail, get_simple_list_text_from_records, get_text_from_records, get_text_from_crawllogs
import config
import numpy as np
from datetime import datetime
import time

def close_old_connections():
    [conn.close_if_unusable_or_obsolete for conn in connections.all()]


####################################################################################
# 查詢台灣 Quadro 網路價格
####################################################################################
def __monitoring_quadro_price():
    products = Product.objects.filter(watching=1).filter(category="Quadro")
    ignore_urls = IgnoreUrl.objects.all()
    ignore_urls = [item.url for item in ignore_urls]
    
    # Start to crawl Taiwan Websites
    # return_logs = list()
    result , return_logs= retrieve_taiwan_gpu_website(products, ignore_urls)
    # Filter out abnormal data and send email
    result = [item for item in result if item.is_verified == 0]
    
    # Write the result of crawling Taiwan Website
    # stop old connection first
    close_old_connections()
    try:
        Record.objects.bulk_create(result)
    except Exception as _exception:
        pass

    if result:
        _recievers = config.tw_quadro_notifiation_list.split(";")

        for _reciever in _recievers:
            send_mail(config.from_sender, _reciever, config.tw_quadro_notifiation_subject, get_text_from_records(result))
        
    return_logs = [item for item in return_logs if item.log_level == "Error"]


    if return_logs:
        _recievers = config.quadro_error_report_list.split(";")

        for _reciever in _recievers:
            send_mail(config.from_sender, _reciever, config.quadro_error_report_subject, get_text_from_crawllogs(return_logs))



####################################################################################
# 查詢台灣輪胎網路價格
####################################################################################
def __monitoring_tire_price():
    products = Product.objects.filter(watching=1).filter(category="Tire")
    ignore_urls = IgnoreUrl.objects.all()
    ignore_urls = [item.url for item in ignore_urls]
    
    # Start to crawl Taiwan Websites
    # return_logs = list()
    result , return_logs= retrieve_taiwan_tire_website(products, ignore_urls)
    
    # Filter out abnormal data and send email
    result = [item for item in result if item.is_verified == 0]
    
    # Write the result of crawling Taiwan Website
    # stop old connection first
    close_old_connections()
    try:
        Record.objects.bulk_create(result)
    except Exception as _exception:
        pass

    if result:
        _recievers = config.tw_tire_notifiation_list.split(";")

        for _reciever in _recievers:
            send_mail(config.from_sender, _reciever, config.tw_tire_notifiation_subject, get_text_from_records(result))
        
    return_logs = [item for item in return_logs if item.log_level == "Error"]


    if return_logs:
        _recievers = config.tire_error_report_list.split(";")

        for _reciever in _recievers:
            send_mail(config.from_sender, _reciever, config.tire_error_report_subject, get_text_from_crawllogs(return_logs))


####################################################################################
# 查詢 ASUS, ZOTAC, Gigabyte, MSI
####################################################################################
def __monitoring_competitor_geforce_price():
    products = Product.objects.filter(watching=1).filter(category="Geforce")
    
    # Start to crawl Taiwan Websites
    result , return_logs= retrieve_taiwan_gpu_website(products, ignore_urls)
    # return_logs = list()
    # result = retrieve_taiwan_gpu_website(products, [])
    
    # Write the result of crawling Taiwan Website
    # stop old connection first
    close_old_connections()
    try:
        Record.objects.bulk_create(result)
    except Exception as _exception:
        pass

    if result:
        # 統計整理 Result 相關的所有資訊
        statistics = dict()

        statistics_text = ""

        # 同時轉換成 StatisticsRecord
        statistic_records = list()
        for product in products:
            statistics[product.product_name] = [record.price for record in result if record.product == product]

            _max_price = np.around(np.max(np.array(statistics[product.product_name])), 1)
            _min_price = np.around(np.min(np.array(statistics[product.product_name])), 1)
            _average_price = np.around(np.mean(np.array(statistics[product.product_name])), 1)
            _std_price = np.around(np.std(np.array(statistics[product.product_name])), 1)

            statistics_text += product.product_name + "\n"
            statistics_text += "Max: " + str(_max_price) + "\n"
            statistics_text += "Min: " + str(_min_price) + "\n"
            statistics_text += "Average: " + str(_average_price) + "\n"
            statistics_text += "Standard Deviation: " + str(_std_price) + "\n\n\n"

            _statistic_record = StatisticsRecord(product=product, average_price = _average_price, 
            standard_deviation_price = _std_price, max_price = _max_price, min_price = _min_price, create_time=datetime.now())

            statistic_records.append(_statistic_record)

        
        close_old_connections()
        try:
            StatisticsRecord.objects.bulk_create(statistic_records)
        except Exception as _exception:
            pass          

        _recievers = config.tw_competitor_geforce_notifiation_list.split(";")

        for _reciever in _recievers:
            send_mail(config.from_sender, _reciever, config.tw_competitor_geforce_notifiation_subject, statistics_text + get_simple_list_text_from_records(result))
        
    return_logs = [item for item in return_logs if item.log_level == "Error"]


    if return_logs:
        _recievers = config.competitor_geforce_error_report_list.split(";")

        for _reciever in _recievers:
            send_mail(config.from_sender, _reciever, config.competitor_geforce_error_report_subject, get_text_from_crawllogs(return_logs))


def main():
    t1 = time.time()
    __monitoring_quadro_price()
    __monitoring_tire_price()
    __monitoring_competitor_geforce_price()
    print(f"total cost time:{time.time() - t1}")

if __name__ == '__main__':
    main()
