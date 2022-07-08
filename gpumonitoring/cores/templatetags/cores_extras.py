from django import template
import datetime
from cores.models import Service
from django.core.serializers.json import DjangoJSONEncoder
import json     

register = template.Library()


# use simple tag to set context variable
@register.simple_tag(takes_context=True)
def get_permitted_services(context):
    request = context['request']

    # 判斷如果 Session 有值，則直接回傳，如果沒有，則比對資料庫
    if request.session.get("cores.services.list") == None:
        # 取得目前登入者的權限清單
        _permissions = request.user.get_all_permissions()

        _services = Service.objects.all()

        result = list()
        
        # 比對 service 的 token，是否存在於目前登入者擁有的列表中
        for _service in _services:
            if _service.security_token == "all" or _service.security_token in _permissions:
                _service_dict = _service.__dict__
                _service_dict.pop('_state', None) #Pop which are not json serialize
                # _service_dict = json.dumps(_service_dict)
                result.append(_service_dict)
        
        #Sort
        result = sorted(result, key = lambda x : x["sorted_index"])
        request.session["cores.services.list"] = result

    return request.session.get("cores.services.list")
