## flask demo with mysql

### 环境
1. python 3.7.6
2. mysql 5.7

### 目录结构
    ```
    .
    ├── Dockerfile  # docker文件
    ├── README
    ├── app # 应用目录
    │   ├── __init__.py # 注册蓝图
    │   ├── test    # 测试代码
    ├── application.py  # 配置Flask的app
    ├── common  # 基础公用代码
    │   ├── base_error.py  # 自定义异常
    │   ├── custom_response.py  # 自定义response
    │   ├── decorators.py  # 自定义装饰器
    │   └── service_decorator.py   # 服务装饰器
    ├── config  # 配置文件
    │   ├── config.py   # app配置
    │   └── logger.py   # 日志配置
    ├── db.py   # mysql实例
    ├── application.py   # flask app创建
    ├── instance
    ├── requirements.txt    # python依赖
    ├── run.py  # 单机运行入口
    └── server.py   # gunicorn运行入口
    ```
### mysql初始化
1. 创建数据库
```
CREATE DATABASE art_show IF NOT EXISTS art_show
DEFAULT CHARACTER SET utf8
COLLATE utf_general_ci;
```


### 更新数据库
1. 初始化
	> export FLASK_APP=server:app
    > flask db init
2. 查看变化
    > migrations/env.py 中引入 "from app.show.show_model import Show"
    > flask db migrate
3. 更新
    > flask db upgrade

### 启动
1. 单机启动
    > python run.py
2. gunicorn启动
    > gunicorn -b 0.0.0.0:80 --timeout 600 server:app
3. celery启动
    > celery -A server.my_celery worker --loglevel=info

### 测试
1. 访问 http://localhost:8000/test/
