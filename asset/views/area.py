#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: area.py
@time: 2019-09-06
"""
import json

from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework.reverse import reverse_lazy

from OpenSA.api import LoginPermissionRequired
from asset.forms import AreaForm, AreaFormUpdate
from asset.models import Area


class AreaList(LoginPermissionRequired, ListView):
    template_name = 'asset/area-list.html'
    model = Area
    context_object_name = 'area_list'

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_area_active": "active",
        }
        kwargs.update(context)
        return super(AreaList, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super(AreaList, self).get_queryset()
        queryset = self.queryset.all().order_by('id')
        return queryset


class AreaAdd(LoginPermissionRequired, CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'asset/area-add-update.html'
    success_url = reverse_lazy('asset:area_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_area_active": "active",
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(AreaAdd, self).form_invalid(form)


class AreaUpdate(LoginPermissionRequired, UpdateView):
    model = Area
    form_class = AreaFormUpdate
    template_name = 'asset/area-add-update.html'
    success_url = reverse_lazy('asset:area_list')

    def get_context_data(self, **kwargs):

        context = {
            "asset_active": "active",
            "asset_area_active": "active",
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(AreaUpdate, self).form_invalid(form)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        return self.url


class AreaDel(LoginPermissionRequired, View):
    model = Area

    def post(self, request):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                Area.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                Area.objects.filter(id__in=ids).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))
