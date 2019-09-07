#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: asset.py
@time: 2019-09-06
"""
import json
import time
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.base import View
from pure_pagination import Paginator
from rest_framework.reverse import reverse_lazy

from OpenSA import settings
from OpenSA.api import LoginPermissionRequired
from asset.forms import AssetFormAdd, AssetForm
from asset.models import Asset


class AssetListAll(LoginPermissionRequired, ListView):
    model = Asset
    template_name = 'asset/asset-list.html'
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1

        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        asset_list = p.page(page)
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "asset_list": asset_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super(AssetListAll, self).get_queryset()
        try:
            project = self.request.session['project']
        except Exception as e:
            project = None
        product = self.request.GET.get('id')
        asset = self.request.GET.get('asset')
        if project:
            if self.request.GET.get('name'):
                query = self.request.GET.get('name', None)
                self.queryset = self.queryset.filter(project__name=project).filter(
                    Q(hostname__icontains=query) |
                    Q(ip__icontains=query) |
                    Q(other_ip__icontains=query)
                ).order_by('-id')

            else:
                if product:
                    self.queryset = self.queryset.filter(project__name=project, product__id=product)
                elif asset:
                    self.queryset = self.queryset.filter(project__name=project, id=asset.strip('-'))
                else:
                    self.queryset = self.queryset.filter(project__name=project).order_by('id')
        else:
            self.queryset = self.queryset.filter(project__name=project).order_by('id')
        return self.queryset


class AssetAdd(LoginPermissionRequired, CreateView):
    model = Asset
    form_class = AssetFormAdd
    template_name = 'asset/asset-add-update.html'
    success_url = reverse_lazy('asset:asset_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
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


class AssetUpdate(LoginPermissionRequired, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'asset/asset-add-update.html'
    success_url = reverse_lazy('asset:asset_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }

        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super(AssetUpdate, self).get_context_data(**kwargs)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        asset = Asset.objects.get(id=pk)
        asset.update_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        asset.save()
        return self.url


class AssetAllDel(LoginPermissionRequired, View):
    model = Asset

    def post(self, request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                Asset.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                Asset.objects.filter(id__in=ids).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))


class AssetDetail(LoginPermissionRequired, DetailView):
    model = Asset
    template_name = 'asset/asset-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = Asset.objects.get(id=pk)
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "asset": detail,
            "nid": pk,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


def AssetZtree(request):
    try:
        project = request.sessiom['project']
    except Exception as e:
        project = None
    data = [{'id': '111', 'pId': '0', 'name': '{}'.format(_("Please Select Project"))}]
    if project:
        manager = Asset.objects.filter(project__name=project)
        data = [{"id": "1111", "pId": "0", "floor": 0, "name": '{} {}'.format(project, _("Project"))}]
        for i in manager:
            try:
                product = {'id': i.project.id, 'pId': '1111', 'floor': 1,
                           'name': '{} {}'.format(i.project.name, _('Product')), 'page': "xx.action"}
                if not product in data:
                    data.append(product)
                node_dict = {"id": '{}'.format(i.id), "pId": i.product.id, "floor": 2,
                             "name": '{} {}'.format(i.hostname, i.ip),
                             "page": "xx.action"}  # "iconSkin":"icon-centos"
                if i.os_type is 0:
                    node_dict["iconSkin"] = "icon-centos"
                elif i.os_type is 1:
                    node_dict["iconSkin"] = "icon-windows"
                elif i.os_type is 2:
                    node_dict["iconSkin"] = "icon-ubuntu"
                elif i.os_type is 3:
                    node_dict["iconSkin"] = "icon-debian"
                data.append(node_dict)
            except Exception as e:
                pass
    return HttpResponse(json.dumps(data))
