from django.conf.urls import url
from django.urls import path

import cores.views as views

urlpatterns = [
    path(r'overview/', views.overview, name='overview'),
    # path(r'aiperformance/list/', views.AIPerformanceListView.as_view(), name='aiperformance-list'),
    # path(r'aiperformance/chart/', views.aiperformance_chart, name='aiperformance-chart'),
    # path(r'aiautovsresult/list/', views.AIAutovsResultListView.as_view(), name='aiautovsresult-list'),
    # path(r'aiautovsresult/chart/', views.aiautovsresult_chart, name='aiautovsresult-chart'),
    # path(r'aiautovsresult/timechart/', views.aiautovsresult_timechart, name='aiautovsresult-timechart'),
    # path(r'aiconfig/list/', views.AIConfigListView.as_view(), name='aiconfig-list'),
    # path(r'aiconfig/updatelist/', views.aiconfig_updatelist, name='aiconfig-updatelist'),
    # path(r'aiconfig/edit/<int:pk>', views.AIConfigUpdateView.as_view(), name='aiconfig-update'),
    # path(r'defectmodemap/list/>', views.DefectModeMappingListView.as_view(), name='defectmodemap-list'),
    # path(r'defectmodemap/updatelist/', views.defectmodemap_updatelist, name='defectmodemap-updatelist'),
    # path(r'defectmodemap/edit/<int:pk>', views.DefectModeMappingUpdateView.as_view(), name='defectmodemap-update'),
    # path(r'areadetectionsetting/edit/', views.areadetectionsetting_edit, name='areadetectionsetting-edit'),
    ]