import getconfig

config = getconfig.Getconfig('/usr/local/k8s_sys/conf/system.conf')
capath = config.getconfig('ca', 'capath')
cakeypath = config.getconfig('ca', 'cakeypath')
print(capath)
print(cakeypath)
