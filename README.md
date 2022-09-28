<h1 align="center">Ху Тао - VK Бот с симулятором гачи</h1>

<p align="center">Ху Тао - это <strong>самый лучший</strong> персонаж из одной популярной аниме-игры, а также бот VK с симулятором гачи/молитв оттуда же</p>
<p align="center"><img alt="Молитва 10 раз" src="pictures/ten_wish_picture.png" /></p>

## Реализованные функции
- Полная синхронизация всех предметов из реальной игры, используя её ресурсы
- Очень похожая гача система на гачу систему из игры
- Информация о профиле человеке из игры (используя API [enka.network](https://enka.network/))
- Поручения
- Ежеденевные награды
- Другие развлекательные команды (будет больше в будущем)
- Команды для администраторов

## Команды
### Начало
`!начать` - создание аккаунта в боте

`!помощь` - ссылка на этот лист

### Информация
`!персонаж`, `!перс` - показ профиля, количества молитв, примогемов, гаранта и UID

`!баланс` - показ количества молитв и примогемов

`!ник <ник>` - установка никнейма в вашем профиле

`!персонажи`, `!персы` - список полученных персонажей

`!инвентарь`, `!инв` - список полученных оружий

`!персонаж <имя>`, `!перс <имя>` - более подробная информация о вашем полученном персонаже

`!айди <UID>` - установка вашего UID из аниме-игры, что бы о вашем профиле из реальной игры можно было посмотреть информацию

`!геншин инфо`, `!геншин инфо <UID>` - показывает информацию из аниме-игры, используя либо ваш UID, который вы установили раннее, либо другой, если вы его указали в команде

Пример: `!геншин инфо 738723523`

### Баннеры
`!баннеры` - показывает список всех текущих баннеров

`!баннер <название>` - показывает более подробную информацию о выбранном баннере

Пример: `!баннер ивент`, `!баннер ивент 2`, `!баннер оруж`

На данный момент всего есть 5 названий: новичка, ивент, ивент 2, оружейный, стандарт

`!выбрать баннер <название>` - выбирает баннер, на который вы будете молиться

Пример: `!выбрать баннер ивент 2`

`!история` - показывает историю о вашем текущем выбранном баннере (выбрать баннер можно командой выше)

### Молитвы
`!помолиться` - создание молитвы на ваш раннее выбранный баннер (если вы не выбирали баннер, по умолчанию будет баннер новичка)

`!помолиться 10` - то же самое, только 10 раз

`!купить молитвы ивент/стандарт <кол-во>` - покупает указанные молитвы за ваши примогемы, если их хватает

Пример: `!купить молитвы ивент 10`

### Способы заработать примогемы
`!награда` - ежедневная награда, можно получить примогемы, а можно вообще ничего не получить...

`!начать поручения` и `!закончить поручения` - начинает или заканчивает ваше поручения, время поручения зависит от вашего ранга приключений в боте

#### Промокоды
`!мой промокод` - вы получите промокод, которым вы можете поделиться с друзьями

`!промокод <промокод>` - если у вас есть промокод, вы можете его ввести сюда, если это промокод человека - человек получит 4800 примогемов, а тот, кто его ввел получит 800 примогемов

### Другое
`!рандомная фраза`, `!<кол-во> рандомных фраз` - берет случайную строчку из текстмапа игры, {NICKNAME} заменяется на Timius100, HTML теги убираются

`!удалить геншин` - самая худшая вещь, которую вы можете только сделать

## Запуск
**Примечание: если вы обычный пользователь, это, скорее всего, не для вас. В этого бота можно поиграть в этой [группе](https://vk.com/we_love_hu_tao)**

Для запуска бота **необходимо** использовать Python версии **3.10 и выше**. Ниже этой версии не сработает, потому что в боте используется match/case, который был добавлен в 3.10

Необходимые модули и библиотеки можно скачать через файл requirements.txt, `pip install -r requirements.txt`

В variables.py необходимо указать 5 переменных - `VK_GROUP_TOKEN`, `GROUP_ID`, тестовый `VK_GROUP_TOKEN`, тестовый `GROUP_ID`, а также `VK_USER_TOKEN`.

В `VK_GROUP_TOKEN` должен быть указан токен группы, в тестовый токен должен быть указан токен второй группы, он будет использоваться, если `TEST_MODE` == True

В `VK_GROUP_ID` должен быть указан айди группы, с тестовым айди все то же самое, что и с токеном

В `VK_USER_TOKEN` должен быть указан токен пользователя, у которого есть права на удаление участников из группы, а также права на чтение записи

Далее необходима база данных PostgreSQL с названием hutao_bot.
База данных должна быть создана пользователем postgres, пароль базы данных надо указать вместо `password` в pgpass.conf

В этой базе данных должно быть 3 таблицы - players, banned и promocodes.

В будущем планируется автоматическое создание таблиц, но сейчас их надо создавать вручную.

Значения таблицы players есть в create_pool

В таблице banned должна быть одна колонка - user_id, тип integer

В таблице promocodes 5 колонок:
- promocode, тип text
- author, тип integer, дефолт 0
- expire_time, тип integer, дефолт 0
- promocode_reward, тип integer, дефолт 800
- redeemed_by, тип integer[], дефолт '{}'::integer[]

После всего этого можно запустить файл main.py - бот запустится