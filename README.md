# SSRP-Dev
dev repo for demo version

## Tech Stack
- Scrapy1.7.4 or just Request
- Elasticsearch 7.6.1 & Kibana 7.6.1
- Django 3.0.4
- D2_admin(Vue) 1.8
- ...

## Language
- Python 3.7
- vue.js(ECMA6)
- ...

## Plugin
- ES analysis-pinyin 7.6.1
- ES analysis-ik 7.6.1
- ...


## File Structure
- .iData     放置scrapy爬虫文件，爬虫名是idata
   - .spiders     主文件夹
     - _init_.py
     - iData_spider.py  爬虫主文件
   - _init_.py    初始文件
   - items.py         爬虫字段定义
   - middlewares.py       爬虫中间件
   - pipelines.py       连接数据库
   - settings.py        爬虫设置
   - proxy_pool.py      代理池
   - user_agent.py     请求头
   - main.py          命令行启动爬虫
   - LOG.text   爬虫日志

- .IDataSearch      放置项目前后端文件
  - .IDataSearch  django主文件夹
    - _init_.py
    - urls.py     主路由
    - wsgi.py     python网关接口
    - asgi.py     异步网关协议
    - settings.py   
  - .backdoor   django-app
    - _init_.py
    - admin.py      django自带后台管理
    - apps.py
    - models.py   模型
    - tests.py
    - urls.py     子路由
    - views.py    视图
    - .migrations  数据库迁移
  - .frontdoor/d2_admin  vue文件夹     
    - .public                         
    - .src                              
    - ...                             
  - db.sqlite3  django自带数据库文件
  - manage.py   创建站点脚本

- .idea           工作目录
- scrapy.cfg     保存用户设置

## About frontdoor
- 暂时使用vue框架下的中后台管理系统d2_admin_smart_kit，后续根据需求更换
- 框架说明来自[d2_admin](https://d2.pub/zh/doc/d2-admin/component/container.html#%E6%A8%A1%E5%BC%8F-card)
- 页面组件来自[element-ui](https://element.eleme.cn/#/zh-CN/component/menu)
- icon来自[fontawesome](https://fontawesome.com）
- 开发调试：![启动命令.jpg](https://ws1.sinaimg.cn/large/85df5809gy1gdbv49ec0qj20kx0dpt9r.jpg)
- ...

## About backdoor
- Django教程来自[刘江的博客](https://www.liujiangblog.com/course/django/2)
- Django DRF框架来自[django-restful-framework](https://q1mi.github.io/Django-REST-framework-documentation/tutorial/2-requests-and-responses_zh)
- ...

## About Vue & Django
- [掘金文章](https://juejin.im/post/5e36d5dc51882520ea398f21)
- [知乎文章](https://zhuanlan.zhihu.com/p/54776124)
- ...

## About Scrapy & Django
- [Scrapy官方文档](https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/djangoitem.html)
- [Theodo Blog](https://blog.theodo.com/2019/01/data-scraping-scrapy-django-integration/)
- ...

## About Elasticsearch & Django
- [CSDN Blog](https://blog.csdn.net/weixin_42149982/article/details/82390900)
- [简书](https://www.jianshu.com/p/46eb88a4e489)
- ...

## todo
- 前端细节完善
- **后端数据库建立，api接口，路由分配等功能实现**
- ES & Django & 爬虫(Scrapy)连接
- 前后端连接
