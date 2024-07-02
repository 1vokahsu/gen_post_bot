import datetime

import gen_scripts as gen
from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, ChatMemberUpdated
from aiogram.filters import CommandStart, StateFilter, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import kb
from database.queries import AsyncORM
from voice_handler import voice_trans

router: Router = Router()


class FSMFillForm(StatesGroup):
    upload_topic = State()
    upload_target = State()
    upload_product = State()
    upload_posts = State()
    upload_idea = State()
    upload_history = State()


# хэндлер обработки /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    print(f'{datetime.datetime.now()} - [INFO] Юзер {message.from_user.id} нажал /start ')
    await message.answer(
        text='Привет!\n'
             'Давай начнем - расскажи немного о себе.\n'
             'Пройди небольшой опрос (всего 3 шага), чтобы я смог лучше тебе помочь и быть более полезным.\n\n'
             '<b>Для начала ответь на вопрос:</b>\n'
             'Какая тематика твоего блога -  чем ты рассказываешь в своем блоге?\n'
             '<i>Например:</i>\n'
             '<i>Фитнес - рассказываю как похудеть.</i>\n\n'
             '____\n'
             '<i>Кстати, ты можешь использовать голосовые сообщения для ответа.</i>'
    )
    print(f'{datetime.datetime.now()} - [INFO] Добавляем user_id {message.from_user.id} в бд')
    await AsyncORM.add_user_id(message.from_user.id, message.from_user.username)
    print(f'{datetime.datetime.now()} - [INFO] set state for {message.from_user.id}')
    await state.set_state(FSMFillForm.upload_topic)


# хэндлер обработки состояния для обработки темы поста
@router.message(StateFilter(FSMFillForm.upload_topic), lambda x: x.text or x.voice)
async def process_topic(message: Message,
                        state: FSMContext,
                        bot: Bot
                        ):
    print(f'{datetime.datetime.now()} - [INFO] state topic check TOPIC')
    user_id = message.from_user.id
    if message.voice:
        print(f'{datetime.datetime.now()} - [INFO] collecting voice data')
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(f'{datetime.datetime.now()} - [INFO] download voice data')
        file_name = f"./data/audio_{file_id}.mp3"
        await bot.download_file(file_path, file_name)
        print(f'{datetime.datetime.now()} - [INFO] voice transcriptions')
        topic = await voice_trans(file_name)
        if topic is not None:
            print(f'{datetime.datetime.now()} - [OK] topic exist')
            print(f'{datetime.datetime.now()} - [INFO] write data to db')
            await AsyncORM.add_topic(user_id, topic)
        else:
            print(f'{datetime.datetime.now()} - [ERROR] topic not exist')
    else:
        print(f'{datetime.datetime.now()} - [INFO] collecting text data')
        topic = message.text
        print(f'{datetime.datetime.now()} - [INFO] text {topic} from {user_id}')
        await AsyncORM.add_topic(user_id, topic)
        print(f'{datetime.datetime.now()} - [INFO] write data to db')

    await message.answer(
        text='Круто!\n'
             'Давай продолжим?\n\n'
             'Кто целевая аудитория твоего блога? (какие люди в основном на тебя подписываются).\n'
             'Можешь просто своими словами описать их.\n\n'
             '<i>Например:</i>\n'
             '<i>В основном это семейные пары, которые хотят наладить свои отношения</i>\n\n'
             '____\n'
             '<i>Ты также можешь использовать голосовые сообщения для ответа :)</i>'
    )
    await state.set_state(FSMFillForm.upload_target)


# хэндлер ловит невалидные сообщения темы поста
@router.message(StateFilter(FSMFillForm.upload_topic))
async def process_no_topic(message: Message):
    print(f"{datetime.datetime.now()} - [INFO] Ловим юзера {message.from_user.id} на невалидных данных TOPIC")
    await message.answer(
        text='То, что ты отправил, не похоже на тематику блога.\n\n'
             'Какая тематика твоего блога -  чем ты рассказываешь в своем блоге?\n'
             '<i>Например:</i>\n'
             '<i>Фитнес - рассказываю как похудеть.</i>\n\n'
             '____\n'
             '<i>Кстати, ты можешь использовать голосовые сообщения для ответа.</i>'
    )


# хэндлер обработки состояния для обработки целевой аудитории
@router.message(StateFilter(FSMFillForm.upload_target), lambda x: x.text or x.voice)
async def process_target(message: Message,
                         state: FSMContext,
                         bot: Bot
                         ):
    print(f'{datetime.datetime.now()} - [INFO] state target check TARGET')
    user_id = message.from_user.id

    if message.voice:
        print(f'{datetime.datetime.now()} - [INFO] collecting voice data')
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(f'{datetime.datetime.now()} - [INFO] download voice data')
        file_name = f"./data/audio_{file_id}.mp3"
        await bot.download_file(file_path, file_name)
        print(f'{datetime.datetime.now()} - [INFO] voice transcriptions')
        target = await voice_trans(file_name)
        if target is not None:
            print(f'{datetime.datetime.now()} - [OK] target exist')
            print(f'{datetime.datetime.now()} - [INFO] text {target} from {user_id}')
            await AsyncORM.add_target(user_id, target)
            print(f'{datetime.datetime.now()} - [INFO] write data to db')
        else:
            print(f'{datetime.datetime.now()} - [ERROR] target not exist')
    else:
        print(f'{datetime.datetime.now()} - [INFO] collecting text data')
        target = message.text
        print(f'{datetime.datetime.now()} - [INFO] text {target} from {user_id}')
        await AsyncORM.add_target(user_id, target)
        print(f'{datetime.datetime.now()} - [INFO] write data to db')

    await message.answer(
        text='Последний вопрос 🙂\n'
             'Продаешь ли ты какие либо продукты в своем блоге?\n\n'
             'Если да - то скажи что это за продукт и какой оффер (обещание) ты сейчас используешь.\n\n'
             '<i>Например:</i>\n'
             '<i>Продаю курсы по подготовке к ЕГЭ по математике. Мой оффер - 95% моих учеников сдают ЕГЭ на 100 '
             'баллов всего за 3 месяца подготовки.</i>\n\n'
             '____\n'
             '<i>Ты также можешь использовать голосовые сообщения для ответа :)</i>'
    )
    await state.set_state(FSMFillForm.upload_product)


# хэндлер невалидные сообщения целевой аудитории
@router.message(StateFilter(FSMFillForm.upload_target))
async def process_no_target(message: Message):
    print(f'{datetime.datetime.now()} - [INFO] Ловим юзера {message.from_user.id} на невалидных данных TARGET')
    await message.answer(
        text='То, что ты отправил, не похоже на целевую аудиторию твоего блога.\n\n'
             'Можешь просто своими словами описать её.\n\n'
             '<i>Например:</i>\n'
             '<i>В основном это семейные пары, которые хотят наладить свои отношения</i>\n\n'
             '____\n'
             '<i>Ты также можешь использовать голосовые сообщения для ответа :)</i>'
    )


# хэндлер обработки состояния для обработки наличия продукта у пользователя
@router.message(StateFilter(FSMFillForm.upload_product), lambda x: x.text or x.voice)
async def process_product(message: Message,
                          state: FSMContext,
                          bot: Bot):
    print(f'{datetime.datetime.now()} - [INFO] state target check PRODUCT')
    user_id = message.from_user.id

    if message.voice:
        print(f'{datetime.datetime.now()} - [INFO] collecting voice data')
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(f'{datetime.datetime.now()} - [INFO] download voice data')
        file_name = f"./data/audio_{file_id}.mp3"
        await bot.download_file(file_path, file_name)
        print(f'{datetime.datetime.now()} - [INFO] voice transcriptions')
        product = await voice_trans(file_name)
        if product is not None:
            print(f'{datetime.datetime.now()} - [OK] product exist')
            print(f'{datetime.datetime.now()} - [INFO] product {product} from {user_id}')
            await AsyncORM.add_product(user_id, product)
            print(f'{datetime.datetime.now()} - [INFO] write data to db')
        else:
            print(f'{datetime.datetime.now()} - [ERROR] product not exist')
    else:
        print(f'{datetime.datetime.now()} - [INFO] collecting text data')
        product = message.text
        print(f'{datetime.datetime.now()} - [INFO] product {product} from {user_id}')
        await AsyncORM.add_product(user_id, product)
        print(f'{datetime.datetime.now()} - [INFO] write data to db')

    kb_ = InlineKeyboardMarkup(
        inline_keyboard=[[kb.skip_btn]]
    )
    await message.answer(
        text='Можешь скинуть мне пару своих предыдущих постов?\n'
             'Я буду использовать их для того, чтобы писать текста более подходящие под твой стиль.\n\n'
             'Если у тебя нет постов или ты не можешь их сейчас скинуть - ничего страшного, просто нажми “Пропустить”.',
        reply_markup=kb_
    )
    await state.set_state(FSMFillForm.upload_posts)


# хэндлер ловит невалидные сообщения про наличие продукта у пользователя
@router.message(StateFilter(FSMFillForm.upload_product))
async def process_no_product(message: Message):
    print(f'{datetime.datetime.now()} - [INFO] Ловим юзера {message.from_user.id} на невалидных данных PRODUCT')
    await message.answer(
        text='То, что ты отправил, не совсем тот ответ, которого я ожидал.\n'
             'Давай попробуем еще раз.\n\n'
             'Продаешь ли ты какие либо продукты в своем блоге?\n\n'
             'Если да - то скажи что это за продукт и какой оффер (обещание) ты сейчас используешь.\n\n'
             '<i>Например:</i>\n'
             '<i>Продаю курсы по подготовке к ЕГЭ по математике. Мой оффер - 95% моих учеников сдают ЕГЭ на 100 '
             'баллов всего за 3 месяца подготовки.</i>\n\n'
             '____\n'
             '<i>Ты также можешь использовать голосовые сообщения для ответа :)</i>'
    )


# хэндлер обработки состояния наличия предыдущих постов у пользователя
@router.message(StateFilter(FSMFillForm.upload_posts), lambda x: x.text or x.voice)
async def process_posts(message: Message,
                        state: FSMContext,
                        bot: Bot):

    print(f'{datetime.datetime.now()} - [INFO] state target check POSTS')
    user_id = message.from_user.id

    if message.voice:
        print(f'{datetime.datetime.now()} - [INFO] collecting voice data')
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(f'{datetime.datetime.now()} - [INFO] download voice data')
        file_name = f"./data/audio_{file_id}.mp3"
        await bot.download_file(file_path, file_name)
        print(f'{datetime.datetime.now()} - [INFO] voice transcriptions')
        posts = await voice_trans(file_name)
        if posts is not None:
            print(f'{datetime.datetime.now()} - [OK] posts exist')
            print(f'{datetime.datetime.now()} - [INFO] posts {posts} from {user_id}')
            await AsyncORM.add_post(user_id, posts)
            print(f'{datetime.datetime.now()} - [INFO] write data to db')
        else:
            print(f'{datetime.datetime.now()} - [ERROR] posts not exist')
    else:
        print(f'{datetime.datetime.now()} - [INFO] collecting text data')
        posts = message.text
        print(f'{datetime.datetime.now()} - [INFO] posts {posts} from {user_id}')
        await AsyncORM.add_post(user_id, posts)
        print(f'{datetime.datetime.now()} - [INFO] write data to db')

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    kb_ = InlineKeyboardMarkup(
        inline_keyboard=[[kb.continue_btn]]
    )
    await message.answer(
        text='Пришли еще или нажми “продолжить”',
        reply_markup=kb_
    )
    await state.set_state(FSMFillForm.upload_posts)


# хэндлер ловит невалидные сообщения про наличие постов у пользователя
@router.message(StateFilter(FSMFillForm.upload_posts))
async def process_no_posts(message: Message):
    print(f'{datetime.datetime.now()} - Ловим юзера {message.from_user.id} на невалидных данных POSTS')
    kb_ = InlineKeyboardMarkup(
        inline_keyboard=[[kb.skip_btn]]
    )
    await message.answer(
        text='Можешь скинуть мне пару своих предыдущих постов?\n'
             'Я буду использовать их для того, чтобы писать текста более подходящие под твой стиль.\n\n'
             'Если у тебя нет постов или ты не можешь их сейчас скинуть - ничего страшного, просто нажми “Пропустить”.',
        reply_markup=kb_
    )


# хэндлер обработки кнопок "пропустить" или "продолжить"
@router.callback_query(F.data == "skip")
async def process_skip(callback: CallbackQuery, state: FSMContext):
    print(f'{datetime.datetime.now()} - [INFO] Юзер {callback.from_user.id} нажал на кнопку \"пропустить\" или \"продолжить\"')
    print(f'{datetime.datetime.now()} - [INFO] Чистим состояние')
    await state.clear()
    kb_ = InlineKeyboardMarkup(
        inline_keyboard=[[kb.seller_btn], [kb.engaging_btn]]
    )

    await callback.message.edit_text(
        text='Теперь давай начнем наполнять твой блог?\n\n'
             'Напиши мне какой пост ты хотел бы написать:\n'
             '\t1. <b>Продающий</b> - пост, после которого, твои читатели будут кидать деньги в экран и писать '
             'тебе в'
             'личку, чтобы не упустить шанс купить твой продукт.\n'
             '\t2. <b>Вовлекающий</b> - твои читатели будут плакать и смеяться у своих экранов, их сердца будут '
             'рекой'
             'сыпаться в виде лайков, а критики назовут твой пост самым ярким событием в этом году.',
        reply_markup=kb_
    )
    await callback.answer()


# хэндлер обработки кнопок "Продающий" или "Вовлекающий"
@router.callback_query(F.data.in_(['seller', 'engaging']))
async def process_skip(callback: CallbackQuery):
    user_id = callback.from_user.id
    print(f'{datetime.datetime.now()} - [INFO] Юзер {user_id} нажал на кнопку \"Продающий\" или \"Вовлекающий\"')
    if callback.data == 'seller':
        type_post = 'Продающий'
    else:
        type_post = 'Вовлекающий'
    print(f'{datetime.datetime.now()} - [INFO] write {type_post} to db')
    await AsyncORM.add_type_post(user_id, type_post)
    kb_ = InlineKeyboardMarkup(
        inline_keyboard=[[kb.say_btn], [kb.offer_btn]]
    )
    await callback.message.edit_text(
        text='Окей, у тебя уже есть задумка по теме этого поста?\n'
             'Опиши или надиктуй мне её.\n\n'
             'Если нет - то ничего страшного, давай я сам подберу подходящую и задам тебе несколько вопросов.\n',
        reply_markup=kb_
    )
    await callback.answer()


# хэндлер обработки кнопки "Мне есть что сказать"
@router.callback_query(F.data == 'say')
async def process_idea_yes(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    print(f'{datetime.datetime.now()} - [INFO] Юзер {user_id} нажал на кнопку “Мне есть что сказать”')
    print(f'{datetime.datetime.now()} - [INFO] set state upload idea')
    await state.set_state(FSMFillForm.upload_idea)
    if callback.message.text != 'Окей, у тебя уже есть задумка по теме этого поста?\n' \
                                'Опиши или надиктуй мне её.\n\n' \
                                'Если нет - то ничего страшного, давай я сам подберу подходящую и задам тебе ' \
                                'несколько вопросов.\n':
        await callback.message.edit_text(
            text='Супер, опиши или надиктуй мне свою идею.\n\n'
                 '____\n'
                 '<i>Ты также можешь использовать голосовые сообщения для ответа :)</i>'
        )
    await callback.answer()


# хэндлер обработки состояния идеи постов пользователя
@router.message(StateFilter(FSMFillForm.upload_idea), lambda x: x.text or x.voice)
async def process_idea(message: Message,
                       state: FSMContext,
                       bot: Bot):

    print(f'{datetime.datetime.now()} - [INFO] state target check IDEA')
    user_id = message.from_user.id

    if message.voice:
        print(f'{datetime.datetime.now()} - [INFO] collecting voice data')
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(f'{datetime.datetime.now()} - [INFO] download voice data')
        file_name = f"./data/audio_{file_id}.mp3"
        await bot.download_file(file_path, file_name)
        print(f'{datetime.datetime.now()} - [INFO] voice transcriptions')
        idea = await voice_trans(file_name)
        if idea is not None:
            print(f'{datetime.datetime.now()} - [OK] idea exist')
            print(f'{datetime.datetime.now()} - [INFO] idea {idea} from {user_id}')
            await AsyncORM.add_idea(user_id, idea)
            print(f'{datetime.datetime.now()} - [INFO] write data to db')
        else:
            print(f'{datetime.datetime.now()} - [ERROR] idea not exist')
    else:
        print(f'{datetime.datetime.now()} - [INFO] collecting text data')
        idea = message.text
        print(f'{datetime.datetime.now()} - [INFO] idea {idea} from {user_id}')
        await AsyncORM.add_idea(user_id, idea)
        print(f'{datetime.datetime.now()} - [INFO] write data to db')
    '''
        алгоритм для подбора структуры постов
    '''
    kb_ = InlineKeyboardMarkup(
        inline_keyboard=[[kb.agree_btn], [kb.disagree_btn]]
    )
    structure = f'\t1. Тема: {await AsyncORM.get_topic(user_id)}\n' \
                f'\t2. Цель нашего поста: {await AsyncORM.get_type_post(user_id)}\n' \
                f'\t3. Какие приемы будем использовать:\n' \
                f'\t\ta. {await gen.gen_sentence()}\n' \
                f'\t\tb. {await gen.gen_sentence()}\n' \
                f'\t\tc. {await gen.gen_sentence()}\n' \
                f'\t4. Чем разбавим текст: {await gen.gen_sentence()}\n' \
                f'\t5. Какие триггеры будем использовать: {await gen.gen_sentence()}\n' \
                f'\t6. Каким призывом закроем пост: {await gen.gen_sentence()}\n\n'
    await AsyncORM.add_structure(user_id=user_id, structure=structure)
    await message.answer(
        text='Смотри, вот такой пост нам точно подойдет:\n\n'
             f'{structure}'
             'Если ты согласен - то просто ответь на следующий вопрос:\n'
             '\t - Смотри, для создания текста мне понадобиться какая-то твоя личная история, расскажи о том, '
             'о какой-нибудь интересной истории, которая приключилась с тобой в последнее время (можно буквально '
             'в 3х '
             'предложениях).\n\n'
             'Если не согласен со структурой - то просто скажи что тебе не понравилось и я переделаю)\n\n'
             '____\n'
             '<i>Напоминаю, ты можешь использовать голосовые сообщения для ответа :)</i>\n\n',
        reply_markup=kb_
    )
    await state.clear()


# хэндлер ловит невалидные сообщения идей постов
@router.message(StateFilter(FSMFillForm.upload_idea))
async def process_no_idea(message: Message):
    print(f'{datetime.datetime.now()} - Ловим юзера {message.from_user.id} на невалидных данных IDEA')
    await message.answer(
        text='Пожалуйста, опиши или надиктуй мне её.\n\n'
             '____\n'
             '<i>Ты также можешь использовать голосовые сообщения для ответа :)</i>'
    )


# хэндлер обработки кнопок "Нет, предложи” или "Не согласен"
@router.callback_query(F.data.in_(['offer', 'disagree']))
async def process_idea_offer(callback: CallbackQuery):
    user_id = callback.from_user.id
    print(f'{datetime.datetime.now()} - [INFO] Юзер {user_id} нажал на кнопку “Нет, предложи” или \"Не согласен\"')
    await AsyncORM.add_idea(user_id, 'no')
    print(f'{datetime.datetime.now()} - [INFO] write idea NO to db')
    '''
    из функции с алгоритмом для подбора структуры постов достаем структуру
    '''
    kb_ = InlineKeyboardMarkup(
        inline_keyboard=[[kb.agree_btn], [kb.disagree_btn]]
    )
    structure = f'\t1. Тема: {await AsyncORM.get_topic(user_id)}\n' \
                f'\t2. Цель нашего поста: {await AsyncORM.get_type_post(user_id)}\n' \
                f'\t3. Какие приемы будем использовать:\n' \
                f'\t\ta. {await gen.gen_sentence()}\n' \
                f'\t\tb. {await gen.gen_sentence()}\n' \
                f'\t\tc. {await gen.gen_sentence()}\n' \
                f'\t4. Чем разбавим текст: {await gen.gen_sentence()}\n' \
                f'\t5. Какие триггеры будем использовать: {await gen.gen_sentence()}\n' \
                f'\t6. Каким призывом закроем пост: {await gen.gen_sentence()}\n\n'
    await AsyncORM.add_structure(user_id=user_id, structure=structure)
    if not callback.message.text.startswith('Смотри, вот') or not callback.message.text.startswith('Окей, у тебя'):
        await callback.message.edit_text(
            text='Смотри, вот такой пост нам точно подойдет:\n\n'
                 f'{structure}'
                 'Если ты согласен - то просто ответь на следующий вопрос:\n'
                 '\t - Смотри, для создания текста мне понадобиться какая-то твоя личная история, расскажи о том, '
                 'о какой-нибудь интересной истории, которая приключилась с тобой в последнее время (можно буквально '
                 'в 3х '
                 'предложениях).\n\n'
                 'Если не согласен со структурой - то просто скажи что тебе не понравилось и я переделаю)\n\n'
                 '____\n'
                 '<i>Напоминаю, ты можешь использовать голосовые сообщения для ответа :)</i>\n\n',
            reply_markup=kb_
        )
    await callback.answer()


# хэндлер обработки кнопок "Согласен”
@router.callback_query(F.data == 'agree')
async def process_idea_offer(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    print(f'{datetime.datetime.now()} - [INFO] Юзер {user_id} нажал на кнопку “Согласен”')
    await callback.message.edit_text(
        text='Супер!\nВнимательно слушаю вашу историю\n\n'
             '____\n'
             '<i>Напоминаю, ты можешь использовать голосовые сообщения для ответа :)</i>\n\n'
    )
    await callback.answer()
    await state.set_state(FSMFillForm.upload_history)


# хэндлер обработки состояния историю пользователя
@router.message(StateFilter(FSMFillForm.upload_history), lambda x: x.text or x.voice)
async def process_idea(message: Message,
                       state: FSMContext,
                       bot: Bot):

    print(f'{datetime.datetime.now()} - [INFO] state target check HISTORY')
    user_id = message.from_user.id

    if message.voice:
        print(f'{datetime.datetime.now()} - [INFO] collecting voice data')
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        print(f'{datetime.datetime.now()} - [INFO] download voice data')
        file_name = f"./data/audio_{file_id}.mp3"
        await bot.download_file(file_path, file_name)
        print(f'{datetime.datetime.now()} - [INFO] voice transcriptions')
        history = await voice_trans(file_name)
        if history is not None:
            print(f'{datetime.datetime.now()} - [OK] history exist')
            print(f'{datetime.datetime.now()} - [INFO] history {history} from {user_id}')
            await AsyncORM.add_history(user_id, history)
            print(f'{datetime.datetime.now()} - [INFO] write data to db')
        else:
            print(f'{datetime.datetime.now()} - [ERROR] history not exist')
    else:
        print(f'{datetime.datetime.now()} - [INFO] collecting text data')
        history = message.text
        print(f'{datetime.datetime.now()} - [INFO] history {history} from {user_id}')
        await AsyncORM.add_history(user_id, history)
        print(f'{datetime.datetime.now()} - [INFO] write data to db')

    '''
    1. Используя функцию, генерируем пост с помощью GPT.
    2. Записываем пост в БД
    '''
    user_data = await AsyncORM.get_user_data(user_id)
    structure = user_data['structure']
    product = user_data['product']
    idea = user_data['idea']
    history = user_data['history']
    post = user_data['post']
    if post == 'no' and idea == 'no':
        promt = 'Сгенерируй пост.\n\n' \
                'Вот такая структура должна быть у поста:\n' \
                f'{structure}\n' \
                'Также учти, что у меня есть свой продукт, вот его короткое описание:\n' \
                f'{product}\n\n' \
                'Моя личная история, которая приключилась со мной в последнее время :\n' \
                f'{history}'
    elif post == 'no' and idea != 'no':
        promt = 'Сгенерируй пост.\n\n' \
                'Вот такая структура должна быть у поста:\n' \
                f'{structure}\n' \
                'Также учти, что у меня есть свой продукт, вот его короткое описание:\n' \
                f'{product}\n\n' \
                'У меня есть идея для поста, вот ее короткое описание:\n' \
                f'{idea}\n\n' \
                'Моя личная история, которая приключилась со мной в последнее время :\n' \
                f'{history}'
    elif post != 'no' and idea == 'no':
        promt = 'Сгенерируй пост.\n\n' \
                'Вот такая структура должна быть у поста:\n' \
                f'{structure}\n' \
                'Также учти, что у меня есть свой продукт, вот его короткое описание:\n' \
                f'{product}\n\n' \
                'Моя личная история, которая приключилась со мной в последнее время :\n' \
                f'{history}\n\n' \
                'Также мои предыдущие посты :\n' \
                f'{post}'
    else:
        promt = 'Сгенерируй пост.\n\n' \
                'Вот такая структура должна быть у поста:\n' \
                f'{structure}\n' \
                'Также учти, что у меня есть свой продукт, вот его короткое описание:\n' \
                f'{product}\n\n' \
                'У меня есть идея для поста, вот ее короткое описание:\n' \
                f'{idea}\n\n' \
                'Моя личная история, которая приключилась со мной в последнее время :\n' \
                f'{history}\n\n' \
                'Также мои предыдущие посты :\n' \
                f'{post}' \

    await AsyncORM.add_gen_post(user_id, 'post body')
    await message.answer(
        text='Смотри какой пост у нас получился:\n\n'
             f'{promt}\n\n'
             'Оценку поста :)',
        reply_markup=kb.get_kb_rate()
    )
    await state.clear()


# хэндлер ловит невалидные сообщения идей постов
@router.message(StateFilter(FSMFillForm.upload_history))
async def process_no_idea(message: Message):
    print(f'{datetime.datetime.now()} - Ловим юзера {message.from_user.id} на невалидных данных HISTORY')
    await message.answer(
        text='Я очень внимательно слушаю вашу историю.\n\n'
             '____\n'
             '<i>Ты также можешь использовать голосовые сообщения для ответа :)</i>'
    )


# хэндлер кнопок оценки
@router.callback_query(F.data.in_(['1', '2', '3', '4', '5']))
async def process_idea_offer(callback: CallbackQuery):
    user_id = callback.from_user.id
    print(f'{datetime.datetime.now()} - [INFO] Юзер {user_id} нажал на кнопку оценки')
    rate = callback.data
    await AsyncORM.add_rate(user_id, rate)
    print(f'{datetime.datetime.now()} - [INFO] write rate {rate} to db')
    await callback.message.edit_text(
        text='Огонь, правда?\n\n'
             f'...\n\n'
    )
    await callback.answer()


# хэндлер ловящий если пользователь кикнул бота
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    await AsyncORM.add_flag_active(event.from_user.id, False)


# хэндлер ловящий если пользователь зашел в бота
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    await AsyncORM.add_flag_active(event.from_user.id, True)

# @router.callback_query(kb.PaymentCallbackFactory.filter(F.choice == "payment"))
# async def confirm(callback: CallbackQuery, callback_data: kb.PaymentCallbackFactory):
#     builder = InlineKeyboardBuilder()
#     builder.button(
#         text="Подтверждаю", callback_data=kb.PaymentCallbackFactory(choice="confirm",
#                                                                     value_gen=callback_data.value_gen,
#                                                                     value_price=callback_data.value_price)
#     )
#     builder.adjust(1)
#     await callback.message.edit_text(
#         text="Приобретая продукт, Вы соглашаетесь с тем, что разработчик не несет ответственности за результат "
#              "сгенерированной фотографии. Ответственность за фотогенерацию лежит исключительно "
#              "на искусственном интеллекте, и конечный результат зависит от его функциональных возможностей и процессов,"
#              " на которые разработчик не имеет влияния.",
#         reply_markup=builder.as_markup()
#     )
#
#
# @router.callback_query(kb.PaymentCallbackFactory.filter(F.choice == "confirm"))
# async def order(callback: CallbackQuery, callback_data: kb.PaymentCallbackFactory, bot: Bot):
#     print(f"Вывод информации для оплаты генераций")
#     await callback.message.edit_text("Отличный выбор!\n"
#                                      "Приобретайте генерации прямо сейчас.\n"
#                                      f"Цена: <b>{callback_data.value_price}₽ за {callback_data.value_gen} генераций!</b>\n"
#                                      )
#     await bot.send_invoice(
#         chat_id=callback.message.chat.id,
#         title='Телеграм бот для генерации фото',
#         description='Оплата дополнительных генераций',
#         payload='Оплата генераций через бота',
#         provider_token=config.payments_token.get_secret_value(),
#         currency='RUB',
#         prices=[
#             LabeledPrice(
#                 label='Оплатить генерации',
#                 amount=int(callback_data.value_price) * 100
#             ),
#         ],
#         start_parameter='oswyndel',
#         provider_data=None,
#         photo_url=None,
#         photo_size=None,
#         photo_width=None,
#         photo_height=None,
#         need_name=False,
#         need_phone_number=False,
#         need_email=False,
#         need_shipping_address=False,
#         protect_content=True,
#         request_timeout=5
#     )
#
#
# @router.pre_checkout_query()
# async def checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#
#
# @router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment(message: Message, state: FSMContext, bot: Bot):
#     print(f"Оплата прошла успешно")
#     print(f"Устанвливаем у юзера {message.from_user.id} флаг оплачено")
#     await AsyncORM.update_rate(message.chat.id, True)
#     if message.successful_payment.total_amount == 6900:
#         gens = 5
#     elif message.successful_payment.total_amount == 9900:
#         gens = 10
#     else:
#         gens = 15
#     print(f"Добавляем юзеру {message.from_user.id} +{gens} генераций")
#     await AsyncORM.add_gens(message.from_user.id, gens)
#     await message.answer("Спасибо за оплату! С Вашего счёта было списано "
#                          f"{message.successful_payment.total_amount // 100} {message.successful_payment.currency}.\n\n"
#                          f"Вам добавлено {gens} генераций")
#     user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=message.from_user.id)
#     print(user_channel_status.status)
#     if user_channel_status.status == ChatMemberStatus.LEFT:
#         await message.answer(
#             text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @haappymom\n\n"
#                  "После подписки нажмите /create_image"
#         )
#     else:
#         gens = await AsyncORM.get_gens(message.from_user.id)
#         print(f"Проверяем, что у юзера {message.from_user.id} есть хотя бы 1 генерация")
#         if gens > 0:
#             await message.answer(
#                 "Загрузите чёткое фото, на котором хорошо видно лицо"
#             )
#             await state.set_state(FSMFillForm.upload_photo)
#         else:
#             print(f"У юзера закончились {message.from_user.id} генерации")
#             await message.answer(text="У вас закончились бесплатные генерации.\n\nМожете приобрести их!",
#                                  reply_markup=kb.get_kb_fab_prices())

# @router.message(Command(commands='help'))
# async def process_help_command(message: Message, state: FSMContext, bot: Bot):
#     print(f"Юзер {message.from_user.id} нажал /help ")
#     await message.answer(
#         ""
#     )
#     print(f"Добавляем юзера {message.from_user.id} в бд")
#     await AsyncORM.add_user_id(message.from_user.id, message.from_user.username)
#     user_channel_status = await bot.get_chat_member(chat_id=-1001711057486, user_id=message.from_user.id)
#     print(user_channel_status.status)
#     if user_channel_status.status == ChatMemberStatus.LEFT:
#         await message.answer(
#             text="Чтобы ознакомиться с возможностями нашего бота, подпишись на канал @\n\n"
#                  "После подписки нажмите /create_image"
#         )
#     else:
#         gens = await AsyncORM.get_gens(message.from_user.id)
#         print(f"Проверяем, что у юзера {message.from_user.id} есть хотя бы 1 генерация")
#         if gens > 0:
#             await message.answer(
#                 "Загрузите чёткое фото, на котором хорошо видно лицо"
#             )
#             await state.set_state(FSMFillForm.upload_photo)
#         else:
#             print(f"У юзера закончились {message.from_user.id} генерации")
#             await message.answer(text="У вас закончились бесплатные генерации.\n\nМожете приобрести их!",
#                                  reply_markup=kb.get_kb_fab_prices())
