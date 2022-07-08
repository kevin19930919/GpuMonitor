from django.contrib import admin

# Register your models here.
import cores.models

admin.site.register(cores.models.Service, cores.models.ServiceAdmin)
admin.site.register(cores.models.Product, cores.models.ProductAdmin)
admin.site.register(cores.models.Record, cores.models.RecordAdmin)
admin.site.register(cores.models.CrawlLog, cores.models.CrawlLogAdmin)
admin.site.register(cores.models.IgnoreUrl, cores.models.IgnoreUrlAdmin)

admin.site.site_header = 'GPU Monitoring'
admin.site.site_title = 'GPU Monitoring'
admin.site.index_title = 'GPU Monitoring'