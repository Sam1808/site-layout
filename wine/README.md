# Новое русское вино

Сайт магазина авторского вина "Новое русское вино".

### Установка

Для использования вам необходимо:
- [python3](www.python.org)
- pip3 (для установки зависимостей из файла requirements.txt)
- интернет браузер (который есть уже везде)

Рекомендуется использовать [виртуальное окружение](https://pythoner.name/documentation/tutorial/venv)
python для разворачивания проекта.

#### Рекомендации при разворацивании в среде Linux

1. Скопируйте проект в локальную папку, например с помощью git:

`git clone https://github.com/Sam1808/site-layout.git`

2. Создайте виртуальное окружение:

`python3 -m venv <название_окружения>`

3. Активируйте виртуальное окружение:

`source <название_окружения>/bin/activate`

4. Опционально - обновите установщик пакетов pip

`pip install --upgrade pip`

После того, как все шаги выполнены, пожалуйста перейдите непосредственно в папку **wine** запустите pip3 для установки зависимостей:

`pip install -r requirements.txt`

##### Как запустить?

Контент сайта храниться в текстовом файле.
Создайте любой текстовый файл (example.txt), со следующим содержимым (пример):

```
# Белые вина


Название: Белая леди
Сорт: Дамский пальчик
Цена: 399
Картинка: images/belaya_ledi.png
Выгодное предложение

Название: Ркацители
Сорт: Ркацители
Цена: 499
Картинка: images/rkaciteli.png

Название: Кокур
Сорт: Кокур
Цена: 450
Картинка: images/kokur.png


# Красные вина


Название: Черный лекарь
Сорт: Качич
Цена: 399
Картинка: images/chernyi_lekar.png

Название: Хванчкара
Сорт: Александраули
Цена: 550
Картинка: images/hvanchkara.png

Название: Киндзмараули
Сорт: Саперави
Цена: 550
Картинка: images/kindzmarauli.png


# Напитки


Название: Чача
Сорт:
Цена: 299
Картинка: images/chacha.png
Выгодное предложение

Название: Коньяк классический
Сорт:
Цена: 350
Картинка: images/konyak_klassicheskyi.png

Название: Коньяк кизиловый
Сорт:
Цена: 350
Картинка: images/konyak_kizilovyi.png

```

#### Важно!

*Вы можете наполнять файл данными, добавлять или удалять позиции,
однако важно соблюдать порядок описания позиции, использование символа ' # ' , а также ' : '.
 Используемая кодировка UTF-8.*


После создания текстового файла, в активном виртуальном окружении запустите:

`python3 main.py <ваш_текстовый_файл>`

Где:
- python3 - файл запуска python
- main.py - скрипт запуска
- <ваш_текстовый_файл> - текстовый файл с описанием контента (обязательный параметр).

Примеры:

`python3 main.py example.txt`

Вы можете указать абсолютный или относительный путь до файла, например это будет выглядеть так:

`python main.py ./myfolder/myfile.txt `

Если вы ошиблись в имени файла или в пути до него, система сообщит об этом и выполнение скрипта будет прервано.

После успешного запуска, тестовый сайт будет доступен локально по [ссылке](http://127.0.0.0:8000/)


##### Описание:

Скрипт запускает локальный учебный web-сервер, который должен соотвествовать заданию преподавателя.  
