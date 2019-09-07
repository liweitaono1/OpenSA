#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: users.py
@time: 2019-09-06
"""
import json

from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from pure_pagination import Paginator
from rest_framework.reverse import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from OpenSA import settings
from OpenSA.api import LoginPermissionRequired
from audit.models import PasswordChangeLog
from users.forms import UsersFormAdd, UsersForm
from users.models import UserProfile


class UsersListAll(LoginPermissionRequired, ListView):
    model = UserProfile
    template_name = 'users/users-list.html'
    queryset = UserProfile.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        user_list = p.page(page)
        context = {
            "users_active": "active",
            "users_users_list": "active",
            "user_list": user_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = super(UsersListAll, self).get_queryset()
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            self.queryset = self.queryset.filter(Q(username__icontains=query)).order_by('-id')
        else:
            self.queryset = self.queryset.all().order_by('id')
        return self.queryset


class UsersAdd(LoginPermissionRequired, CreateView):
    model = UserProfile
    form_class = UsersFormAdd
    template_name = 'users/users-add-update.html'
    success_url = reverse_lazy('users/users_list')

    def get_context_data(self, **kwargs):
        context = {
            "users_active": "active",
            "users_users_list": "active",
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super(UserAdd, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(UserAdd, self).form_invalid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        form.save()
        return super(UserAdd, self).form_valid(form)


class UsersUpdate(LoginPermissionRequired, UpdateView):
    model = UserProfile
    form_class = UsersForm
    template_name = 'users/users-add-update.html'
    success_url = reverse_lazy('users:users_list')

    def get_context_data(self, **kwargs):
        context = {
            "users_active": "active",
            "users_users_list": "active",
        }
        if '__next__' in self.request.POST:
            context['i__next__'] = self.request.POST['__next__']
        else:
            try:
                context['i__next__'] = self.request.META['HTTP_REFERER']
            except Exception as e:
                pass
        kwargs.update(context)
        return super(UsersUpdate, self).get_context_data(**kwargs)

    def form_invalid(self, form):
        return super(UsersUpdate, self).form_invalid(form)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        return self.url


class UsersAllDel(LoginPermissionRequired, View):
    model = UserProfile

    def post(self, request):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                UserProfile.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                UserProfile.objects.filter(id__in=ids).delete()

        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))


class UsersChangePassword(LoginPermissionRequired, View):
    model = UserProfile

    def post(self, request):
        ret = {'status': True, 'error': None}
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            remote_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            remote_ip = request.META['REMOTE_ADDR']
        try:
            pk = request.POST.get('id', None)
            newpassword = request.POST.get('password', None)
            upobj = UserProfile.objects.get(id=pk)
            upobj.set_password(newpassword)
            upobj.save()
            operator = UserProfile.objects.get(email=self.request.user).username
            PasswordChangeLog.objects.create(user=upobj.username, change_by=operator, remote_addr=remote_ip)
        except Exception as e:
            ret['status'] = False
            ret['error'] = _('Deletion error，{}'.format(e))
        finally:
            return HttpResponse(json.dumps(ret))


class UsersDetail(LoginPermissionRequired, DetailView):
    model = UserProfile
    template_name = 'users/users-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = UserProfile.objects.get(id=pk)

        context = {
            "users_active": "active",
            "users_users_list": "active",
            "users": detail,
            "nid": pk,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
