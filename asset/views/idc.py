#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: idc.py
@time: 2019-09-06
"""
import json

from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import View
from rest_framework.reverse import reverse_lazy
from django.utils.translation import ugettext as _
from OpenSA.api import LoginPermissionRequired
from asset.forms import IdcForm, IdcFormUpdate
from asset.models import Idc


class IdcList(LoginPermissionRequired, ListView):
    template_name = 'asset/idc-list.html'
    model = Idc
    context_object_name = 'idc_list'

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_idc_active": "active",
        }
        kwargs.update(context)
        return super(IdcList, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super(IdcList, self).get_queryset()
        queryset = self.queryset.all().order_by('id')
        return queryset


class IdcAdd(LoginPermissionRequired, CreateView):
    model = Idc
    form_class = IdcForm
    template_name = 'asset/idc-add-update.html'
    success_url = reverse_lazy('asset:idc_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_idc_active": "active",
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
        return super(IdcAdd, self).form_invalid(form)


class IdcUpdate(LoginPermissionRequired, UpdateView):
    model = Idc
    form_class = IdcFormUpdate
    template_name = 'asset/idc-add-update.html'
    success_url = reverse_lazy('asset:idc_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_idc_active": "active",
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
        return super(IdcUpdate, self).form_invalid(form)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        return self.url


class IdcDel(LoginPermissionRequired, View):
    model = Idc

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                Idc.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                Idc.objects.filter(id__in=ids).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))
