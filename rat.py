import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Ваш токен Telegram бота
TOKEN = "9162995471:AAG-vL1gW8n4sSrmZMA8HyXgVH1fDbAxxoo"
bot = telebot.TeleBot(TOKEN)

# Функция для создания или чтения файла оферты и политики безопасности
def load_political_text():
    file_path = "Political.txt"
    # Если файл не существует, создаем его с вашим текстом оферты автоматически
    if not os.path.exists(file_path):
        oferta_content = """ПУБЛИЧНАЯ ОФЕРТА
на оказание услуг по предоставлению доступа к сервису шифрования трафика
г.Москва улица Маршала Савицкого 28, 13.09.2026
Исполнитель: Шенгелия Георгий Евгеньевич, ИНН 771538058109

1. Термины и определения
1.1. Оферта — настоящее предложение Исполнителя заключить договор на оказание услуг на указанных в нём условиях.
1.2. Акцепт — полное и безоговорочное принятие условий Оферты путём оплаты Услуги в боте.
1.3. Пользователь — физическое лицо, акцептовавшее Оферту.
1.4. Услуга — предоставление доступа к инфраструктуре сервиса для шифрования сетевого трафика и обеспечения конфиденциальности передачи данных в сети Интернет.
1.6. Пробный период — период предоставления Услуги продолжительностью 3 (три) календарных дня по специальной цене 10 (десять) рублей.
1.7. Основной тариф — стоимость Услуги после окончания Пробного периода, указанная в боте в рублях.
1.8. Автопродление — автоматическое списание денежных средств за следующий период оказания Услуги, если Пользователь не отменил продление до окончания текущего периода.

2. Предмет договора
2.2. Пользователь обязуется оплатить Услугу в порядке и на условиях, предусмотренных настоящей Офертой.
2.3. Услуга предоставляется в виде доступа к учётной записи либо использования серверной инфраструктуры Исполнителя.

3. Порядок оказания услуги и оплата
3.1. Стоимость Услуги определяется в соответствии с действующими тарифами, размещёнными в боте и указывается в рублях.
3.2. Оплата производится с использованием платёжной системы ЮKassa.
3.3. При оформлении подписки Пользователь соглашается с условиями Пробного периода: 3 календарных дня за 10 рублей, после чего происходит автоматическое продление подписки по Основному тарифу.
3.4. Доступ к Услуге предоставляется автоматически в течение 10-30 минут после поступления денежных средств на счёт Исполнителя.
3.5. Данные для доступа (учётные данные/конфигурационный файл) направляются на адрес электронной почты, указанный при оформлении заказа, либо отображаются в Личном кабинете Пользователя.
3.6. Срок действия доступа определяется выбранным тарифом и начинает исчисляться с момента предоставления доступа. Для Пробного периода срок составляет 3 календарных дня.
3.7. Автопродление происходит за 24 часа до окончания текущего оплаченного периода, если Пользователь не отключил продление в Личном кабинете.
3.8. Списание средств при автопродлении производится с платёжной карты/счёта, использованного при первоначальной оплате.

4. Соблюдение законодательства РФ
4.1. Пользователь уведомлён, что использование Услуги не должно нарушать действующее законодательство Российской Федерации.
4.2. Исполнитель обязуется ограничивать доступ к информационным ресурсам, распространение которых запрещено на территории РФ, в соответствии с требованиями Федерального закона от 27.07.2006 № 149-ФЗ.
4.3. Доступ к таким ресурсам может быть ограничен Исполнителем в одностороннем порядке без предварительного уведомления Пользователя.

5. Права и обязанности сторон
5.1. Обязанности Исполнителя: обеспечивать работоспособность сервиса в рамках заявленных характеристик; защищать персональные данные Пользователя в соответствии с законодательством РФ; уведомлять Пользователей об изменении тарифов не менее чем за 3 календарных дня.
5.2. Обязанности Пользователя: не передавать данные доступа третьим лицам; не использовать сервис для противоправных действий (спам, взлом, DDoS-атаки и т. п.); соблюдать законодательство РФ.

6. Ответственность и форс-мажор
6.1. Исполнитель не несёт ответственности за перебои в работе Услуги, вызванные сбоями в работе сети Интернет, действиями третьих лиц или форс-мажорными обстоятельствами.

7. Персональные данные
7.1. Принимая условия Оферты, Пользователь даёт согласие на обработку своих персональных данных в соответствии с ФЗ № 152 «О персональных данных».

8. Изменение и расторжение договора
8.1. Исполнитель вправе вносить изменения в условия Оферты в одностороннем порядке. Новая редакция публикуется в канале.

9. Возврат денежных средств
9.1. Возврат средств производится при неоказании Услуги по вине Исполнителя или по заявлению Пользователя в течение первых 3 календарных дней при условии, что трафик не потреблялся.

10. Прочие условия
10.1. Споры подлежат урегулированию путём переговоров. Во всём остальном стороны руководствуются законодательством РФ.

Исполнитель: Шенгелия Георгий Евгеньевич, ИНН 771538058109"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(oferta_content)

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Главное меню с инлайн-кнопками (сетка квадратами)
def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("💳 Тарифы", callback_data="tariffs"),
        InlineKeyboardButton("💬 Чаты", url="https://mashagpt.ru/community")
    )
    keyboard.row(
        InlineKeyboardButton("ℹ️ О нас", callback_data="about"),
        InlineKeyboardButton("🔒 NDA", callback_data="privacy")
    )
    keyboard.row(
        InlineKeyboardButton("📜 Политика", callback_data="policy_txt"),
        InlineKeyboardButton("📄 Оферта ИП", callback_data="oferta")
    )
    return keyboard

# Меню выбора тарифов
def get_tariffs_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("⭐ Ultra (1 990 ₽)", callback_data="pay_ultra"),
        InlineKeyboardButton("💎 Pro (19 990 ₽)", callback_data="pay_pro")
    )
    keyboard.row(
        InlineKeyboardButton("⚡ Base (990 ₽)", callback_data="pay_base"),
        InlineKeyboardButton("🌱 Free (0 ₽)", callback_data="pay_free")
    )
    keyboard.row(InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu"))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤖 *ZentrAI Ecosystem*\n\n"
        "Добро пожаловать! Доступ к 50+ нейросетям.\n\n"
        "📜 *Соглашение о конфиденциальности и NDA:*\n"
        "Используя бота, вы подтверждаете согласие с политикой обработки данных, конфиденциальностью и неразглашением (NDA) информации.\n\n"
        "Выберите раздел на панели ниже:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        if call.data == "main_menu":
            bot.edit_message_text(
                "🤖 *Главное меню ZentrAI:*\n\nВыберите нужный раздел в панели ниже:",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=get_main_menu(),
                parse_mode="Markdown"
            )
        elif call.data == "tariffs":
            text = (
                "💳 *Тарифные планы ZentrAI:*\n\n"
                "• *Ultra (1 990 ₽/мес)* — 50 млн ед. энергии.\n"
                "• *Base (990 ₽/мес)* — 20 млн ед. энергии.\n"
                "• *Pro (19 990 ₽/мес)* — 700 млн ед. энергии для бизнеса.\n"
                "• *Free (0 ₽)* — 5 генераций в сутки."
            )
            bot.edit_message_text(
                text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=get_tariffs_menu(),
                parse_mode="Markdown"
            )
        elif call.data == "about":
            text = (
                "ℹ️ *О платформе ZentrAI*\n\n"
                "Платформа объединяет передовые языковые и графические нейросети без необходимости настройки VPN."
            )
            back_kb = InlineKeyboardMarkup()
            back_kb.row(InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu"))
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back_kb, parse_mode="Markdown")
        elif call.data == "privacy":
            text = (
                "🔒 *Политика конфиденциальности и NDA*\n\n"
                "1. Все ваши текстовые запросы защищены соглашением о неразглашении (NDA).\n"
                "2. Данные не передаются третьим сторонам."
            )
            back_kb = InlineKeyboardMarkup()
            back_kb.row(InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu"))
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back_kb, parse_Mode="Markdown")
        elif call.data == "policy_txt":
            # Загружаем полный текст из файла Political.txt
            full_text = load_political_text()
            back_kb = InlineKeyboardMarkup()
            back_kb.row(InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu"))
            
            bot.answer_callback_query(call.id, "Загружаю документ политики...")
            
            # Telegram ограничивает длину одного сообщения в 4096 символов, отправляем частями если нужно
            if len(full_text) > 4000:
                for i in range(0, len(full_text), 4000):
                    bot.send_message(call.message.chat.id, full_text[i:i+4000])
                bot.send_message(call.message.chat.id, "Вернуться в главное меню:", reply_markup=back_kb)
            else:
                bot.edit_message_text(
                    full_text,
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=back_kb,
                    parse_mode=None
                )
        elif call.data == "oferta":
            text = (
                "📄 *Публичная оферта и реквизиты ИП*\n\n"
                "<b>Продавец:</b> ИП ШЕНГЕЛИЯ ГЕОРГИЙ ЕВГЕНЬЕВИЧ\n"
                "<b>ИНН:</b> 771538058109\n"
                "<b>ОГРНИП:</b> 326774600827264\n"
                "<b>Email:</b> shengelia2311@gmail.com\n"
                "<b>Адрес:</b> Москва, улица Маршала Савицкого д. 28, кв. 195\n\n"
                "<b>Банковские реквизиты:</b>\n"
                "Банк: ПАО Сбербанк\n"
                "БИК: 044525225\n"
                "Р/с: 40802810538720122064\n"
                "К/с: 30101810400000000225"
            )
            back_kb = InlineKeyboardMarkup()
            back_kb.row(InlineKeyboardButton("⬅️ Главное меню", callback_data="main_menu"))
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=back_kb, parse_mode="HTML")
        elif call.data.startswith("pay_"):
            tariff = call.data.split("_")[1].upper()
            bot.answer_callback_query(call.id, f"Выбран тариф {tariff}")
            bot.send_message(
                call.message.chat.id,
                f"💳 Вы выбрали тариф *{tariff}*.\n\n"
                f"Оплата через ЮKassa и по реквизитам ИП Шенгелия Г.Е. Обратитесь в поддержку.",
                parse_mode="Markdown"
            )
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    print("Бот успешно запущен!")
    bot.infinity_polling()
