from sqlalchemy import text
from sqlalchemy import select
from database.database import async_engine, Base, async_session_factory
from database.models import Users, UsersPosts, GenPosts, Criteria, CriteriaData


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def check_user_id(user_id: int):
        async with async_session_factory() as session:
            query = (
                select(select("*").select_from(Users).where(Users.user_id == user_id).exists())
            )
            exist_query = await session.execute(query)
            return exist_query.all()[0][0]

    @staticmethod
    async def add_user_id(user_id: int, username: str):
        async with async_session_factory() as session:
            exist_query = await AsyncORM.check_user_id(user_id)
            if not exist_query:
                exist_query = Users(user_id=user_id, username=username, has_active=True)
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
            exist_query = await AsyncORM.check_user_id(user_id)
            if exist_query:
                exist_query = UsersPosts(user_id=user_id, post=post)
                session.add(exist_query)
                await session.flush()
                await session.commit()
            else:
                await AsyncORM.add_user_id(user_id)
                exist_query = UsersPosts(user_id=user_id, post=post)
                session.add(exist_query)
                await session.flush()
                await session.commit()

    @staticmethod
    async def add_gen_post(user_id: int, post: str):
        async with async_session_factory() as session:
            exist_query = await AsyncORM.check_user_id(user_id)
            if exist_query:
                exist_query = GenPosts(user_id=user_id, post=post)
                session.add(exist_query)
                await session.flush()
                await session.commit()
            else:
                await AsyncORM.add_user_id(user_id)
                exist_query = GenPosts(user_id=user_id, post=post)
                session.add(exist_query)
                await session.flush()
                await session.commit()

    @staticmethod
    async def add_rate(user_id: int, rate: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE gen_posts SET rate=:new_rate WHERE user_id=:id").bindparams(new_rate=int(rate),
                                                                                            id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_flag_active(user_id: int, active: bool):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET has_active=:new_active WHERE user_id=:id").bindparams(new_active=active,
                                                                                                id=user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_flag_active(user_id: int):
        async with async_session_factory() as session:
            exist_query = await AsyncORM.check_user_id(user_id)
            if exist_query:
                query = (
                    select(Users.has_active).select_from(Users).filter_by(user_id=user_id)
                )
                check = await session.execute(query)
                check = check.all()
                return check[0][0]

    @staticmethod
    async def get_topic(user_id: int):
        async with async_session_factory() as session:
            exist_query = await AsyncORM.check_user_id(user_id)
            if exist_query:
                query = (
                    select(Users.topic).select_from(Users).filter_by(user_id=user_id)
                )
                check = await session.execute(query)
                check = check.all()
                return check[0][0]

    @staticmethod
    async def get_type_post(user_id: int):
        async with async_session_factory() as session:
            exist_query = await AsyncORM.check_user_id(user_id)
            if exist_query:
                query = (
                    select(Users.type_post).filter_by(user_id=user_id)
                )
                # stmt = text("SELECT * FROM users WHERE user_id=:id").bindparams(id=user_id)
                check = await session.execute(query)
                # print('adf', check)
                check = check.all()
                return check[0][0]

    @staticmethod
    async def add_criteria(criteria: str):
        async with async_session_factory() as session:
            exist_query = Criteria(criteria=criteria)
            session.add(exist_query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def add_criteria_data(criteria_id: int, criteria_data: str):
        async with async_session_factory() as session:
            exist_query = CriteriaData(criteria_data=criteria_data, criteria_id=criteria_id)
            session.add(exist_query)
            await session.flush()
            await session.commit()

    @staticmethod
    async def get_criteria_data(criteria_id: int, criteria_data_number: int) -> list:
        async with async_session_factory() as session:
            query = (
                select(CriteriaData.criteria_data).select_from(CriteriaData).filter_by(criteria_id=criteria_id)
            )
            criteria_data = await session.execute(query)
            criteria_data = criteria_data.all()[criteria_data_number - 1][0]
            return criteria_data

    @staticmethod
    async def add_structure(user_id: int, structure: str):
        async with async_session_factory() as session:
            stmt = text("UPDATE users SET structure=:new_structure WHERE user_id=:id").bindparams(
                new_structure=structure,
                id=user_id
            )
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_user_data(user_id: int) -> list:
        async with async_session_factory() as session:
            user = (
                select('*').select_from(Users).filter_by(user_id=user_id)
            )
            user_res = await session.execute(user)
            user_res = user_res.all()
            user_data = (
                select('*').select_from(UsersPosts).filter_by(user_id=user_id)
            )
            user_data_res = await session.execute(user_data)
            user_data_res = user_data_res.all()
            result_dic = {}
            if user_data_res:
                result_dic = {
                    'product': user_res[0][5],
                    'structure': user_res[0][8],
                    'history': user_res[0][9],
                    'idea': user_res[0][7],
                    'post': user_data_res[0][2]
                }
            else:
                result_dic = {
                    'product': user_res[0][5],
                    'structure': user_res[0][8],
                    'history': user_res[0][9],
                    'idea': user_res[0][7],
                    'post': 'no'
                }

            return result_dic

            # return result_dic
