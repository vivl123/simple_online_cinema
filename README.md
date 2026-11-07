# Онлайн-кинотеатр

Нужен Python 3.10 или новее. Установка библиотек не требуется.

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

## Как заменить предыдущую версию

Скопируйте файлы из архива в свой проект. Сохраните свою папку .git.
Удалите четыре старых файла: errors.py, serializer.py, xml_storage.py,
viewing_stats.py — их код перенесён или заменён стандартными средствами.

## Что читать

1. main.py — запуск.
2. app.py — выбор команды через if/elif.
3. cinema.py — CRUD фильмов и пользователей.
4. cinema_actions.py и account_actions.py — действия меню.
5. storage.py — сохранение и загрузка JSON/XML.

В report.md описаны все 10 классов. UML находится в online_cinema.drawio.

## Отправка в GitHub

В терминале своей папки проекта:

```bash
git status
git add -A
git --no-pager diff --cached --stat
git commit -m "Simplify cinema to 10 classes"
git push origin main
```

Перед commit проверьте список изменений, чтобы не отправить лишние файлы.
