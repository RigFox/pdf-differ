# Установка
Для работы требует установить `poppler` (https://poppler.freedesktop.org)

MacOS: `brew install poppler`

Установить зависимости: `pip install -r requirements.txt`

# Использование
1. Закинуть сравниваемые PDF в папку `pdfs` с названиями `old.pdf`, `new.pdf`.
2. Запустить скрипт `python convert.py`
3. Смотреть различия в папке `result/diff`