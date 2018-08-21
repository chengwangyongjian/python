import etcd

def get():
    client = etcd.Client(host='10.10.99.81', port=2379)
    r = client.read('/nginx', recursive=True, sorted=True)
    d={child.key:child.value for child in r.children}
    return d
