import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8310822414:AAFjjFU7thWFEpCiUTcHhLk5jP7eXuW51hw"  # <-- вставь сюда реальный токен от BotFather

NBA_PLAYERS = {
    "LeBron James": "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png",
    "Stephen Curry": "https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png",
    "Kevin Durant": "https://cdn.nba.com/headshots/nba/latest/1040x760/201142.png",
    "Giannis Antetokounmpo": "https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png",
    "Nikola Jokić": "https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png",
    "Luka Dončić": "https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png",
    "Joel Embiid": "https://cdn.nba.com/headshots/nba/latest/1040x760/203954.png",
    "Jayson Tatum": "https://cdn.nba.com/headshots/nba/latest/1040x760/1628369.png",
    "Jimmy Butler": "https://cdn.nba.com/headshots/nba/latest/1040x760/202710.png",
    "Damian Lillard": "https://cdn.nba.com/headshots/nba/latest/1040x760/203081.png",
    "Devin Booker": "https://cdn.nba.com/headshots/nba/latest/1040x760/1626164.png",
    "Shai Gilgeous-Alexander": "https://cdn.nba.com/headshots/nba/latest/1040x760/1628983.png",
    "Anthony Davis": "https://cdn.nba.com/headshots/nba/latest/1040x760/203076.png",
    "Ja Morant": "https://cdn.nba.com/headshots/nba/latest/1040x760/1629630.png",
    "Kawhi Leonard": "https://cdn.nba.com/headshots/nba/latest/1040x760/202695.png",
    "Paul George": "https://cdn.nba.com/headshots/nba/latest/1040x760/202331.png",
    "Kyrie Irving": "https://cdn.nba.com/headshots/nba/latest/1040x760/202681.png",
    "James Harden": "https://cdn.nba.com/headshots/nba/latest/1040x760/201935.png",
    "Russell Westbrook": "https://cdn.nba.com/headshots/nba/latest/1040x760/201566.png",
    "Trae Young": "https://cdn.nba.com/headshots/nba/latest/1040x760/1629027.png",
    "Zion Williamson": "https://cdn.nba.com/headshots/nba/latest/1040x760/1629627.png",
    "Karl-Anthony Towns": "https://cdn.nba.com/headshots/nba/latest/1040x760/1626157.png",
    "Bradley Beal": "https://cdn.nba.com/headshots/nba/latest/1040x760/203078.png",
    "Donovan Mitchell": "https://cdn.nba.com/headshots/nba/latest/1040x760/1628378.png",
    "Jamal Murray": "https://cdn.nba.com/headshots/nba/latest/1040x760/1627750.png",
    "Jaylen Brown": "https://cdn.nba.com/headshots/nba/latest/1040x760/1627759.png",
    "Chris Paul": "https://cdn.nba.com/headshots/nba/latest/1040x760/101108.png",
    "Tyrese Haliburton": "https://cdn.nba.com/headshots/nba/latest/1040x760/1630169.png",
    "DeMar DeRozan": "https://cdn.nba.com/headshots/nba/latest/1040x760/201942.png",
    "LaMelo Ball": "https://cdn.nba.com/headshots/nba/latest/1040x760/1630163.png",
}

game_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎮 Создать игру", callback_data="create_game")]]
    await update.message.reply_text(
        "🏀 ШПИОН: NBA EDITION\n\nНажми кнопку ниже:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == "create_game":
        game_data[chat_id] = {"count": 0, "roles": [], "index": 0}
        keyboard = [
            [InlineKeyboardButton("➕ Добавить игрока", callback_data="add")],
            [InlineKeyboardButton("▶ Начать игру", callback_data="begin")]
        ]
        await query.edit_message_text(
            "Игроков: 0\n\nДобавьте игроков:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "add":
        game_data[chat_id]["count"] += 1
        count = game_data[chat_id]["count"]
        keyboard = [
            [InlineKeyboardButton("➕ Добавить игрока", callback_data="add")],
            [InlineKeyboardButton("▶ Начать игру", callback_data="begin")]
        ]
        await query.edit_message_text(
            f"Игроков: {count}\n\nДобавьте игроков:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "begin":
        count = game_data[chat_id]["count"]
        if count < 3:
            await query.answer("Минимум 3 игрока!", show_alert=True)
            return

        player_name = random.choice(list(NBA_PLAYERS.keys()))
        player_photo = NBA_PLAYERS[player_name]
        spy_index = random.randint(0, count - 1)

        roles = []
        for i in range(count):
            if i == spy_index:
                roles.append("SPY")
            else:
                roles.append({"name": player_name, "photo": player_photo})

        random.shuffle(roles)
        game_data[chat_id]["roles"] = roles
        game_data[chat_id]["index"] = 0

        keyboard = [[InlineKeyboardButton("👀 Посмотреть роль", callback_data="show")]]
        await query.edit_message_text(
            "Игра началась!\n\nИгрок 1, нажми кнопку:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "show":
        index = game_data[chat_id]["index"]
        roles = game_data[chat_id]["roles"]

        if index < len(roles):
            role = roles[index]
            keyboard = [[InlineKeyboardButton("➡ Передать дальше", callback_data="next")]]

            if role == "SPY":
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo="https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
                    caption="🚨 CLASSIFIED 🚨\n\n🕶 ТЫ ШПИОН\n\nВсе обсуждают одного NBA-игрока.\nПопробуй понять кого и не выдать себя.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=role["photo"],
                    caption=f"🏀 Игрок: {role['name']}",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

    elif query.data == "next":
        # Удаляем последнее сообщение с ролью, чтобы скрыть картинку
        try:
            await query.message.delete()
        except:
            pass  # если удаление не удалось, просто продолжаем

        # Переходим к следующему игроку
        game_data[chat_id]["index"] += 1
        index = game_data[chat_id]["index"]
        total = len(game_data[chat_id]["roles"])

        if index < total:
            keyboard = [[InlineKeyboardButton("👀 Посмотреть роль", callback_data="show")]]
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Игрок {index + 1}, нажми кнопку:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="🎉 Все роли розданы!\n\nНачинайте обсуждение!"
            )
            del game_data[chat_id]

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
