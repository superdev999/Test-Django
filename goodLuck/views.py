from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.forms import ModelForm

from goodLuck.models import Mymodel

from random import randint

import csv
import datetime

class GoodLuckForm(ModelForm):
    class Meta:
        model = Mymodel
        fields = ['name', 'birthday']

def goodLuck_list(request, template_name='goodLuck/goodLuck_list.html'):
    goods = Mymodel.objects.all()    
    data = {}
    data['user_list'] = goods    
    return render(request, template_name, data)

def goodLuck_create(request, template_name='goodLuck/goodLuck_form.html'):
    form = GoodLuckForm(request.POST or None)
        
    if form.is_valid():   
        form.save()         
       
        return redirect('goodLuck:goodLuck_list')
    return render(request, template_name, {'form':form})

def goodLuck_update(request, pk, template_name='goodLuck/goodLuck_form_2.html'):
    goods= get_object_or_404(Mymodel, pk=pk)
    form = GoodLuckForm(request.POST or None, instance=goods)
    if form.is_valid():
        form.save()
        return redirect('goodLuck:goodLuck_list')
    return render(request, template_name, {'form':form})

def goodLuck_delete(request, pk, template_name='goodLuck/goodLuck_delete.html'):
    goods= get_object_or_404(Mymodel, pk=pk)    
    if request.method=='POST':
        goods.delete()
        return redirect('goodLuck:goodLuck_list')
    return render(request, template_name, {'object':goods})
    
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Birthday', 'RandNum', 'BizzFuzz'])

    users = Mymodel.objects.all().values_list('name', 'birthday', 'randNum', 'bizz')
    for user in users:
        writer.writerow(user)

    return response