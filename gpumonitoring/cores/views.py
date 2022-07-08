from django.shortcuts import render
import pandas as pd
# Create your views here.
# specific to this view
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, UpdateView
from django.http import HttpResponse,JsonResponse
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from PIL import Image, ImageDraw
from django.db.models import Q, F, Avg, Count
from django.contrib.auth.decorators import permission_required
from datetime import datetime, timedelta

@login_required
def overview(request):
    return render(request, 'cores/overview.html')

# #######################################################################################################################
# #function for create defect mode map
# #######################################################################################################################
# def create_mapping_dict(ai_defect_transform,human_defect_tranform):
#     defect_mode_mapping_list = DefectModeMapping.objects.all()

#     for defect_mode_mapping in defect_mode_mapping_list:
#         if defect_mode_mapping.data_type == "AI":
#             ai_defect_transform[defect_mode_mapping.key] = defect_mode_mapping.token
#         elif defect_mode_mapping.data_type == "HUMAN":
#             human_defect_tranform[defect_mode_mapping.key] = defect_mode_mapping.token

#     return ai_defect_transform, human_defect_tranform 

# ##########################################################################################################################
# # AIPerformance List View
# ##########################################################################################################################
# @method_decorator(login_required, name='dispatch')
# class AIPerformanceListView(ListView):
#     model = AIPerformance
#     template_name = 'cores/aiperformance-list.html'
#     context_object_name = 'performances'
#     paginate_by = 30
    
#     @method_decorator(permission_required('cores.view_aiperformance', raise_exception=True))
#     def dispatch(self, request):
#         return super(AIPerformanceListView, self).dispatch(request)

#     def get_context_data(self, **kwargs):
#         context = super(AIPerformanceListView, self).get_context_data(**kwargs)
#         performances = self.get_queryset()
#         page = self.request.GET.get('page')
#         paginator = Paginator(performances, self.paginate_by)
#         try:
#             performances = paginator.page(page)
#         except PageNotAnInteger:
#             performances = paginator.page(1)
#         except EmptyPage:
#             performances = paginator.page(paginator.num_pages)
#         context['performances'] = performances
#         return context

#     def get_queryset(self):
#         q_from_start_time = self.request.GET.get('q_from_start_time')
#         q_to_start_time = self.request.GET.get('q_to_start_time')

        
#         if q_from_start_time:
#             q_from_start_time = q_from_start_time.replace("/", "-")
#         if q_to_start_time:
#             q_to_start_time = q_to_start_time.replace("/", "-")

#         if q_from_start_time and q_to_start_time:
#             performances = AIPerformance.objects.filter(log_start_time__range=[q_from_start_time, q_to_start_time])
#         elif q_from_start_time:
#             performances = AIPerformance.objects.filter(log_start_time__gte=q_from_start_time)
#         elif q_to_start_time:
#             performances = AIPerformance.objects.filter(log_start_time__lte=q_to_start_time)
#         else:
#             performances = AIPerformance.objects.all()

#         return performances



# ##########################################################################################################################
# # 繪製 AI Performance Time Series Chart
# ##########################################################################################################################
# @login_required
# @permission_required('cores.view_aiperformance', raise_exception=True)
# def aiperformance_chart(request):
#     q_from_start_time = request.GET.get('q_from_start_time')
#     q_to_start_time = request.GET.get('q_to_start_time')
    
#     return render(request, 'cores/aiperformance_chart.html', {
#         'data': _retrieve_aiperformance_time_sereis_data(q_from_start_time, q_to_start_time),
#     })

# def _retrieve_aiperformance_time_sereis_data(q_from_start_time, q_to_start_time):
#     if q_from_start_time:
#         q_from_start_time = q_from_start_time.replace("/", "-")
#     if q_to_start_time:
#         q_to_start_time = q_to_start_time.replace("/", "-")
    
#     if q_from_start_time and q_to_start_time:
#         performances = AIPerformance.objects.filter(log_start_time__range=[q_from_start_time, q_to_start_time],latest=1)
#     elif q_from_start_time:
#         performances = AIPerformance.objects.filter(log_start_time__gte=q_from_start_time,latest=1)
#     elif q_to_start_time:
#         performances = AIPerformance.objects.filter(log_start_time__lte=q_to_start_time,latest=1)
#     else:
#         performances = AIPerformance.objects.filter(latest=1)   

#     labels = list()
#     data = list()
#     timechart_data = list()
#     for performance in performances:
#         labels.append(performance.log_start_time.strftime("%Y/%m/%d %H:%M:%S"))
#         data.append(performance.performance_value)
#         timechart_data.append({"x":performance.log_start_time.strftime("%Y/%m/%d %H:%M:%S") + " GMT", "y":round(performance.performance_value,2)})
#     timechart_data = sorted(timechart_data, key = lambda x : x["x"])
#     return timechart_data

# ##########################################################################################################################
# # AIAutovsResult List View
# ##########################################################################################################################
# @method_decorator(login_required, name='dispatch')
# class AIAutovsResultListView(ListView):
#     model = AIAutovsResult
#     template_name = 'cores/aiautovsresult-list.html'
#     context_object_name = 'autovsresults'
#     paginate_by = 30

    
#     @method_decorator(permission_required('cores.view_aiautovsresult', raise_exception=True))
#     def dispatch(self, request):
#         return super(AIAutovsResultListView, self).dispatch(request)

#     def get_context_data(self, **kwargs):
#         context = super(AIAutovsResultListView, self).get_context_data(**kwargs)
#         autovsresults = self.get_queryset()
#         page = self.request.GET.get('page')
#         paginator = Paginator(autovsresults, self.paginate_by)
#         try:
#             autovsresults = paginator.page(page)
#         except PageNotAnInteger:
#             autovsresults = paginator.page(1)
#         except EmptyPage:
#             autovsresults = paginator.page(paginator.num_pages)
#         context['autovsresults'] = autovsresults
#         return context

#     def get_queryset(self):
#         q_from_create_time = self.request.GET.get('q_from_create_time')
#         q_to_create_time = self.request.GET.get('q_to_create_time')
#         q_part_number = self.request.GET.get('q_part_number')
#         q_lot_number = self.request.GET.get('q_lot_number')
#         q_serial_number = self.request.GET.get('q_serial_number')
        
#         if q_from_create_time:
#             q_from_create_time = q_from_create_time.replace("/", "-")
#         if q_to_create_time:
#             q_to_create_time = q_to_create_time.replace("/", "-")

#         if q_from_create_time and q_to_create_time:
#             autovsresults = AIAutovsResult.objects.filter(create_time__range=[q_from_create_time, q_to_create_time])
#         elif q_from_create_time:
#             autovsresults = AIAutovsResult.objects.filter(create_time__gte=q_from_create_time)
#         elif q_to_create_time:
#             autovsresults = AIAutovsResult.objects.filter(create_time__lte=q_to_create_time)
#         else:
#             autovsresults = AIAutovsResult.objects.all()

#         if q_part_number:
#             autovsresults = autovsresults.filter(part_number__contains=q_part_number)
#         if q_lot_number:
#             autovsresults = autovsresults.filter(lot_number__contains=q_lot_number)
#         if q_serial_number:
#             autovsresults = autovsresults.filter(serial_number__contains=q_serial_number)
        
#         return autovsresults


# ##########################################################################################################################
# # 繪製 AIAutovsResult Confusion matrix
# ##########################################################################################################################
# @login_required
# @permission_required('cores.view_aiautovsresult', raise_exception=True)
# def aiautovsresult_chart(request):
#     q_from_create_time = request.GET.get('q_from_create_time')
#     q_to_create_time = request.GET.get('q_to_create_time')

#     return render(request, 'cores/aiautovsresult_chart.html', {
#         'series': _retrieve_aiautovsresult_confusion_matrix_data(q_from_create_time, q_to_create_time),
#     })

# def _retrieve_aiautovsresult_confusion_matrix_data(q_from_create_time, q_to_create_time):
#     if q_from_create_time:
#         q_from_create_time = q_from_create_time.replace("/", "-")
#     if q_to_create_time:
#         q_to_create_time = q_to_create_time.replace("/", "-")

#     if q_from_create_time and q_to_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__range=[q_from_create_time, q_to_create_time])
#     elif q_from_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__gte=q_from_create_time)
#     elif q_to_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__lte=q_to_create_time)
#     else:
#         autovsresults = AIAutovsResult.objects.all()

    
#     time_flag_start = datetime.now()

#     ai_defect_transform = dict()
#     human_defect_transform = dict()
#     ai_defect_transform, human_defect_transform = create_mapping_dict(ai_defect_transform, human_defect_transform)
    
#     # 2. 高效能方法，利用資料庫計算 is_ai_correct 欄位的總和
#     heatmap = dict()
#     defect_mode_set = set()

#     autovsresults = autovsresults.values('ai_defect_mode', 'human_defect_mode').annotate(the_count=Count('is_ai_correct'))

#     for autovsresult in autovsresults:
#         if autovsresult['ai_defect_mode'] in ai_defect_transform and autovsresult['human_defect_mode'] in human_defect_transform:
#             key = ai_defect_transform[autovsresult['ai_defect_mode']] + "." + human_defect_transform[autovsresult['human_defect_mode']]
#             defect_mode_set.add(ai_defect_transform[autovsresult['ai_defect_mode']])
#             defect_mode_set.add(human_defect_transform[autovsresult['human_defect_mode']])
#             if key not in heatmap:
#                 heatmap[key] = 0  
#             heatmap[key] = heatmap[key] + autovsresult['the_count']

#     defect_names = list(defect_mode_set)
#     defect_names.sort()

#     # 繪圖
#     series = list()
#     for i in range(len(defect_names)):
#         item = dict()
#         item["name"] = defect_names[i]
#         item["data"] = list()
#         for j in range(len(defect_names)):
#             key = defect_names[i] + "." + defect_names[j]
#             quantity = 0
#             if key in heatmap:
#                 quantity = heatmap[key]
#             item["data"].append({"x":defect_names[j], "y":quantity})
#         series.append(item)
#     series.reverse()    
    
#     time_flag_end = datetime.now()
#     #print((time_flag_end - time_flag_start).seconds)

#     return series

# ##########################################################################################################################
# # 繪製 AIAutovsResult Confusion matrix
# ##########################################################################################################################
# @login_required
# @permission_required('cores.view_aiautovsresult', raise_exception=True)
# def aiautovsresult_timechart(request):
#     q_from_create_time = request.GET.get('q_from_create_time')
#     q_to_create_time = request.GET.get('q_to_create_time')
    
#     return render(request, 'cores/aiautovsresult_timechart.html', {
#         'data': _retrieve_aiautovsresult_time_series_data(q_from_create_time, q_to_create_time),
#     })

# def _retrieve_aiautovsresult_time_series_data(q_from_create_time, q_to_create_time):
#     if q_from_create_time:
#         q_from_create_time = q_from_create_time.replace("/", "-")
#     if q_to_create_time:
#         q_to_create_time = q_to_create_time.replace("/", "-")

#     if q_from_create_time and q_to_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__range=[q_from_create_time, q_to_create_time])
#     elif q_from_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__gte=q_from_create_time)
#     elif q_to_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__lte=q_to_create_time)
#     else:
#         autovsresults = AIAutovsResult.objects.all()

#     time_flag_start = datetime.now()

#     # 統計辨識結果，以時間 (create_time) 為維度統計 (正確, 錯誤)
#     static_dict = dict()
    
#     # 2. 高效能方法，利用資料庫計算 is_ai_correct 欄位的平均值
#     autovsresults = autovsresults.values('create_time').annotate(accuracy=Avg('is_ai_correct'))
    
#     time_flag_end = datetime.now()
#     #print((time_flag_end - time_flag_start).seconds)
#     time_flag_start = datetime.now()

#     for autovsresult in autovsresults:
#         static_dict[autovsresult["create_time"]] = autovsresult["accuracy"]

    
#     time_flag_end = datetime.now()
#     #print((time_flag_end - time_flag_start).seconds)
#     time_flag_start = datetime.now()


#     timechart_data = list()
#     for key, value in static_dict.items():
#         # timechart_data.append({"x":key.strftime("%Y/%m/%d %H:%M:%S"), "y":value[0] / (value[0] + value[1])})
#         timechart_data.append({"x":key.strftime("%Y/%m/%d %H:%M:%S") + " GMT", "y":round(value, 2)})

#     timechart_data = sorted(timechart_data, key = lambda x : x["x"])
#     return timechart_data


# ##########################################################################################################################
# # 繪製 AIAutovsResult AI Defect Mode Chart
# ##########################################################################################################################
# def _retrieve_aiautovsresult_ai_defect_mode_data(q_from_create_time, q_to_create_time):
#     if q_from_create_time:
#         q_from_create_time = q_from_create_time.replace("/", "-")
#     if q_to_create_time:
#         q_to_create_time = q_to_create_time.replace("/", "-")

#     if q_from_create_time and q_to_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__range=[q_from_create_time, q_to_create_time])
#     elif q_from_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__gte=q_from_create_time)
#     elif q_to_create_time:
#         autovsresults = AIAutovsResult.objects.filter(create_time__lte=q_to_create_time)
#     else:
#         autovsresults = AIAutovsResult.objects.all()

#     time_flag_start = datetime.now()

#     ai_defect_transform = dict()
#     human_defect_transform = dict()
#     ai_defect_transform, human_defect_transform = create_mapping_dict(ai_defect_transform, human_defect_transform)
    
#     # 2. 高效能方法，利用資料庫計算 is_ai_correct 欄位的總和
#     autovsresults = autovsresults.values('ai_defect_mode').annotate(the_count=Count('is_ai_correct'))

#     series = list()
#     categories = list()
#     for autovsresult in autovsresults:
#         if autovsresult['ai_defect_mode'] in ai_defect_transform:
#             categories.append(ai_defect_transform[autovsresult['ai_defect_mode']])
#             series.append(autovsresult['the_count'])
    
#     time_flag_end = datetime.now()
#     #print((time_flag_end - time_flag_start).seconds)

#     return {'categories':categories, 'data':series}

# @method_decorator(login_required, name='dispatch')
# class AIConfigListView(ListView):
#     model = AIConfig
#     template_name = 'cores/aiconfig-list.html'
#     context_object_name = 'aiconfigs'
#     paginate_by = 20

#     @method_decorator(permission_required('cores.view_aiconfig', raise_exception=True))
#     def dispatch(self, request):
#         return super(AIConfigListView, self).dispatch(request)

#     def get_context_data(self, **kwargs):
#         context = super(AIConfigListView, self).get_context_data(**kwargs)
#         aiconfigs = self.get_queryset()
#         page = self.request.GET.get('page')
#         paginator = Paginator(aiconfigs, self.paginate_by)
#         try:
#             aiconfigs = paginator.page(page)
#         except PageNotAnInteger:
#             aiconfigs = paginator.page(1)
#         except EmptyPage:
#             aiconfigs = paginator.page(paginator.num_pages)
#         context['aiconfigs'] = aiconfigs
#         return context

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         if query:
#             return AIConfig.objects.filter(key__contains=query)
#         else:
#             return AIConfig.objects.all()


# @method_decorator(login_required, name='dispatch')
# class AIConfigUpdateView(UpdateView):
#     model = AIConfig
#     template_name = 'cores/aiconfig-update.html'
#     context_object_name = 'aiconfig'
#     fields = ('key', 'token', 'description','readonly')

    
#     @method_decorator(permission_required('cores.change_aiconfig', raise_exception=True))
#     def dispatch(self, request):
#         return super(AIConfigUpdateView, self).dispatch(request)

#     def get_success_url(self):
#         return reverse_lazy('aiconfig-list')


# @login_required
# @permission_required('cores.change_aiconfig', raise_exception=True)
# def aiconfig_updatelist(request):
#     if request.POST.get("button_type") == "Save":
#         # 讀取 POST 內的資料更新置資料庫
#         _objects = __parseObjects(request.POST, "aiconfig")
#         for _id, _entity_data in _objects.items():
#             AIConfig.objects.filter(id=_id).update(**_entity_data)


#     query = request.POST.get('query')
#     if query:
#         aiconfig_set = AIConfig.objects.filter(key__contains=query, readonly=False)
#     else:
#         query = ""
#         aiconfig_set = AIConfig.objects.filter(readonly=False)

#     return render(request, 'cores/aiconfig-updatelist.html', {
#         'aiconfig_set': aiconfig_set,
#         'query' : query
#     })

# def __parseObjects(_post, class_name):
#     data = dict()
#     for key, value in _post.items():
#         if key.startswith(class_name):
#             attr_id = key.replace(class_name + "_", "")
#             id = attr_id.split("_")[-1]
#             attr = attr_id.replace("_" + id, "")
#             if id not in data:
#                 data[id] = dict()
#             data[id][attr] = value
#     return data


# @method_decorator(login_required, name='dispatch')
# class DefectModeMappingListView(ListView):
#     model = DefectModeMapping
#     template_name = 'cores/defectmodemap-list.html'
#     context_object_name = 'defectmodemaps'
#     paginate_by = 20

    
#     @method_decorator(permission_required('cores.view_defectmodemapping', raise_exception=True))
#     def dispatch(self, request):
#         return super(DefectModeMappingListView, self).dispatch(request)

#     def get_context_data(self, **kwargs):
#         context = super(DefectModeMappingListView, self).get_context_data(**kwargs)
#         defectmodemaps = self.get_queryset()
#         page = self.request.GET.get('page')
#         paginator = Paginator(defectmodemaps, self.paginate_by)
#         try:
#             defectmodemaps = paginator.page(page)
#         except PageNotAnInteger:
#             defectmodemaps = paginator.page(1)
#         except EmptyPage:
#             defectmodemaps = paginator.page(paginator.num_pages)
#         context['defectmodemaps'] = defectmodemaps
#         return context

#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         if query:
#             return DefectModeMapping.objects.filter(Q(key__contains=query)|Q(token__contains=query)|Q(data_type__contains=query))
#         else:
#             return DefectModeMapping.objects.all()

# @method_decorator(login_required, name='dispatch')
# class DefectModeMappingUpdateView(UpdateView):
#     model = DefectModeMapping
#     template_name = 'cores/defectmodemap-update.html'
#     context_object_name = 'defectmodemap'
#     fields = ('key', 'token', 'data_type')

    
#     @method_decorator(permission_required('cores.update_defectmodemapping', raise_exception=True))
#     def dispatch(self, request):
#         return super(DefectModeMappingUpdateView, self).dispatch(request)

#     def get_success_url(self):
#         return reverse_lazy('defectmodemap-list')


# @login_required
# @permission_required('cores.change_defectmodemapping', raise_exception=True)
# def defectmodemap_updatelist(request):
#     if request.POST.get("button_type") == "Save":
#         # 讀取 POST 內的資料更新置資料庫
#         _objects = __parseObjects(request.POST, "defectmodemap")
#         for _id, _entity_data in _objects.items():
#             DefectModeMapping.objects.filter(id=_id).update(**_entity_data)


#     query = request.POST.get('query')
#     if query:
#         defectmodemap_set = DefectModeMapping.objects.filter(Q(key__contains=query)|Q(token__contains=query)|Q(data_type__contains=query))
#         #defectmodemap_set = DefectModeMapping.objects.filter(Q(token__contains=query))
#     else:
#         query = ""
#         defectmodemap_set = DefectModeMapping.objects.all()

#     return render(request, 'cores/defectmodemap-updatelist.html', {
#         'defectmodemap_set': defectmodemap_set,
#         'query' : query
#     }) 

# @login_required
# @permission_required('cores.change_aiconfig', raise_exception=True)
# def areadetectionsetting_edit(request):
#     if request.method == "POST":
#         if request.POST.get("button_type") == "Save":
#             # 檢查是否有圖檔，有圖檔則儲存，儲存成 demo.jpg
#             demo_img = request.FILES.get('demo_image')
#             if demo_img:
#                 if default_storage.exists('demo.jpg'):
#                     default_storage.delete('demo.jpg')
#                 default_storage.save('demo.jpg', ContentFile(demo_img.read()))

#             # 儲存設定的圖片寬與高
#             setting_width = request.POST.get('setting_width')
#             setting_height = request.POST.get('setting_height')

#             # Read demo.jpg and draw rectangle then save
#             image_width = 0
#             image_height = 0
#             if default_storage.exists('demo.jpg'):
#                 img = Image.open(default_storage.path('demo.jpg'))
#                 if img:
#                     image_width = img.width
#                     image_height = img.height
                    
#                     if int(setting_width) > image_width:
#                         setting_width = str(image_width)
#                     if int(setting_height) > image_height:
#                         setting_height = str(image_height)
#                     # 進行畫框作業，並且儲存成 demo-with-line.jpg
#                     if setting_width and setting_height and image_width and image_height:
#                         shape = [((image_width - int(setting_width))//2, (image_height - int(setting_height))//2), 
#                         ((image_width + int(setting_width))//2, (image_height + int(setting_height))//2)]
#                         ImageDraw.Draw(img).rectangle(shape, outline="red", width=2)
#                         img.save(default_storage.path('demo.jpg').replace('demo.jpg', "demo-with-line.jpg"), "JPEG")
            
#             AIConfig.objects.filter(key="area_detection_width").update(token=str(setting_width))
#             AIConfig.objects.filter(key="area_detection_height").update(token=str(setting_height))
    
#     # 準備送往前端的數據
    
#     # 查詢目前 config 中所設定的數值
#     _query = AIConfig.objects.filter(key="area_detection_width")

#     if len(_query) == 1:
#         setting_width = _query[0].token

#     _query = AIConfig.objects.filter(key="area_detection_height")

#     if len(_query) == 1:
#         setting_height = _query[0].token

#     # Read demo.jpg and draw rectangle then save
#     image_width = 0
#     image_height = 0
#     if default_storage.exists('demo.jpg'):
#         img = Image.open(default_storage.path('demo.jpg'))
#         if img:
#             image_width = img.width
#             image_height = img.height

#     return render(request, 'cores/areadetectionsetting_edit.html', 
#     {
#         'image_width': image_width,
#         'image_height': image_height,
#         'setting_width': setting_width,
#         'setting_height': setting_height
#     })
