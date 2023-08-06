==============================
python-plcloudclient
==============================
*宝德云API SDK (http://console.plcloud.com)*

依赖
-----------
1. python-keystoneclient >= 0.8.0


提供的SDK有
---------------
1. CDN (CDN服务)
2. Ticket (工单系统)

使用概述
------------
1. 认证

::
    >>> from plcloudclient.v1_0 import client
    >>> username='demo'
    >>> password='secreetword'
    >>> tenant_name='demo'
    >>> auth_url='http://192.168.106:5001/v2.0'
    >>> plcloud = client.Client(username=username, password=password,
    ...                         tenant_name=tenant_name, auth_url=auth_url)


2. 调用函数(如显示所有CDN域名)

::
    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> plcloud.cdn.list()
