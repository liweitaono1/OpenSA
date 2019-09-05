#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: login.py
@time: 2019-09-05
"""
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login as auth_login, logout as auth_logout

from users.models import UserProfile


class UserLoginView(FormView):
    template_name = 'users/login.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = {}
        kwargs.update(context)

    def post(self, request, *args, **kwargs):
        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            ipaddr = self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            ipaddr = self.request.META['REMOTE_ADDR']
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        check_code = request.POST.get('checkcode')
        user = authenticate(username=username, password=password)
        session_code = request.session["CheckCode"]
        if check_code.strip().lower() != session_code.lower():
            login_err = _('Did you slip the wrong hand? try again')
        else:
            try:
                limit_num = 5
                curr_login_limit = UserProfile.objects.get(email=username).login_limit
                new_login_limit = int(curr_login_limit) + 1
                login_limit_info = UserProfile.objects.filter(email=username)
                if new_login_limit == 5:
                    login_limit_info.update(limit=new_login_limit, is_active=0)
                    login_err = _("Warning: {} has been disabled, please contact the administrator".format(username))
                else:
                    login_limit_info.update(limit=new_login_limit)
                    login_err = _("Warning: {} remaining attempts are {}".format(username, limit_num - new_login_limit))
            except Exception as e:
                login_err = _('Verification failed? Think again ^.^')
        return render(request, 'users/login.html', {'login_err': login_err})


class UserLogoutView(TemplateView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = {
            'messages': 'Logout success',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
