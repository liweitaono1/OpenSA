#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: views.py
@time: 2019-09-07
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
import io

from OpenSA.utils import create_validate_code


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


def page_not_found(request):
    return render(request, '404.html')

def server_error(request):
    return render(request, '500.html')

def permission_denied(request):
    return render(request, '404.html')

def CheckCode(request):
    mstream = io.BytesIO()
    validate_code = create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    request.session["CheckCode"] = validate_code[1]
    return HttpResponse(mstream.getvalue())

