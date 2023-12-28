from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb = InlineKeyboardMarkup(row_width=5)

ib1 = InlineKeyboardButton(text="Добавить пользователя в вайтлист",
                           callback_data="add_whitelist")
ib2 = InlineKeyboardButton(text="Удалить пользователя из вайтлиста",
                           callback_data="del_whitelist")
ib3 = InlineKeyboardButton(text="Сделать пользователя админом",
                           callback_data="add_admin")
ib4 = InlineKeyboardButton(text="Отобрать права админа у пользователя",
                           callback_data="del_admin")
ib5 = InlineKeyboardButton(text="Закрыть",
                           callback_data="cancel_panel")

ikb.add(ib1).add(ib2).add(ib3).add(ib4).add(ib5)

ikbc = InlineKeyboardMarkup(row_width=1)

ibc = InlineKeyboardButton(text="Отменить действие",
                           callback_data="cancel")
ikbc.add(ibc)
