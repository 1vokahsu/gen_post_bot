import asyncio
from database.queries import AsyncORM


async def main():
    # await AsyncORM.create_tables()
    # await AsyncORM.insert_workers()
    # await AsyncORM.add_user_id(60329246543443, 'askjdh')
    # await AsyncORM.add_topic(60329246543443, "Фитнес")
    # await AsyncORM.add_post(60329246543443, "asdfgh - sdfjg ahsdahjd -")
    print(await AsyncORM.get_flag_active(701275421))
    # print(await AsyncORM.get_sex(701275421))
    # await AsyncORM.add_flag_active(701275421, True)
    # print(users[0])
    # print(users[1])
    # await AsyncORM.update_rate(701275421, False)


if __name__ == "__main__":
    asyncio.run(main())
