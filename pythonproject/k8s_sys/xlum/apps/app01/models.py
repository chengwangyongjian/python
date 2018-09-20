from datetime import datetime

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    chinese_name = models.CharField(max_length=100, verbose_name="中文名")
    is_root = models.BooleanField(default=0, verbose_name="是否超级用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "登录平台用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Record(models.Model):
    users = models.ForeignKey("User", related_name='record', verbose_name="操作人", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="操作时间")
    operation_type_choice = (
        ("create", "增"),
        ("delete", "删"),
        ("update", "改"),
        ("select", "查"),
    )
    operation_type = models.CharField(max_length=10, null=False, choices=operation_type_choice, verbose_name="操作类型")
    operation_detail = models.TextField(verbose_name="操作日志")

    class Meta:
        verbose_name = "操作记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.users.username


class Permission(models.Model):
    p_name = models.CharField(max_length=100, unique=True, null=False, verbose_name='权限名')
    p_type = models.CharField(max_length=100, null=False, verbose_name='权限类型')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updater = models.CharField(max_length=100, null=False, verbose_name='最后操作员')
    last_time = models.DateTimeField(auto_now=True, verbose_name='最后操作时间')
    expired_days = models.IntegerField(default=1, verbose_name="过期时间(天)")

    class Meta:
        verbose_name = "k8s用户组权限"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%s)" % (self.p_name, self.p_type)


class Zone(models.Model):
    z_name = models.CharField(max_length=100, null=False, verbose_name="区域名")
    api_server = models.GenericIPAddressField(null=False, verbose_name="APIserver地址")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updater = models.CharField(max_length=100, null=False, verbose_name='最后操作员')
    last_time = models.DateTimeField(auto_now=True, verbose_name='最后操作时间')

    class Meta:
        verbose_name = "区域"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.z_name


class Group(models.Model):
    zone = models.ForeignKey(Zone, related_name='group', verbose_name='区域', on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100, unique=True, null=False, verbose_name='K8s用户组名')
    group_pass = models.CharField(max_length=100, unique=False, verbose_name="k8s用户组密码")
    # Namespace Group关联关系
    namespace = models.ManyToManyField('NameSpace', related_name='group', db_table='group_to_namespace')

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updater = models.CharField(max_length=100, null=False, verbose_name='最后操作员')
    last_time = models.DateTimeField(auto_now=True, verbose_name='最后操作时间')


    class Meta:
        verbose_name = "k8s用户组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name


class NameSpace(models.Model):
    zone = models.ForeignKey(Zone, related_name='namespace', verbose_name='区域')
    namespace = models.CharField(max_length=100, null=False)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updater = models.CharField(max_length=100, null=False, verbose_name='最后操作员')
    last_time = models.DateTimeField(auto_now=True, verbose_name='最后操作时间')

    def __str__(self):
        return self.namespace


class ExtraNamespace(models.Model):
    '''Namespace Group Permission关联关系表'''
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=100)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    last_updater = models.CharField(max_length=100, null=False, verbose_name='最后操作员')
    last_time = models.DateTimeField(auto_now=True, verbose_name='最后操作时间')

    def __str__(self):
        return "%s-%s" % (self.group.group_name, self.namespace)

    class Meta:
        db_table = 'extra_namespace'
        unique_together = ('group', 'namespace', 'permission')
