import os
import requests
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ---
bot_tickets = []
active_bots = []
templates = []

# Цены по умолчанию (обновляются с сайта)
bot_prices = {
    "trial": 10,
    "personal": 249,
    "premium": 349,
    "family": 699
}

# --- ТЕКСТЫ ---
WELCOME_TEXT = """👋 Добро пожаловать в <b>OfficialVPN</b>!

Мы предоставляем высокоскоростной и безопасный доступ к интернету без ограничений. Ваш трафик надежно зашифрован, а скорость не падает даже в часы пик.

🛡 <b>Соглашение о неразглашении (NDA) и Политика конфиденциальности:</b>
Используя наш сервис, вы соглашаетесь с тем, что мы не сохраняем логи вашей активности, историю посещений или переданные данные. Ваша конфиденциальность — наш главный приоритет. Мы обязуемся не передавать ваши данные третьим лицам и не раскрывать информацию о вашем подключении.

Выберите действие на клавиатуре ниже, чтобы продолжить:"""

TARIFFS_TEXT = """💎 <b>Наши тарифы:</b>

🔥 <b>Личный</b> — {personal}₽ / мес.
├ 2 устройства
└ 35 ГБ обхода

🚀 <b>Премиум</b> — {premium}₽ / мес.
├ 4 устройства
├ 75 ГБ обхода
└ Премиум-локации

👨‍👩‍👧‍👦 <b>Семейный</b> — {family}₽ / мес.
├ 8 устройств
├ 125 ГБ обхода
└ Премиум-локации"""

TRIAL_TEXT = """🔥 <b>Пробный период на 7 дней всего за {trial}₽!</b>

Оцените скорость и стабильность нашего сервиса без риска. Что входит в пробный доступ:
• 1 устройство
• Безлимитный трафик
• Доступ ко всем базовым локациям

⚠️ Пробный период доступен один раз на аккаунт. По истечении 7 дней подписка автоматически продлится по тарифу "Личный", если вы не отмените её заранее."""

PROFILE_TEXT = """👤 <b>Ваш профиль:</b>

• Статус подписки: <b>Не активна</b>
• Остаток дней: 0
• Текущий тариф: —"""


# --- API ДЛЯ СОХРАНЕНИЯ ЦЕН С САЙТА ---
@app.route('/api/update-tariff', methods=['POST', 'OPTIONS'])
def update_tariff():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    key = data.get('key')
    price = data.get('price')
    
    if key and price:
        bot_prices[key] = price
        print(f"[PRICE UPDATED] {key} -> {price}₽")
        return jsonify({"success": True})
    return jsonify({"success": False}), 400


# --- ФОНОВЫЙ ПРОЦЕСС БОТА ---
def poll_telegram_bot(bot_token):
    offset = 0
    print(f"[BOT] Запущен опрос для токена: {bot_token[:10]}...")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/getUpdates?offset={offset}&timeout=30"
            response = requests.get(url, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                for update in data.get('result', []):
                    offset = update['update_id'] + 1
                    
                    # --- ТЕКСТОВЫЕ СООБЩЕНИЯ ---
                    message = update.get('message')
                    if message:
                        chat_id = message['chat']['id']
                        user_id = message['from']['id']
                        username = message['from'].get('username', str(user_id))
                        text = message.get('text', '')
                        
                        send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

                        if text.startswith('/start'):
                            reply_keyboard = {
                                "keyboard": [
                                    [{"text": "📅 Продлить VPN"}, {"text": "👥 Добавить слот"}],
                                    [{"text": "🔑 Показать мои ключи VPN"}, {"text": "💬 Поддержка"}]
                                ],
                                "resize_keyboard": True,
                                "is_persistent": True
                            }
                            requests.post(send_url, json={
                                "chat_id": chat_id,
                                "text": WELCOME_TEXT,
                                "parse_mode": "HTML",
                                "reply_markup": reply_keyboard
                            })
                            continue

                        # Обработка Reply-кнопок
                        if text == "📅 Продлить VPN":
                            # Инлайн-кнопки выбора тарифа
                            inline_kb = {
                                "inline_keyboard": [
                                    [{"text": f"🔥 Пробный — {bot_prices['trial']}₽", "callback_data": "buy_trial"}],
                                    [{"text": f"Личный — {bot_prices['personal']}₽", "callback_data": "buy_personal"}],
                                    [{"text": f"Премиум — {bot_prices['premium']}₽", "callback_data": "buy_premium"}],
                                    [{"text": f"Семейный — {bot_prices['family']}₽", "callback_data": "buy_family"}]
                                ]
                            }
                            
                            formatted_tariffs = TARIFFS_TEXT.format(
                                personal=bot_prices['personal'],
                                premium=bot_prices['premium'],
                                family=bot_prices['family']
                            )
                            
                            requests.post(send_url, json={
                                "chat_id": chat_id, 
                                "text": formatted_tariffs, 
                                "parse_mode": "HTML",
                                "reply_markup": inline_kb
                            })
                        
                        elif text == "👥 Добавить слот":
                            requests.post(send_url, json={"chat_id": chat_id, "text": "👥 Вы можете добавить еще одно устройство к вашей подписке.\n\nСтоимость: +50₽/мес."})
                            
                        elif text == "🔑 Показать мои ключи VPN":
                            requests.post(send_url, json={"chat_id": chat_id, "text": "🔑 <b>Ваши ключи:</b>\n\n<i>У вас пока нет активных подписок.</i>", "parse_mode": "HTML"})
                            
                        elif text == "💬 Поддержка":
                            requests.post(send_url, json={"chat_id": chat_id, "text": "💬 Напишите ваш вопрос следующим сообщением, и мы скоро ответим."})

                        elif not text.startswith('/'):
                            # Логика заявок
                            if user_id not in [t['user_id'] for t in bot_tickets]:
                                bot_tickets.append({
                                    'id': len(bot_tickets) + 1,
                                    'token': bot_token,
                                    'user_id': user_id,
                                    'username': username,
                                    'text': text,
                                    'status': 'waiting',
                                    'date': time.strftime("%d.%m.%Y %H:%M")
                                })
                                requests.post(send_url, json={"chat_id": chat_id, "text": "✅ Сообщение передано в поддержку."})

                    # --- ОБРАБОТКА ИНЛАЙН-КНОПОК ---
                    callback = update.get('callback_query')
                    if callback:
                        callback_id = callback['id']
                        chat_id = callback['message']['chat']['id']
                        message_id = callback['message']['message_id']
                        data_cb = callback.get('data')
                        
                        # Убираем загрузку с кнопки
                        requests.post(f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery", json={"callback_query_id": callback_id})

                        # Обработка нажатия на тариф
                        if data_cb and data_cb.startswith("buy_"):
                            tariff_key = data_cb.replace("buy_", "")
                            price = bot_prices.get(tariff_key, 0)
                            
                            # Шаг 1: Показываем анимацию загрузки
                            requests.post(f"https://api.telegram.org/bot{bot_token}/editMessageText", json={
                                "chat_id": chat_id, "message_id": message_id,
                                "text": "⏳ <i>Генерация ссылки на оплату...</i>", "parse_mode": "HTML"
                            })
                            
                            time.sleep(1.5) # Пауза для анимации
                            
                            # Шаг 2: Выдаем результат
                            requests.post(f"https://api.telegram.org/bot{bot_token}/editMessageText", json={
                                "chat_id": chat_id, "message_id": message_id,
                                "text": f"✅ Тариф <b>{tariff_key.capitalize()}</b> выбран.\n\nК оплате: <b>{price}₽</b>.\n\n<i>(Здесь будет ссылка на оплату)</i>", 
                                "parse_mode": "HTML"
                            })
                            
        except Exception as e:
            print(f"[BOT ERROR] {e}")
        time.sleep(1)


# --- ОСТАЛЬНЫЕ API ---
@app.route('/api/deploy-bot', methods=['POST'])
def deploy_bot():
    data = request.json
    token = data.get('token')
    if token and token not in active_bots:
        active_bots.append(token)
        threading.Thread(target=poll_telegram_bot, args=(token,), daemon=True).start()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Бот уже запущен или токен неверный"})

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    token = request.args.get('token')
    status = request.args.get('status', 'all')
    filtered = [t for t in bot_tickets if t['token'] == token]
    if status != 'all':
        filtered = [t for t in filtered if t['status'] == status]
    return jsonify({"success": True, "tickets": filtered})

@app.route('/api/reply-ticket', methods=['POST'])
def reply_ticket():
    data = request.json
    token = data.get('token')
    ticket_id = data.get('ticket_id')
    text = data.get('text')
    
    for t in bot_tickets:
        if t['id'] == ticket_id:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={"chat_id": t['user_id'], "text": text})
            t['status'] = 'closed'
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "Тикет не найден"})

@app.route('/api/save-template', methods=['POST'])
def save_template():
    templates.append(request.json)
    return jsonify({"success": True})

@app.route('/api/update-bot-photo', methods=['POST', 'OPTIONS'])
def update_bot_photo():
    if request.method == 'OPTIONS':
        return '', 200

    bot_token = request.form.get('token')
    photo = request.files.get('photo')

    if not bot_token or not photo:
        return jsonify({"success": False, "message": "Нет токена или фото"}), 400

    temp_path = "temp_avatar.jpg"
    photo.save(temp_path)

    try:
        url = f"https://api.telegram.org/bot{bot_token}/setMyPhoto"
        with open(temp_path, 'rb') as f:
            files = {'photo': f}
            response = requests.post(url, files=files)
        result = response.json()
        return jsonify({"success": result.get('ok', False), "message": result.get('description', '')})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)