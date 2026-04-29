from flask import Flask, render_template, request, jsonify, session
import re
import json
import os

app = Flask(__name__)
app.secret_key = 'секретный_ключ_12345'


# ==================== ЧАСТЬ 1: ВАЛИДАЦИЯ ====================

def validate_email(email):
    """Задание 1.1: Проверка email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email.strip()):
        return True, "✅ Email корректный"
    return False, "❌ Неправильный email! Пример: name@mail.ru"


def validate_phone(phone):
    """Задание 1.2: Проверка телефона"""
    phone = phone.strip()
    patterns = [
        r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$',
        r'^\+7 \d{3} \d{3} \d{2} \d{2}$',
        r'^\+7\d{10}$',
        r'^8-\d{3}-\d{3}-\d{4}$',
        r'^8 \d{3} \d{3} \d{4}$',
        r'^8\d{10}$'
    ]
    for pattern in patterns:
        if re.match(pattern, phone):
            clean = re.sub(r'\D', '', phone)
            if clean.startswith('8'):
                clean = '+7' + clean[1:]
            elif clean.startswith('7'):
                clean = '+' + clean
            return True, "✅ Телефон корректный", clean
    return False, "❌ Неправильный телефон! Пример: +7-999-123-45-67", None


def validate_inn(inn):
    """Задание 1.3: Проверка ИНН"""
    inn = inn.strip()
    if not inn.isdigit():
        return False, "❌ ИНН должен содержать только цифры!"
    if len(inn) == 10:
        return True, "✅ ИНН организации корректен (10 цифр)"
    elif len(inn) == 12:
        return True, "✅ ИНН физического лица корректен (12 цифр)"
    return False, "❌ ИНН должен содержать 10 или 12 цифр!"


def validate_passport(passport):
    """Дополнительное задание 1: Проверка паспорта (45 03 123456)"""
    pattern = r'^\d{2} \d{2} \d{6}$'
    if re.match(pattern, passport.strip()):
        return True, "✅ Паспорт корректен (формат: 45 03 123456)"
    return False, "❌ Неправильный паспорт! Формат: 45 03 123456"


def validate_password(password, is_admin=False):
    """Проверка пароля"""
    min_len = 8 if is_admin else 6
    if len(password) < min_len:
        return False, f"❌ Пароль должен быть не менее {min_len} символов"
    return True, "✅ Пароль корректный"


# ==================== ЧАСТЬ 2: ПОИСК В ТЕКСТЕ ====================

def find_emails(text):
    """Задание 2.1: Поиск email в тексте"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


def find_phones(text):
    """Задание 2.2: Поиск телефонов в тексте"""
    pattern = r'\+7[- ]?\d{3}[- ]?\d{3}[- ]?\d{2}[- ]?\d{2}|8[- ]?\d{3}[- ]?\d{3}[- ]?\d{4}'
    return re.findall(pattern, text)


def find_dates(text):
    """Задание 2.3: Поиск дат в тексте (ДД.ММ.ГГГГ или ДД/ММ/ГГГГ)"""
    pattern = r'\d{2}[./]\d{2}[./]\d{4}'
    return re.findall(pattern, text)


def find_prices(text):
    """Задание 2.4: Поиск цен в тексте"""
    pattern = r'\d+(?:[.,]\d+)?\s?(?:руб|₽|\$|€)'
    return re.findall(pattern, text)


def find_urls(text):
    """Задание 2.5: Поиск ссылок в тексте"""
    pattern = r'https?://[a-zA-Z0-9./?=_-]+|www\.[a-zA-Z0-9./?=_-]+'
    return re.findall(pattern, text)


def find_hashtags(text):
    """Дополнительное задание 3: Поиск хэштегов"""
    pattern = r'#[a-zA-Zа-яА-Я0-9_]+'
    return re.findall(pattern, text)


def find_ips(text):
    """Дополнительное задание 2: Поиск IP-адресов"""
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.findall(pattern, text)


# ==================== МАРШРУТЫ (СТРАНИЦЫ) ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register-user')
def register_user():
    return render_template('register-user.html')


@app.route('/register-admin')
def register_admin():
    return render_template('register-admin.html')


@app.route('/user-main')
def user_main():
    return render_template('user-main.html')


@app.route('/status')
def status():
    return render_template('status.html')


@app.route('/admin-requests')
def admin_requests():
    return render_template('admin-requests.html')


@app.route('/success')
def success():
    return render_template('success.html')


# ==================== API ДЛЯ ВАЛИДАЦИИ (ЛР 13) ====================

@app.route('/api/validate-email', methods=['POST'])
def api_validate_email():
    data = request.get_json()
    valid, message = validate_email(data.get('email', ''))
    return jsonify({'valid': valid, 'message': message})


@app.route('/api/validate-phone', methods=['POST'])
def api_validate_phone():
    data = request.get_json()
    valid, message, clean = validate_phone(data.get('phone', ''))
    return jsonify({'valid': valid, 'message': message, 'clean': clean})


@app.route('/api/validate-inn', methods=['POST'])
def api_validate_inn():
    data = request.get_json()
    valid, message = validate_inn(data.get('inn', ''))
    return jsonify({'valid': valid, 'message': message})


@app.route('/api/validate-passport', methods=['POST'])
def api_validate_passport():
    data = request.get_json()
    valid, message = validate_passport(data.get('passport', ''))
    return jsonify({'valid': valid, 'message': message})


@app.route('/api/validate-password', methods=['POST'])
def api_validate_password():
    data = request.get_json()
    valid, message = validate_password(data.get('password', ''), data.get('is_admin', False))
    return jsonify({'valid': valid, 'message': message})


# ==================== API ДЛЯ ПОИСКА В ТЕКСТЕ (ЛР 13) ====================

@app.route('/api/search-text', methods=['POST'])
def api_search_text():
    """Объединяет все функции поиска"""
    data = request.get_json()
    text = data.get('text', '')
    return jsonify({
        'emails': find_emails(text),
        'phones': find_phones(text),
        'dates': find_dates(text),
        'prices': find_prices(text),
        'urls': find_urls(text),
        'hashtags': find_hashtags(text),
        'ips': find_ips(text)
    })


# ==================== API ДЛЯ РЕГИСТРАЦИИ ====================

@app.route('/api/register-user', methods=['POST'])
def api_register_user():
    data = request.get_json()
    valid_email, email_msg = validate_email(data.get('email', ''))
    valid_pass, pass_msg = validate_password(data.get('password', ''), False)

    # Проверка телефона (если заполнен)
    phone_valid = True
    phone_msg = ""
    if data.get('phone'):
        phone_valid, phone_msg, _ = validate_phone(data.get('phone'))

    # Проверка ИНН (если заполнен)
    inn_valid = True
    inn_msg = ""
    if data.get('inn'):
        inn_valid, inn_msg = validate_inn(data.get('inn'))

    if not data.get('name', '').strip():
        return jsonify({'success': False, 'message': '❌ Введите имя!'})
    if not valid_email:
        return jsonify({'success': False, 'message': email_msg})
    if not valid_pass:
        return jsonify({'success': False, 'message': pass_msg})
    if not phone_valid:
        return jsonify({'success': False, 'message': phone_msg})
    if not inn_valid:
        return jsonify({'success': False, 'message': inn_msg})

    session['user_name'] = data.get('name')
    session['user_phone'] = data.get('phone')
    return jsonify({'success': True, 'message': 'Регистрация успешна!'})


@app.route('/api/register-admin', methods=['POST'])
def api_register_admin():
    data = request.get_json()
    valid_email, email_msg = validate_email(data.get('email', ''))
    valid_pass, pass_msg = validate_password(data.get('password', ''), True)

    if not data.get('name', '').strip():
        return jsonify({'success': False, 'message': '❌ Введите имя!'})
    if not valid_email:
        return jsonify({'success': False, 'message': email_msg})
    if not valid_pass:
        return jsonify({'success': False, 'message': pass_msg})
    if data.get('code') != 'ADMIN123':
        return jsonify({'success': False, 'message': '❌ Неверный код доступа!'})

    session['admin_name'] = data.get('name')
    session['is_admin'] = True
    return jsonify({'success': True, 'message': 'Регистрация администратора успешна!'})


@app.route('/api/create-booking', methods=['POST'])
def api_create_booking():
    data = request.get_json()
    return jsonify({'success': True, 'message': 'Заявка отправлена!'})


@app.route('/api/get-user-requests', methods=['GET'])
def api_get_user_requests():
    return jsonify([])


@app.route('/api/get-all-requests', methods=['GET'])
def api_get_all_requests():
    return jsonify([])


@app.route('/api/update-status', methods=['POST'])
def api_update_status():
    return jsonify({'success': True})
@app.route('/search')
def search():
    return render_template('search.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)