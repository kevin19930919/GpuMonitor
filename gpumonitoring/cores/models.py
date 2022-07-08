from django.db import models
from django.contrib import admin


####################################################################################
# 顯示服務
####################################################################################
class Service(models.Model):
    service_name = models.CharField(max_length=200, null=False)

    security_token = models.CharField(max_length=200, null=True)
    
    description = models.CharField(max_length=200, null=True, default='')

    navigation_link = models.CharField(max_length=200, null=True, default='')

    sorted_index = models.IntegerField(default=0)

    def __str__(self):
        """String for representing the Model object."""
        return self.service_name + "-" + self.description + "-" + str(self.sorted_index)

    class Meta:
        verbose_name_plural = 'Service'



class ServiceAdmin(admin.ModelAdmin):

    search_fields = ['service_name', 'security_token', 'description', 'navigation_link']

####################################################################################
# 監控產品
####################################################################################
class Product(models.Model):
    product_id = models.CharField(max_length=100, null=True)

    product_name = models.CharField(max_length=100, null=False)

    product_standard_price = models.FloatField()

    product_standard_price_for_ecommerce = models.FloatField(default=0)

    must_in_keywords = models.CharField(max_length=200, null=False)

    must_out_keywords = models.CharField(max_length=200, null=True, default="")

    location = models.CharField(max_length=100, null=False, default="Taiwan")

    watching = models.BooleanField(null=False, default=True)
    
    category = models.CharField(max_length=100, null=False, default="Quadro")

    # 進行輸入文字檢查，是否正確屬於此產品
    def verify(self, description):
        # must_out_keywords 列表文字必須均不存在於 description
        items = self.must_out_keywords.lower().split(";")

        for item in items:
            if item.lower() in description.lower():
                return False

        # must_in_keywords 
        # 以 [] 做群組區隔，[] 內的列表必須至少有一個文字存在於 description
        # 群組之間以 ; 分隔，群組間以 , 分隔
        true_return_value_count = 0

        items = self.must_in_keywords.lower().split(";")

        for item in items:
            subitems = item.replace("[", "").replace("]", "").split(",")

            sub_return_value = False
            for subitem in subitems:
                if subitem.lower() in description.lower():
                    sub_return_value = True
                    break
            
            if sub_return_value:
                true_return_value_count = true_return_value_count + 1
            

        return true_return_value_count == len(items)


    def __str__(self):
        """String for representing the Model object."""
        return self.product_name + "@" + self.location + " wih Standard Price:" + str(self.product_standard_price)

    class Meta:
        verbose_name_plural = 'Product'

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name', 'product_standard_price', 'must_in_keywords', 'must_out_keywords', 'location']

####################################################################################
# 每天爬網價格紀錄
####################################################################################
class Record(models.Model):
    website = models.CharField(max_length=100, null=False)

    location = models.CharField(max_length=100, null=False)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='records')
    
    title = models.CharField(max_length=300, null=False)

    price = models.FloatField(null=False)
    
    standard_price = models.FloatField(null=True)
    
    url = models.CharField(max_length=300, null=False)

    create_time = models.DateTimeField()
    
    is_verified = models.FloatField(default=1)

    # 紀錄此查詢查到多少相關產品數量
    total_number_of_product = models.FloatField(null=False, default=0)

    def __str__(self):
        """String for representing the Model object."""
        return self.website + "." + self.title + "." + str(self.create_time)

    class Meta:
        verbose_name_plural = 'Record'


class RecordAdmin(admin.ModelAdmin):
    search_fields = ['website', 'location', 'product', 'website', 'title', 'price', 'url', 'create_time', 'is_verified']


####################################################################################
# 每天爬網統計資訊
####################################################################################
class StatisticsRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='statistics_records')

    average_price = models.FloatField(null=False)
    
    standard_deviation_price = models.FloatField(null=True)
    
    max_price = models.FloatField(null=True)
    
    min_price = models.FloatField(null=True)

    create_time = models.DateTimeField()

    def __str__(self):
        """String for representing the Model object."""
        return str(self.product) + "." + str(self.create_time)

    class Meta:
        verbose_name_plural = 'StatisticsRecord'



class StatisticsRecordAdmin(admin.ModelAdmin):
    search_fields = ['product', 'average_price', 'standard_deviation_price', 'max_price', 'min_price', 'create_time']

####################################################################################
# 爬網 Log 記錄
####################################################################################
class CrawlLog(models.Model):
    log_time = models.DateTimeField()
    
    log_level = models.CharField(max_length=20, null=False)

    website = models.CharField(max_length=100, null=False)

    location = models.CharField(max_length=100, null=False)
    
    message = models.CharField(max_length=500, null=False)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.log_time) + "." + self.log_level + "." + self.website + "." + self.location
        
    class Meta:
        verbose_name_plural = 'CrawlLog'

class CrawlLogAdmin(admin.ModelAdmin):
    search_fields = ['website', 'location', 'message', 'log_time']

####################################################################################
# 忽略 URL 清單
####################################################################################
class IgnoreUrl(models.Model):    
    url = models.CharField(max_length=500, null=False)

    create_time = models.DateTimeField()

    def __str__(self):
        """String for representing the Model object."""
        return self.url + "." + str(self.create_time)

    class Meta:
        verbose_name_plural = 'IgnoreUrl'


class IgnoreUrlAdmin(admin.ModelAdmin):
    search_fields = ['url', 'create_time']