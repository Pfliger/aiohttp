import aiopg
import config
from aiohttp import web
import asyncio
from models import db
from views import Health, PostView, PostsView, UserView, UsersView



async def register_pg_pool(app):
    async with aiopg.pool.create_pool(config.DB_DSN) as pool:
        app['pg_pool'] = pool
        yield

async def register_orm(app):

    await db.set_bind(config.DB_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = web.Application()
app.cleanup_ctx.append(register_pg_pool)
app.cleanup_ctx.append(register_orm)
app.add_routes([web.get('/', Health)])
app.add_routes([web.get(r'/user/{user_id:\d+}', UserView)])
app.add_routes([web.post('/user', UserView)])
app.add_routes([web.get('/users', UsersView)])
app.add_routes([web.get(r'/post/{post_id:\d+}', PostView)])
app.add_routes([web.post('/post', PostView)])
app.add_routes([web.get('/posts', PostsView )])
app.add_routes([web.delete(r'/post/{post_id:\d+}', PostView)])
app.add_routes([web.delete(r'/user/{user_id:\d+}', UserView)])
web.run_app(app, port=8080)