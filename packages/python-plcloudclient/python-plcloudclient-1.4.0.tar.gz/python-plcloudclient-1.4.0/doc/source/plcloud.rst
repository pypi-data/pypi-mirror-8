=================
Plcloud API
=================

公共参数
============
* API auth_url: http://api.plcloud.com:5001/v2.0
* username: 用户登录名
* password: 用户登录密码
* tenant_name: 用户登录名

身份认证API
============

身份认证API是使用REST风格的Web服务接口来实现。 进行身份验证，您必须提供用户名和密码::

    >>> from plcloudclient.v1_0 import client
    >>> username='demo'
    >>> password='secreetword'
    >>> tenant_name='demo'
    >>> auth_url='http://api.plcloud.com:5001/v2.0'
    >>> plcloud = client.Client(username=username, password=password,
    ...                         tenant_name=tenant_name, auth_url=auth_url)

CDN API
============

显示CDN域名列表::

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.list()


新建CDN::

    参数
    domain(域名)
    origin_ips(源IP）list类型 例如 ['114.114.114.114', '115.115.115.115']
    areas（服务区域）list类型 例如 ['cn', 'hk', 'ov']
    type(类型) 默认 'web'
    icp_record(ICP备案号)(国内域名请确认已备案，否则将无法使用CDN服务。)

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> data = {'domain': domain,
                'origin_ips': ['114.114.114.114'],
                'areas': ['cn'],
                'type': 'web',
                'icp_record': None}
    >>> result = plcloud.cdn.create(**data)


更新CDN::

    参数
    domain_id(域名ID) 例如 206813
    origin_ips(源IP) list类型 例如 ['114.114.114.114', '115.115.115.115']
    areas(服务区域) list类型 例如 ['cn', 'hk', 'ov']

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> data = {'origin_ips': ['114.114.114.114'],
                'areas': ['cn']}
    >>> result = plcloud.cdn.update(domain_id,
                                    **data)


获取单个CDN::

    参数
    domain_id(域名ID) 例如 206813

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.get(domain_id)


删除CDN::

    参数
    domain_id(域名ID) 例如 206813

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.delete(domain_id)


获取CDN流量::

    参数
    domain_id(域名ID) 例如 206813

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.flow(domain_id)


充值::

    参数
    flow(流量数) 单位为GB

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.recharge(flow)


创建常用链接::

    参数
    urls

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.create_urls(urls)


常用链接列表::

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.list_urls()


删除常用链接::

    参数
    url_id

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.delete_urls(url_id)


缓存刷新::

    参数
    domain_id (域名ID）例如 206813
    urls（文件列表) list类型
    dirs （目录列表）list类型

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.cache_flush(domain_id, urls, dirs)


日志::

    参数
    domain_id (域名ID）例如 206813
    type 默认值 'cache'
    start_at (起始时间）
    end_at(结束时间）

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.request_log(domain_id,
                                        type,
                                        start_at,
                                        end_at)

文件预取::

    参数
    urls 预取url,可以为多个,注意: urls会有域名验证,必须已经平台创建完成。

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.prefetch(urls)


文件预取进度查询::

    参数
    request_id (文件预存操作成功后返回的request_id)

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.cdn.prefetch_query(request_id)

工单 API
============

工单列表::

    参数
    user_id (用户ID）

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.ticket.list(user_id)


单个工单::

    参数
    ticket_id (工单ID）

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.ticket.get(ticket_id)


工单创建::

    参数
    summary (概要)
    description(描述)

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.ticket.create(summary, description)


更新工单状态::

    参数
    ticket_id (工单ID)
    status(状态) 'accepted' 'closed'

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.ticket.update(ticket_id, status)


工单回复列表::

    参数
    ticket_id (工单ID)

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.ticket.list_reply(ticket_id)


工单回复::

    参数
    ticket_id (工单ID)
    content(回复的内容)

    >>> from plcloudclient.v1_0 import client
    >>> plcloud = client.Client(...)
    >>> result = plcloud.ticket.reply(ticket_id, content)
