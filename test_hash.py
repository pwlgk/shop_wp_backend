# test_hash.py
import hashlib
import hmac
from urllib.parse import unquote, parse_qsl, urlencode # Добавили urlencode
import json

# --- Вставьте ТОТ ЖЕ initData, что и в логе фронтенда ---
init_data_str = "query_id=AAFCux9DAAAAAEK7H0P57f4m&user=%7B%22id%22%3A1126153026%2C%22first_name%22%3A%22Pavel%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22target_l8nk%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FYgdVPMJltrKxtSwQr-6OBQFgs1M8EgPsstnF7BqAkRM.svg%22%7D&auth_date=1743097135&signature=f-qSc2wJenRpi6KfPryYZzvoGRzfhB5B6zUgiKaW62ZxrmjzozJoxHHYiiB6HAhhJzoPA43-ZangUTIzMqJdBQ&hash=b1e90054ab1d633595f0bdb163cc64451bf1868f24a00ae06c62101e4cf7aa23"
# Используйте последнюю initData из ваших логов, если она другая
# init_data_str = "query_id=AAFCux9DAAAAAEK7H0Nk1szo&user=..." # и т.д. с хешем df6ec...

# --- Вставьте АКТУАЛЬНЫЙ токен бота ---
bot_token = "7678058490:AAHd4ZQQTW3xOQbei8QNI4KYrVpUlZbde8Q" # Убедитесь, что это ПОСЛЕДНИЙ токен

# --- Код парсинга (оставляем как есть) ---
def parse_init_data(init_data: str) -> dict:
    parsed_data = {}
    for key, value in parse_qsl(init_data):
        decoded_value = unquote(value)
        # Не парсим JSON здесь, оставим как URL-кодированную строку, как в оригинале
        # if key in ('user', 'receiver', 'chat') and decoded_value.startswith('{') and decoded_value.endswith('}'):
        #     try:
        #         parsed_data[key] = json.loads(decoded_value)
        #     except json.JSONDecodeError:
        #          parsed_data[key] = decoded_value
        # else:
        parsed_data[key] = value # <<< ИЗМЕНЕНИЕ: Сохраняем ОРИГИНАЛЬНОЕ значение (до unquote)
    return parsed_data

# --- Код валидации (минимальный, только хеш) ---
try:
    # Парсим ОРИГИНАЛЬНУЮ строку, чтобы получить ВСЕ пары ключ=значение как они есть
    # Используем parse_qsl, чтобы сохранить порядок и необработанные значения
    original_pairs = parse_qsl(init_data_str, keep_blank_values=True)

    # Находим и удаляем пару с ключом 'hash'
    received_hash = None
    data_pairs_for_check = []
    for key, value in original_pairs:
        if key == 'hash':
            received_hash = value
        else:
            data_pairs_for_check.append((key, value))

    if received_hash is None:
         raise ValueError("Hash not found in initData")

    print(f"Data Pairs (for check string): {data_pairs_for_check}")
    print(f"Received Hash: {received_hash}")

    # Сортируем пары по ключу
    sorted_pairs = sorted(data_pairs_for_check, key=lambda item: item[0])

    # Формируем строку для проверки, используя оригинальные (возможно, URL-кодированные) значения
    data_check_string_parts = [f"{key}={value}" for key, value in sorted_pairs]
    data_check_string = "\n".join(data_check_string_parts)
    print(f"\nData Check String:\n{data_check_string}\n")

    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    print(f"Calculated Hash: {calculated_hash}")
    print(f"Match: {calculated_hash == received_hash}")

except Exception as e:
    print(f"Error: {e}")
