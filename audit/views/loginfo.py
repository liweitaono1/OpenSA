#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: loginfo.py
@time: 2019-09-06
"""
import datetime

from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from pure_pagination import Paginator

from OpenSA import settings
from OpenSA.api import LoginPermissionRequired
from audit.models import RequestRecord, PasswordChangeLog
from users.models import UserProfile


class LoginLogList(LoginPermissionRequired, ListView):
    model = RequestRecord
    template_name = 'audit/login-log.html'
    queryset = RequestRecord.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        loginlog_list = p.page(page)

        context = {
            "audit_active": "active",
            "audit_login_active": "active",
            "loginlog_list": loginlog_list,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = RequestRecord.objects.filter(get_full_path__in=['/users/login/', '/users/logout/'])
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        operator = UserProfile.objects.get(email=self.request.user)
        if self.request.GET.get('name') and operator.is_superuser:
            query = self.request.GET.get('name', None)
            self.queryset = self.queryset.filter(username__username=query).order_by('-datetime')
            if date_from and date_to:
                end = datetime.datetime.strptime(date_to, '%Y-%m-%d') + datetime.timedelta(days=1)
                self.queryset = self.queryset.filter(datetime__gte=date_from).filter(datetime__lte=end).order_by(
                    '-datetime')
        else:
            if date_from and date_to:
                end = datetime.datetime.strptime(date_to, '%Y-%m-%d') + datetime.timedelta(days=1)
                self.queryset = self.queryset.filter(datetime__gte=date_from).filter(datetime__lte=end).order_by(
                    '-datetime')
            else:
                self.queryset = self.queryset.order_by('-datetime')
        return self.queryset


class PasswordChangeList(LoginPermissionRequired, ListView):
    model = PasswordChangeLog
    template_name = 'audit/password-change-log.html'
    queryset = PasswordChangeLog.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        requestlog_list = p.page(page)

        context = {
            "audit_active": "active",
            "password_change_log": "active",
            "loginlog_list": requestlog_list,
            'date_from': (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y-%m-%d'),
            'date_to': (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime('%Y-%m-%d')

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = PasswordChangeLog.objects.all()
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        operator = UserProfile.objects.get(email=self.request.user)
        if self.request.GET.get('name') and operator.is_superuser:
            query = self.request.GET.get('name', None)
            self.queryset = self.queryset.filter(user=query).order_by('-datetime')
            if date_from and date_to:
                end = datetime.datetime.strptime(date_to, '%Y-%m-%d') + datetime.timedelta(days=1)
                self.queryset = self.queryset.filter(datetime__gte=date_from).filter(datetime__lte=end).order_by(
                    '-datetime')
        else:
            if date_from and date_to:
                end = datetime.datetime.strptime(date_to, '%Y-%m-%d') + datetime.timedelta(days=1)
                self.queryset = self.queryset.filter(datetime__gte=date_from).filter(datetime__lte=end).order_by(
                    '-datetime')
            else:
                self.queryset = self.queryset.order_by('-datetime')

        return self.queryset


class RequestLogList(LoginPermissionRequired, ListView):
    model = RequestRecord
    template_name = 'audit/request-log.html'
    queryset = RequestRecord.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1
        p = Paginator(self.queryset, getattr(settings, 'DISPLAY_PER_PAGE'), request=self.request)
        requestlog_list = p.page(page)
        context = {
            "audit_active": "active",
            "audit_request_active": "active",
            "loginlog_list": requestlog_list,
            'date_from': (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y-%m-%d'),
            'date_to': (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime('%Y-%m-%d')

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = RequestRecord.objects.exclude(get_full_path__in=['/users/login/', '/users/logout/'])
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        operator = UserProfile.objects.get(email=self.request.user)
        if self.request.GET.get('name') and operator.is_superuser:
            query = self.request.GET.get('name', None)
            self.queryset = self.queryset.filter(operator=query).order_by('-datetime')
            if date_from and date_to:
                end = datetime.datetime.strptime(date_to, '%Y-%m-%d') + datetime.timedelta(days=1)
                self.queryset = self.queryset.filter(datetime__gte=date_from).filter(datetime__lte=end).order_by(
                    '-datetime')
        else:
            if date_from and date_to:
                end = datetime.datetime.strptime(date_to, '%Y-%m-%d') + datetime.timedelta(days=1)
                self.queryset = self.queryset.filter(datetime__gte=date_from).filter(datetime__lte=end).order_by(
                    '-datetime')
            else:
                self.queryset = self.queryset.order_by('-datetime')

        return self.queryset
