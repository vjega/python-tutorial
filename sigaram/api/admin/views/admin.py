from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime 
from portaladmin import models
# Create your views here.

@csrf_exempt
def addfolder(request):
	"""
	folder_name = request.POST.get('folder_name','')
	remark = request.POST.get('remark','')
	order_no = request.POST.get('order_no','')
	res = {
		"folder_name" : folder_name,
		"remark" : remark,
		"order_no" : order_no
	}
	"""
	date = datetime.now()
	data = request.POST.get("data")
	req = json.loads(data)
	af = models.AdminFolders()
	af.folder_name = req.get('folder_name')
	af.folder_description = req.get("remark")
	af.folder_order = int(req.get("order_no"))
	af.added_date   = "%d-%d-%d" %(date.year, date.month, date.day)
	af.save()
	ret = {
				"msg":"ok"
			}
	return HttpResponse(json.dumps(ret), status=200)