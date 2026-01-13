import requests

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://gisp.gov.ru/goods/",               # ← очень важно!
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # "Origin": "https://gisp.gov.ru",                     # можно попробовать добавить
}

# Если хотите максимально повторить ваш браузер → добавьте cookies
cookies = {
    "PHPSESSID": "HFq3ulkty7VcuNXlS6pEz2Zq0VhBPl68",     # ← ваша сессия
    # остальные куки можно тоже передать, но PHPSESSID часто самый важный
}

url = "https://gisp.gov.ru/mapm/api/product-detail/3725836"

response = requests.get(url, headers=headers, cookies=cookies, timeout=15)

print("Статус:", response.status_code)
print("Заголовки ответа:", response.headers)

if response.status_code == 200:
    print(response.json())
else:
    print(response.text[:500])   # первые символы ошибки