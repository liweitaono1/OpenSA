#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: role.py
@time: 2019-09-06
"""
import json

from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, UpdateView, DeleteView
from pure_pagination import Paginator

from OpenSA import settings
from OpenSA.api import LoginPermissionRequired
from users.forms import RoleForm
from users.models import RoleList, PermissionList


class RoleAll(LoginPermissionRequired, ListView):
    model = RoleList
    template_name = 'users/role-list.html'
    queryset = RoleList.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        role_list = p.page(page)
        error = self.request.GET.get('error')
        context = {
            "users_active": "active",
            "users_role_list": "active",
            "role_list": role_list,
            "error": error
        }

        kwargs.update(context)
        return super(RoleAll, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super(RoleAll, self).get_queryset()
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            self.queryset = self.queryset.filter(Q(name__icontains=query)).order_by('-id')
        else:
            self.queryset = self.queryset.all().order_by('id')
        return self.queryset

    def post(self, request, *args, **kwargs):
        role_name = request.POST.get('role_name')
        url = ''
        try:
            RoleList.objects.create(name=role_name)
            url = '/users/role-list/'
        except Exception as e:
            url = '/users/role-list/?error={}'.format(e)
        finally:
            return HttpResponseRedirect(url)


class RoleEdit(LoginPermissionRequired, UpdateView):
    model = RoleList
    template_name = 'users/role-edit.html'
    form_class = RoleForm

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        error = self.request.GET.get('error')
        msg = self.request.GET.get('msg')
        role_obj = RoleList.objects.get(id=pk)
        role_urls = role_obj.permission.all()
        permission_list = PermissionList.objects.all()
        urls = []
        for url in permission_list:
            if url not in role_urls:
                if url not in role_urls:
                    urls.append(url)
        context = {
            "users_active": "active",
            "users_role_list": "active",
            "role_obj": role_obj,
            "role_urls": role_urls,
            "urls": urls,
            "permission_list": permission_list,
            "error": error,
            "msg": msg,
        }
        kwargs.update(context)
        return super(RoleEdit, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('nid')
        role_obj = RoleList.objects.get(id=pk)
        urls_select = request.POST.getlist('urls_select[]')
        ret = {'status': True, 'error': None}
        try:
            if len(urls_select) is not None:
                role_obj.permission.clear()
                for p_id in urls_select:
                    role_obj.permission.add(p_id)
                role_obj.save()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))


class RoleAllDel(LoginPermissionRequired, DeleteView):
    model = RoleList

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                RoleList.objects.get(id=id).permission.clear()
                RoleList.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                for id in ids:
                    RoleList.objects.get(id=id).permission.clear()
                    RoleList.objects.get(id=id).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))
