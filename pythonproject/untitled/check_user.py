import etcd

def check(username,password):
    client=etcd.Client(host='10.10.99.81',port=2379)
    if password == client.get('/users/'+username).value:
        return True
    else:
        return False