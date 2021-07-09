from aiohttp import web
from models import User, Post

class Health(web.View):
    def get(self):
        return web.json_response({'status': 'OK!'})

class UserView(web.View):

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user = await User.get_or_404(user_id)
        return web.json_response(user.to_dict())

    async def post(self):
        data = await self.request.json()
        user = await User.create_instance(**data)
        return web.json_response(user.to_dict())

    async def delete(self):
        user_id = int(self.request.match_info['user_id'])
        user = await User.delete_or_404(user_id)
        return web.json_response({'Deleted ID': user})

class PostView(web.View):

    async def get(self):
        post_id = int(self.request.match_info['post_id'])
        post = await Post.get_or_404(post_id)
        return web.json_response(post.to_dict())

    async def delete(self):
        post_id = int(self.request.match_info['post_id'])
        post = await Post.delete_or_404(post_id)
        return web.json_response({'Deleted ID': post})

    async def post(self):
        data = await self.request.json()
        post = await Post.create_instance(**data)
        return web.json_response(post.to_dict())


class UsersView(web.View):

    async def get(self):
        pool = self.request.app['pg_pool']
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT id, username, email FROM public.user')
                users = await cursor.fetchall()
                return web.json_response(users)


class PostsView(web.View):

    async def get(self):
        pool = self.request.app['pg_pool']
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT id, title, text, user_id, created_date FROM public.post')
                posts = await cursor.fetchall()
                return web.json_response(posts)