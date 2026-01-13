import requests
import json

url = "https://gisp.gov.ru/mapm/api/product-list"

# Payload (тело запроса)
payload = {
    "page": 1,
    "per_page": 1,
    "use_ai_search": True,
    "order": [
        {"field": "name", "direction": "asc"}
    ],
    "filters": {
        "status_code": "product"
    },
    "type": "[Product] Query"
}

# Headers (важные для XHR)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://gisp.gov.ru",
    "Referer": "https://gisp.gov.ru/goods/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Requested-With": "XMLHttpRequest",
    "X-Ajax-Token": "8887ad9c0cd09d86d04232551def7493a29e4216a96d783d6ebe87e54f6ba5c4",
    "X-CSRFToken": "1889f479797dfffa20dec08607193d88f6c65b6bfa505c15d570cd5321ead48fceff7817001fa3a2"
}

# Cookies (как в браузере)
cookies = {
    "_ym_uid": "175829964771016105",
    "_ym_d": "1758299647",
    "_ym_isad": "1",
    "nan-session": "1889b88e8a0fcf8b099f8702beb261f560b2b2aeb97263c7601419296af9d83829fbc1a5101d73b69b7cd1b6d3b9000f",
    "PHPSESSID": "HFq3ulkty7VcuNXlS6pEz2Zq0VhBPl68",
    "BITRIX_SM_GUEST_ID": "112976554",
    "BITRIX_SM_LAST_VISIT": "11.01.2026 22:23:58",
    "_pk_ses.1.8b63": "1",
    "_pk_id.1.8b63": "a16c4868c2c45f38.1764706263.7.1768213135.1768159440"
}

# Отправка запроса
response = requests.post(
    url,
    headers=headers,
    cookies=cookies,
    data=json.dumps(payload),
    timeout=15
)

# Проверка результата
response.raise_for_status()

# JSON-ответ
data = response.json()

print("Статус:", response.status_code)
print("Получено записей:", len(data.get("data", [])))
print(json.dumps(data, indent=2, ensure_ascii=False))
