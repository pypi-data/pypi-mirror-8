==============================
python-plcloudclient
==============================
*宝德云API SDK (http://console.plcloud.com)*

.. image:: https://pypip.in/version/python-plcloudclient/badge.png
    :target: https://pypi.python.org/pypi/python-plcloudclient/
    :alt: Latest Version

.. image:: https://pypip.in/download/python-plcloudclient/badge.png?period=month
    :target: https://pypi.python.org/pypi/python-plcloudclient/
    :alt: Downloads

依赖
-----------
1. python-keystoneclient >= 0.8.0


提供的SDK有
---------------
1. CDN (CDN服务)
2. Ticket (工单服务)

使用概述
------------
1. 公共参数::
    * API auth_url: http://api.plcloud.com:5001/v2.0
    * username: 用户登录名
    * password: 用户登录密码
    * tenant_name: 用户登录名

2. 认证::

    >>> from plcloudclient.v1_0 import client
    >>> username='demo'
    >>> password='secreetword'
    >>> tenant_name='demo'
    >>> auth_url='http://api.plcloud.com:5001/v2.0'
    >>> plcloud = client.Client(username=username, password=password,
    ...                         tenant_name=tenant_name, auth_url=auth_url)

3. 调用函数(如显示所有CDN域名)::

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> plcloud.cdn.list()
