# 基于NETCONF的配置管理系统（华为CE系列）
# logging
20210131 更新到v2.0.0版本：
    1.根据params动态生成配置数据展示。
    2.模板参数新增label参数，显示表单的标题和表格的标题。
    3.特别，因为改用params生成显示表格，原来get的方式的模板也需要配置参数！

## 功能

## 依赖
* django
* django-cors-headers
* pymysql
* djangorestframework
* django-filter
* djangorestframework-jwt
* ncclient
* ping3
* xmltodict

## 运行
python manage.py runserver 127.0.0.1:8282