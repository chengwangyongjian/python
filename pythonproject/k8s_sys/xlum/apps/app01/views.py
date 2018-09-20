import json

from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Record, Zone, Permission, Group, NameSpace, ExtraNamespace
from utils.inquire_sql import query_user
from utils.create_namespace import CreateNamespace

from utils.create_systemuser import CreateSystemUser
from utils.create_usercerts import CreateCerts
from utils.create_kubeconfig import CreateKubeconfig
from utils.authorization import ClusterRoleBinding, ListClusterRoles
from utils.getconfig import Getconfig
from utils.delete_user import DeleteUser
from utils.ListPod import ListPod

from .forms import CreateUserForm


def auth(func):
    '''登录验证装饰器'''
    def inner(request, *args, **kwargs):
        user = request.session.get('user')
        user_obj = query_user(user)
        if not user_obj:
            return render(request, 'login.html', {'msg': "请登录"})
        return func(request, *args, **kwargs)
    return inner


class LoginView(View):
    '''登录'''
    def get(self, request):
        request.session.clear()
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('account', '')
        password = request.POST.get('password', '')
        user_obj = query_user(username)
        if user_obj and user_obj.f_password == password:
            request.session['user'] = user_obj.f_account
            return redirect('/rbac/index/tw06m1/')
        else:
            return render(request, 'login.html', {'msg': "用户名或密码错误"})


class LogoutView(View):
    '''登出'''
    def get(self, request):
        request.session.clear()
        return render(request, 'login.html')


@method_decorator([auth], name='dispatch')
class CreateUserView(View):
    '''创建k8s用户（Ajax实现）'''
    def post(self, request):
        ret_dict = {'status': True, 'error': None, 'zone': None, 'data': None}
        msg_form = CreateUserForm(request.POST)
        if msg_form.is_valid():
            group = request.POST.get('username', '')
            expire_time = request.POST.get('expire_time', '')
            if_create_ns = request.POST.get('if_create_ns', '')
            current_zone = request.session['current_zone']
            ret_dict['zone'] = current_zone
            zone_obj = Zone.objects.filter(z_name=current_zone).first()

            config = Getconfig('conf/system.conf')
            capath = config.getconfig(current_zone, 'capath')
            cakeypath = config.getconfig(current_zone, 'cakeypath')
            kubeconfig = config.getconfig(current_zone, 'kubeconfig')
            apiserver = zone_obj.api_server

            # 创建k8s用户
            create_user_return = json.loads(CreateSystemUser(group))
            if create_user_return['status'] != 'ok':
                ret_dict['status'] = False
                ret_dict['error'] = create_user_return['message']
                return HttpResponse(json.dumps(ret_dict))

            # 创建k8s用户证书
            create_cert_return = json.loads(CreateCerts(group, apiserver, expire_time, capath, cakeypath, current_zone))
            if create_cert_return['certs']['status'] != 'ok':
                ret_dict['status'] = False
                ret_dict['error'] = '创建用户证书失败，请重试!'
                return HttpResponse(json.dumps(ret_dict))

            # 创建kubeconfig
            create_kubeconfig_return = json.loads(CreateKubeconfig(apiserver, capath, group, current_zone))
            if create_kubeconfig_return['kubeconfig']['status'] != 'ok':
                ret_dict['status'] = False
                ret_dict['error'] = '创建kubeconfig失败，请重试!'
                return HttpResponse(json.dumps(ret_dict))

            # 用户同名namespace绑定默认clusterRole
            if if_create_ns == 'yes':
                namespace = group
                create_namespace_return = json.loads(CreateNamespace(namespace, kubeconfig))
                if create_namespace_return['status'] != 'ok':
                    ret_dict['status'] = False
                    ret_dict['error'] = '用户同名namespace创建失败'
                    return HttpResponse(json.dumps(ret_dict))

                clusterrole = 'superadmin'
                bind_role_return = json.loads(ClusterRoleBinding(group, clusterrole, namespace, kubeconfig, current_zone))
                if bind_role_return['status'] != 'ok':
                    ret_dict['status'] = False
                    ret_dict['error'] = bind_role_return['message']
                    return HttpResponse(json.dumps(ret_dict))

            # 写入数据库
            try:
                password = create_user_return['password']
            except KeyError as e:
                ret_dict['status'] = False
                ret_dict['error'] = '用户已存在'
                return HttpResponse(json.dumps(ret_dict))
            user_obj = query_user(request.session['user'])
            group_obj = Group(group_name=group, group_pass=password, last_updater=user_obj.f_account)
            group_obj.zone = zone_obj
            group_obj.save()
            if if_create_ns == 'yes':
                ns_obj = NameSpace(namespace=group, zone=zone_obj, last_updater=user_obj.f_account)
                ns_obj.save()
                ns_list = [ns_obj]
                group_obj.namespace = ns_list
                group_obj.save()
            request.session['new_user'] = "%s:   %s" % (group, password)
            return HttpResponse(json.dumps(ret_dict))

        else:
            err_msg = msg_form.errors.as_text()
            ret_dict['status'] = False
            ret_dict['error'] = err_msg
            return HttpResponse(json.dumps(ret_dict))


@method_decorator([auth, csrf_exempt], name='dispatch')
class CreateNamespaceView(View):
    '''创建Namespace（Ajax实现）'''
    def post(self, request):
        ret_dict = {'status': True, 'error': None, 'zone': None, 'data': None}
        namespace = request.POST.get('namespace', '')
        user_bind = request.POST.get('user_bind', '')
        if namespace == '' or user_bind == '':
            ret_dict['status'] = False
            ret_dict['error'] = '请输入namespace并选择绑定的用户!'
            return HttpResponse(json.dumps(ret_dict))
        user_obj = query_user(request.session['user'])
        current_zone = request.session['current_zone']
        ret_dict['zone'] = current_zone
        config = Getconfig('conf/system.conf')
        kubeconfig = config.getconfig(current_zone, 'kubeconfig')
        create_namespace_return = json.loads(CreateNamespace(namespace, kubeconfig))
        if create_namespace_return['status'] != 'ok':
            ret_dict['status'] = False
            ret_dict['error'] = 'namespace创建失败'
            return HttpResponse(json.dumps(ret_dict))

        clusterrole = 'superadmin'
        bind_role_return = json.loads(ClusterRoleBinding(user_bind, clusterrole, namespace, kubeconfig, current_zone))
        if bind_role_return['status'] != 'ok':
            ret_dict['status'] = False
            ret_dict['error'] = bind_role_return['message']
            return HttpResponse(json.dumps(ret_dict))

        # 写入数据库
        group_obj = Group.objects.filter(group_name=user_bind).first()
        permission_obj = Permission.objects.filter(p_name='superadmin').first()
        ns_obj = ExtraNamespace(namespace=namespace, group=group_obj, permission=permission_obj, last_updater=user_obj.f_account)
        ns_obj.save()
        return HttpResponse(json.dumps(ret_dict))


@method_decorator([auth, csrf_exempt], name='dispatch')
class DeleteUserView(View):
    '''删除用户'''
    def get(self, request, group):
        current_zone = request.session['current_zone']
        config = Getconfig('conf/system.conf')
        kubeconfig = config.getconfig(current_zone, 'kubeconfig')
        ns = NameSpace.objects.filter(group__group_name=group).first()
        extra_ns = ExtraNamespace.objects.filter(group__group_name=group).values_list('namespace')
        all_ns = [item[0] for item in extra_ns]
        if ns:
            all_ns.append(ns.namespace)
        delete_user_return = json.loads(DeleteUser(group, all_ns, kubeconfig, current_zone))
        return_msg = delete_user_return['message']
        request.session['alert_msg'] = return_msg
        if delete_user_return['status'] == 'failed':
            if delete_user_return['message'] == 'unbinding failed.':
                return_msg = delete_user_return['message'] + '\n未解除绑定的namespace列表：\n' + delete_user_return['namespacelist']
                request.session['alert_msg'] = return_msg
            return redirect('/rbac/index/%s/' % current_zone)

        zone_obj = Zone.objects.filter(z_name=current_zone).first()
        Group.objects.filter(group_name=group, zone=zone_obj).delete()
        return redirect('/rbac/index/%s/' % current_zone)


@method_decorator([auth, csrf_exempt], name='dispatch')
class AddExtraNamespaceView(View):
    '''添加ExtraNamespace'''
    def post(self, request):
        current_zone = request.session['current_zone']
        group = request.POST.get('user', '')
        extra_namespace = request.POST.get('extra_namespace', '')
        permission = request.POST.get('permission', '')

        clusterrole = 'superadmin'
        config = Getconfig('conf/system.conf')
        kubeconfig = config.getconfig(current_zone, 'kubeconfig')
        bind_role_return = json.loads(ClusterRoleBinding(group, clusterrole, extra_namespace, kubeconfig, current_zone))
        request.session['alert_msg'] = bind_role_return['message']
        if bind_role_return['status'] != 'ok':
            return redirect('/rbac/index/%s/' % current_zone)

        # 写入数据库
        user_obj = query_user(request.session['user'])
        group_obj = Group.objects.filter(group_name=group).first()
        permission_obj = Permission.objects.filter(p_name=permission).first()
        ExtraNamespace.objects.create(group=group_obj, permission=permission_obj, namespace=extra_namespace, last_updater=user_obj.f_account)
        return redirect('/rbac/index/%s/' % current_zone)


@auth
def index(request, zone, selected_group=None):
    request.session['current_zone'] = zone
    zone_sql = Zone.objects.values('z_name')
    zone_list = [item['z_name'] for item in zone_sql]
    permission_sql = Permission.objects.values('p_name')
    permission_list = [item['p_name'] for item in permission_sql]
    zone_obj = Zone.objects.filter(z_name=zone).first()
    group_dict = Group.objects.filter(zone=zone_obj)
    all_group = [item['group_name'] for item in group_dict.values('group_name')]
    if selected_group:
        group_dict = group_dict.filter(group_name=selected_group)
    group_ns_dict = {}
    for group in group_dict:
        ns = NameSpace.objects.filter(group=group).first()
        extra_ns = ExtraNamespace.objects.filter(group=group).values_list('namespace')
        all_ns = [item[0] for item in extra_ns]
        if ns:
            all_ns.append(ns.namespace)
        group_ns_dict[group.group_name] = all_ns

    user_obj = query_user(request.session['user'])
    ns_sql = NameSpace.objects.filter(zone=zone_obj).values('namespace')
    namespace_list = [item['namespace'] for item in ns_sql]
    extra_ns_sql = ExtraNamespace.objects.filter(group__zone=zone_obj).values('namespace')
    extra_ns_list = [item['namespace'] for item in extra_ns_sql]
    namespace_list.extend(extra_ns_list)
    namespace_list = set(namespace_list)

    new_user = request.session.get('new_user', '')
    try:
        del request.session['new_user']
    except:
        pass
    new_user = json.dumps(new_user)

    alert_msg = request.session.get('alert_msg', '')
    try:
        del request.session['alert_msg']
    except:
        pass
    alert_msg = json.dumps(alert_msg)

    content = {
        'group_ns_dict': group_ns_dict,
        'user': user_obj,
        'group_list': all_group,
        'namespace_list': namespace_list,
        'zone_list': zone_list,
        'permission_list': permission_list,
        'current_zone': zone,
        'new_user': new_user,
        'alert_msg': alert_msg,
    }
    return render(request, 'index.html', content)

@auth
def details(request, zone, selected_group,selected_namespace=None):
    user_obj = query_user(request.session['user'])
    zone_sql = Zone.objects.values('z_name')
    zone_list = [item['z_name'] for item in zone_sql]
    zone_obj = Zone.objects.filter(z_name=zone).first()
    ns_sql = NameSpace.objects.filter(zone=zone_obj).values('namespace')
    namespace_list = [item['namespace'] for item in ns_sql]
#获取选择的group的所有ns
    group_dict = Group.objects.filter(zone=zone_obj)
    group = group_dict.filter(group_name=selected_group)
    ns = NameSpace.objects.filter(group=group).first()
    extra_ns = ExtraNamespace.objects.filter(group=group).values_list('namespace')
    all_ns = [item[0] for item in extra_ns]
    if ns:
        all_ns.append(ns.namespace)
    #读取pod
    pod_dict={}
    if selected_namespace != None:
         config = Getconfig('conf/system.conf')
         kubeconfig = config.getconfig(zone, 'kubeconfig')
         list_pod_return = json.loads(ListPod(kubeconfig,selected_namespace))
         if list_pod_return['status'] != 'ok':
              return HttpResponse("get pod error!")
         pod_dict=list_pod_return['podinfo']
    else:
         selected_namespace='请选择命名空间'
    content={
    'user': user_obj,
    'current_zone': zone,
    'namespace_list': all_ns,
    'group': selected_group,
    'namespace': selected_namespace,
    'zone_list': zone_list,
    'pod_dict': pod_dict
    }
    return render(request, 'details.html',content)
