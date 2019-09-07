#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: permission.py
@time: 2019-09-05
"""
import json

from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pure_pagination import Paginator
from rest_framework.reverse import reverse_lazy

from OpenSA import settings
from OpenSA.api import LoginPermissionRequired
from users.forms import PermissionListForm
from users.models import PermissionList


class PermissionListAll(LoginPermissionRequired, ListView):
    model = PermissionList
    template_name = 'users/permission-list.html'
    queryset = PermissionList.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        permission_list = p.page(page)
        context = {
            "users_active": "active",
            "users_permission_list": "active",
            "permission_list": permission_list,
        }
        kwargs.update(context)
        return super(PermissionListALL, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super(PermissionListALL, self).get_queryset()
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            self.queryset = self.queryset.filter(Q(name__icontains=query) | Q(url__icontains=query)).order_by('-id')
        else:
            self.queryset = self.queryset.all().order_by('id')
        return self.queryset


class PermissionAdd(LoginPermissionRequired, CreateView):
    model = PermissionList
    form_class = PermissionListForm
    template_name = 'users/permission-add-update.html'
    success_url = reverse_lazy('users:permission_list')

    def get_context_data(self, **kwargs):
        context = {
            "users_active": "active",
            "users_permission_list": "active",
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super(PermissionAdd, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(PermissionAdd, self).form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class PermissionUpdate(LoginPermissionRequired, UpdateView):
    model = PermissionList
    form_class = PermissionListForm
    template_name = 'users/permission-add-update.html'
    success_url = reverse_lazy('users:permission_list')

    def get_context_data(self, **kwargs):
        context = {
            "users_active": "active",
            "users_permission_list": "active",
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super(PermissionUpdate, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(PermissionUpdate, self).get_form_kwargs()
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        try:
            lable_name = PermissionList.objects.get(pk=pk).lable_name
        except Exception as e:
            lable_name = None
        kwargs['lable_name'] = lable_name
        return kwargs

    def form_invalid(self, form):
        return super(PermissionUpdate, self).form_invalid(form)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        return self.url


class PermissionAllDel(LoginPermissionRequired, DeleteView):
    model = PermissionList

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                PermissionList.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                PermissionList.objects.filter(id__in=ids).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))
