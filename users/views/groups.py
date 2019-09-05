#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: groups.py
@time: 2019-09-05
"""
import json

from django.conf import settings
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pure_pagination import Paginator
from rest_framework.reverse import reverse_lazy

from OpenSA.api import LoginPermissionRequired
from users.forms import GroupsForm
from users.models import DepartMent


class GroupsListAll(LoginPermissionRequired, ListView):
    model = DepartMent
    template_name = 'users/groups-list.html'
    queryset = DepartMent.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        group_list = p.page(page)

        context = {
            "users_active": "active",
            "users_groups_list": "active",
            "group_list": group_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super().get_queryset()
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            self.queryset = self.queryset.filter(Q(name__icontains=query) | Q(comment__icontains=query)).order_by('-id')
        else:
            self.queryset = self.queryset.all().order_by('id')

        return self.queryset


class GroupsAdd(LoginPermissionRequired, CreateView):
    model = DepartMent
    form_class = GroupsForm
    template_name = 'users/groups-add-update.html'
    success_url = reverse_lazy('users:groups_list')

    def get_context_data(self, **kwargs):
        context = {
            'users_active': 'active',
            'users_groups_list': 'active'
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super(GroupsAdd, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(GroupsAdd, self).form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(GroupsAdd, self).form_valid(form)


class GroupsUpdate(LoginPermissionRequired, UpdateView):
    model = DepartMent
    form_class = GroupsForm
    template_name = 'users/groups-add-update.html'
    success_url = reverse_lazy('users:groups_list')

    def get_context_data(self, **kwargs):

        context = {
            "users_active": "active",
            "users_groups_list": "active",
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super(GroupsUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(GroupsUpdate, self).form_invalid(form)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        return self.url


class GroupsAllDel(LoginPermissionRequired, DeleteView):
    model = DepartMent

    def post(self, request, *args, **kwargs):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                DepartMent.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                DepartMent.objects.filter(id__in=ids).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))
