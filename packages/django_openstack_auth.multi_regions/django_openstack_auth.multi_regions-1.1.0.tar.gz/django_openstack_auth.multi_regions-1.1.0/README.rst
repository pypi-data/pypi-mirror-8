==============================
openstack_auth.multi_regions
==============================
*宝德云多区域切换库 (http://console.plcloud.com)*

依赖
-----------
1. openstack_auth > 1.1.4


配置方法
------------

1. 修改openstack_dashboard/urls.py文件, 替换auth url

::

  - url(r'^auth/', include('openstack_auth.urls'))
  + url(r'^auth/', include('openstack_auth.multi_regions.urls'))


2. 修改openstack_dashboard/settings.py文件,添加multi_regions app

::

  INSTALLED_APPS = (
      '''
      'openstack_auth.multi_regions',
      '''
  )


3. 配置local_settings.py 添加MULTI_REGIONS

::

  MULTI_REGIONS = [
      ('http://10.0.0.1:5000/v2.0', 'beijing', 'BeiJing-1(PEK-1)'),
      ('http://172.16.0.1:5000/v2.0', 'shenzhen', 'ShenZhen-1(SZX-1)'),
      ('http://192.168.100.1:5000/v2.0', 'lab-test', 'Lab-Test-1(Lab-1)'),
  ]
  OPENSTACK_KEYSTONE_URL = MULTI_REGIONS[0][0]

