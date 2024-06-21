import asyncio
import csv
import datetime
import random

from database.queries import AsyncORM


# функция записи в БД критериев и генерация списка критериев
async def add_criteria_data(file_criteria: str, file_criteria_data: str) -> None:
    print(f'{datetime.datetime.now()} [INFO] collecting criteria from {file_criteria}')
    with open(file_criteria, 'r+') as file:
        reader = list(csv.reader(file))
        print(f'{datetime.datetime.now()} [OK] criteria from {file_criteria} collected')
        count = 0
        for cr in reader:
            critera = cr[0]
            if critera != 'Критерий':
                count += 1
                print(f'{datetime.datetime.now()} [INFO] write criteria: {critera} to db')
                await AsyncORM.add_criteria(criteria=critera)
                print(f'{datetime.datetime.now()} [OK] criteria: {critera} writed')
                for i in range(1, 11):
                    criteria_data = critera + '_' + str(i)
                    print(f'{datetime.datetime.now()} [INFO] write criteria_data: {criteria_data} to db')
                    await AsyncORM.add_criteria_data(criteria_id=count, criteria_data=criteria_data)
                    print(f'{datetime.datetime.now()} [OK] criteria_data: {criteria_data} writed')


# функция генерации предложения
async def gen_sentence() -> str:
    sentence = ''
    for i in range(1, 36):
        sentence += await AsyncORM.get_criteria_data(i, random.randint(1, 10)) + ' '

    return sentence


async def main():
    # await AsyncORM.create_tables()
    # await add_criteria_data(file_criteria='data/criteria.csv', file_criteria_data='')
    # print(await AsyncORM.get_criteria_data(1, 5))
    print(await gen_sentence())

if __name__ == "__main__":
    asyncio.run(main())
