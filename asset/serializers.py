#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: serializers.py
@time: 2019-09-06
"""
from rest_framework import serializers

from asset.models import Asset, Idc, Service


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ('hostname','ip')


class IdcSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idc
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
