#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: project.py
@time: 2019-09-05
"""
import json

from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework.reverse import reverse_lazy
from django.utils.translation import ugettext as _
from OpenSA.api import LoginPermissionRequired
from users.forms import ProjectFormAdd, ProjectForm
from users.models import Project


class ProjectListAll(LoginPermissionRequired, ListView):
    template_name = 'users/project-list.html'
    model = Project
    context_object_name = 'project_list'

    def get_context_data(self, **kwargs):
        context = {
            'users_active': 'active',
            'users_project_list': 'active'
        }
        kwargs.update(context)
        return super(ProjectListAll, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super(ProjectListAll, self).get_queryset()
        queryset = self.queryset.all().order_by('id')
        return queryset


class ProjectAdd(LoginPermissionRequired, CreateView):
    model = Project
    form_class = ProjectFormAdd
    template_name = 'users/project-add-update.html'
    success_url = reverse_lazy('users:project_list')

    def get_context_data(self, **kwargs):
        context = {
            "users_active": "active",
            "users_project_list": "active",
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
        return super(ProjectAdd, self).form_invalid(form)


class ProjectUpdate(LoginPermissionRequired, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'users/project-add-update.html'
    success_url = reverse_lazy('users:users_list')

    def get_context_data(self, **kwargs):
        context = {
            "users_active": "active",
            "users_project_list": "active",
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
        return super(ProjectUpdate, self).form_invalid(form)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        return self.url


class ProjectDel(LoginPermissionRequired, View):
    model = Project

    def post(self, request):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                Project.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                Project.objects.filter(id__in=ids).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))
