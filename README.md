# 基于NETCONF的配置管理系统
# changeLog
* 20210502 更新到v2.1.0版本：
    1. 修复添加position后的数据显示问题。
    2. 往系统目前已有的配置模板都添加数据位置。
* 20210206 更新到v2.0.1版本：
    1. 模板需要指定position，定位显示的数据位置（父字节的标签名），通过标签名的方式获取。
    2. 参数可以指定key角色，该参数在显示数据时，该数据列隐藏（因为后台没有返回key参数的内容）。
* 20210131 更新到v2.0.0版本：
    1. 根据params动态生成配置数据展示。
    2. 模板参数新增label参数，显示表单的标题和表格的标题。
    3. 特别，因为改用params生成显示表格，原来get的方式的模板也需要配置参数！

## 功能

## 依赖
项目依赖在*requests.txt*。
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
