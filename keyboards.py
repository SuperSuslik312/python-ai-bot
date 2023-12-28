from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ib_cancel = InlineKeyboardButton(text="Закрыть",
                                 callback_data="cancel_panel")

ikb_admin = InlineKeyboardMarkup(row_width=5)
ib_admin1 = InlineKeyboardButton(text="Добавить пользователя в вайтлист",
                                 callback_data="add_whitelist")
ib_admin2 = InlineKeyboardButton(text="Удалить пользователя из вайтлиста",
                                 callback_data="del_whitelist")
ib_admin3 = InlineKeyboardButton(text="Сделать пользователя админом",
                                 callback_data="add_admin")
ib_admin4 = InlineKeyboardButton(text="Отобрать права админа у пользователя",
                                 callback_data="del_admin")
ikb_admin.add(ib_admin1).add(ib_admin2).add(ib_admin3).add(ib_admin4).add(ib_cancel)

ikb_cancel_admin = InlineKeyboardMarkup(row_width=1)
ib_cancel_admin = InlineKeyboardButton(text="Отмена",
                                       callback_data="cancel_admin")
ikb_cancel_admin.add(ib_cancel_admin)

ikb_cancel_user = InlineKeyboardMarkup(row_width=1)
ib_cancel_user = InlineKeyboardButton(text="Назад",
                                      callback_data="cancel_user")
ikb_cancel_user.add(ib_cancel_user)

ikb_user = InlineKeyboardMarkup(row_width=3)
ib_user1 = InlineKeyboardButton(text="Стереть мне память(",
                                callback_data="clear")
ib_user2 = InlineKeyboardButton(text="Задать моё поведение",
                                callback_data="set_prompt")
ib_user3 = InlineKeyboardButton(text="Сбросить моё поведение до заводского",
                                callback_data='reset_prompt')
ikb_user.add(ib_user1).add(ib_user2).add(ib_user3).add(ib_cancel)
