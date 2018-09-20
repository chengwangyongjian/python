# k8s system api

## 建立新的用户api调用顺序

create-systemuser --> create-usercerts --> create-kubeconfig --> authorization.ClusterRoleBinding


## config文件用法
```
import getconfig

config = getconfig.Getconfig('/usr/local/k8s_sys/conf/system.conf')
capath = config.getconfig('ca', 'capath')
cakeypath = config.getconfig('ca', 'cakeypath')
print(capath)
print(cakeypath)
```
