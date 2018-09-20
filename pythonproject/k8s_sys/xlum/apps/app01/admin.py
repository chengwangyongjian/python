#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/8/18

from django.contrib import admin

from .models import User, Record, Zone, Permission, Group, NameSpace, ExtraNamespace


class UserAdmin(admin.ModelAdmin):
    # list_display = ['chinese_name', 'is_root', 'add_time']  # 默认展示字段
    # search_fields = ['chinese_name', 'is_root']  # 搜索框可搜索内容
    # list_filter = ['chinese_name', 'is_root', 'add_time']  # 过滤器列表
    pass


class RecordAdmin(admin.ModelAdmin):
    pass


class ZoneAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.last_updater = request.user.username
        obj.save()

    readonly_fields = ("last_updater",)


class PermissionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.last_updater = request.user.username
        obj.save()

    readonly_fields = ("last_updater",)


class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'add_time', 'last_time', 'zone']

    def save_model(self, request, obj, form, change):
        obj.last_updater = request.user.username
        obj.save()

    readonly_fields = ("last_updater",)


class NameSpaceAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.last_updater = request.user.username
        obj.save()

    readonly_fields = ("last_updater",)


class ExtraNamespaceAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.last_updater = request.user.username
        obj.save()

    readonly_fields = ("last_updater",)


admin.site.register(User, UserAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(NameSpace, NameSpaceAdmin)
admin.site.register(ExtraNamespace, ExtraNamespaceAdmin)
