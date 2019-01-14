import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


"""
g是一个特殊的对象，对于每一个请求都是唯一的。它用于存储请求期间可能由多个函数访问的数据。
如果在同一请求中第二次调用get_db，则存储并重用连接而不是创建新连接。

current_app 是另一个指向处理请求的Flask应用程序的特殊对象。由于您使用的是应用程序工厂，
因此在编写其余代码时没有应用程序对象。创建应用程序并处理请求时将调用get_db，
因此可以使用current_app。 

sqlite3.connect（）建立与DATABASE配置键指向的文件的连接。此文件尚不存在，并且在您稍后
初始化数据库之前不会存在。

sqlite3.Row 告诉连接返回行为类似于dicts的行。这允许按名称访问列。

Close_db通过检查是否已设置g.db来检查是否创建了连接。如果连接存在，则关闭。 
再往下，您将告诉您的应用程序有关应用程序工厂中的close_db函数，以便在每次请求后调用它。
"""


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


"""
open_resource()打开一个相对于flaskr包的文件，这很有用，因为您以后在部署应用程序时不一定知道该位置的位置。
get_db返回数据库连接，用于执行从文件读取的命令。

click.command()定义了一个名为init-db的命令行命令，该命令调用init_db函数并向用户显示成功消息。
您可以阅读命令行界面以了解有关编写命令的更多信息。
"""


def init_app(app):
    """如果要执行close_db和init_db_command方法需要注册"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


"""
app.teardown_appcontext()告诉Flask在返回响应后清理时调用该函数。

app.cli.add_command()添加了一个可以使用flask命令调用的新命令。
"""