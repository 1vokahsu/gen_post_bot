from sqlalchemy import text
from sqlalchemy import select
from database.database import async_engine, Base, async_session_factory
from database.models import Users, UsersPosts, GenPosts


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user_id(user_id: int, username: str):
        async with async_session_factory() as session:
            '''
            SELECT EXISTS (SELECT * FROM users WHERE user_id = 123)
            '''
            query = (
                select(select("*").select_from(Users).where(Users.user_id == user_id).exists())
            )
            exist_query = await session.execute(query)
            exist_query = exist_query.all()[0][0]
            if not exist_query:
                exist_query = Users(user_id=user_id, username=username)
                session.add(exist_query)
                await session.flush()
                await session.commit()

    @staticmethod
    async def add_topic(user_id: int, topic: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET topic=:new_topic WHERE user_id=:id").bindparams(new_topic=topic, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_target(user_id: int, target: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET target=:new_target WHERE user_id=:id").bindparams(new_target=target,
                                                                                            id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_product(user_id: int, product: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET product=:new_product WHERE user_id=:id").bindparams(new_product=product,
                                                                                              id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_type_post(user_id: int, type_post: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET type_post=:new_type_post WHERE user_id=:id").bindparams(
                new_type_post=type_post, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_idea(user_id: int, idea: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET idea=:new_idea WHERE user_id=:id").bindparams(new_idea=idea, id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_history(user_id: int, history: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET history=:new_history WHERE user_id=:id").bindparams(new_history=history,
                                                                                              id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_post(user_id: int, post: str):
        async with async_session_factory() as session:
            exist_query = UsersPosts(user_id=user_id, post=post)
            session.add(exist_query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def add_gen_post(user_id: int, post: str):
        async with async_session_factory() as session:
            exist_query = GenPosts(user_id=user_id, post=post)
            session.add(exist_query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def add_rate(user_id: int, rate: int):
        async with async_session_factory() as session:
            stmt = text("UPDATE gen_posts SET rate=:new_rate WHERE user_id=:id").bindparams(new_rate=int(rate),
                                                                                            id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_topic(user_id: int):
        async with async_session_factory() as session:
            query = (
                select(Users.topic).select_from(Users).filter_by(user_id=user_id)
            )
            check = await session.execute(query)
            check = check.all()

            return check[0][0]
