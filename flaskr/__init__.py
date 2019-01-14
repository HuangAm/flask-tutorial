import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)  # creates the Flask instance
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )  # set some default configuration that the app will use

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
"""
create_app是application的工厂函数。您将在本教程的后面添加它，但它已经做了很多。
1.app = Flask(__name__,instance_relative_config=True) 创建Flask实例。
    - __name__是当前python模块的名字。app需要知道它所在的位置以设置一些路径，
      并且__name__是一种方便的告诉它的方式。
    - instance_relative_config=True 告诉app配置文件是相对于实例文件夹的。
      实例文件夹位于flaskr包之外，可以保存不应提交给版本控制的本地数据，例如
      配置机密和数据库文件。
2.app.config.from_mapping() 设置应用程序将使用的一些默认配置：
    - SECRET_KEY Flask和扩展使用它来保证数据安全。它被设置为'dev'以在开发期
      间提供方便的值，但在部署时应该用随机值覆盖它。
    - DATABASE 是保存SQLite数据库文件的路径。它位于app.instance_path下，
      这是Flask为实例文件夹选择的路径。
3.app.config.from_pyfile() 使用从实例文件夹中的config.py文件获取的值覆盖默
认配置（如果存在）。例如，在部署时，这可用于设置真正的SECRET_KEY。
    - test_config 也可以传递给工厂，并将用于代替实例配置。这样您将在本教程后面
      编写的测试可以独立于您配置的任何开发值进行配置。
4.os.makedirs() 确保app.instance_path存在。Flask不会自动创建实例文件夹，但需
要创建它，因为您的项目将在那里创建SQLite数据库文件。
5.@app.route()创建一个简单的路由，以便在进入本教程的其余部分之前可以看到应用程序正常工作。
它在URL /hello 和返回响应的函数之间创建了一个连接，字符串'Hello，World！'在这种情况下。
"""