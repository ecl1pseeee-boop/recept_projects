## Описание Проекта
Веб-приложение для умного подбора рецептов на основе имеющихся у пользователя продуктов. Система интегрируется с API Spoonacular для получения данных о рецептах и предоставляет интеллектуальную систему подбора рецептов по ингредиентам.
## Стек Технологий
- **Backend**: Django (Python)
- **База данных**: MySQL
- **Frontend**: HTML, Tailwind CSS, HTMX, Alpine.js
- **Инфраструктура**: Docker, Nginx
- **Внешний API**: Spoonacular.com
## Основной Функционал

### 1. Каталог Рецептов
- Просмотр всех доступных рецептов
- Фильтрация рецептов по категориям (завтрак, обед, ужин, десерты, вегетарианское, веганское и т.д.)
- Функция поиска
- Пагинация
- Сортировка (по популярности, времени приготовления, сложности)
### 2. Детальная Страница Рецепта
- Полная информация о рецепте:
    - Название и изображение
    - Время приготовления и количество порций
    - Уровень сложности
    - Список ингредиентов с количеством
    - Пошаговая инструкция приготовления
    - Информация о питательной ценности
    - Теги/категории
- Добавление в избранное
- Функция "Поделиться"
### 3. Управление Избранным
- Сохранение рецептов в избранное
- Просмотр всех избранных рецептов
- Удаление из избранного
- Счетчик избранных рецептов
### 4. Создание Рецептов
- Форма создания пользовательского рецепта:
    - Название рецепта
    - Описание
    - Загрузка изображения
    - Ингредиенты с количеством
    - Инструкция по приготовлению
    - Время подготовки и приготовления
    - Количество порций
    - Выбор категории
    - Теги
- Возможность сохранения черновика
- Редактирование и удаление собственных рецептов
### 5. Умный Подбор по Ингредиентам
- Интерфейс ввода имеющихся продуктов
- Поиск ингредиентов с автодополнением
- Управление ингредиентами (добавление/удаление)
- Сохранение инвентаря ингредиентов
- Умные предложения рецептов на основе:
    - Полного совпадения (все ингредиенты есть)
    - Частичного совпадения (с указанием недостающих ингредиентов)
    - Отображение процента совпадения
- Фильтрация предложений по:
    - Максимальному количеству недостающих ингредиентов
    - Категориям рецептов
    - Времени приготовления
### 6. Аутентификация Пользователей
- Регистрация
- Вход/Выход
- Восстановление пароля
- Управление профилем
## Технические Требования

### Стандарты Качества Кода
- **Безопасность**:
    - CSRF защита
    - Предотвращение SQL-инъекций
    - XSS защита
    - Безопасное хранение паролей (хеширование)
    - Защита API ключей
    - Rate limiting для API вызовов
    - Валидация и санитизация входных данных
- **Принципы ООП**:
    - Class-based views где применимо
    - Наследование моделей
    - Инкапсуляция
    - Слои абстракции
    - Паттерн Service Layer
- **Принцип DRY**:
    - Переиспользуемые компоненты
    - Наследование шаблонов
    - Общие утилиты и хелперы
    - Отсутствие дублирования кода
- **Маппинг Данных**:
    - Сериализаторы для API ответов
    - Паттерн DTO (Data Transfer Objects)
    - Трансформация моделей БД во frontend данные
- **Best Practices**:
    - RESTful API дизайн
    - Корректная обработка ошибок
    - Логирование
    - Переменные окружения для конфигурации
    - Миграции базы данных
    - Правильная индексация
    - Оптимизация запросов
    - Стратегия кеширования
### Архитектура
#### Схема Базы Данных
**Users**
- id, email, username, password, created_at, updated_at
**Recipes**
- id, title, description, image, source (spoonacular/user), external_id, cooking_time, prep_time, servings, difficulty, instructions, created_at, updated_at, user_id
**Categories**
- id, name, slug
**Recipe_Categories** (Many-to-Many)
- recipe_id, category_id
**Ingredients**
- id, name, normalized_name
**Recipe_Ingredients**
- id, recipe_id, ingredient_id, quantity, unit
**User_Favorites**
- id, user_id, recipe_id, created_at
**User_Ingredients** (Холодильник)
- id, user_id, ingredient_id, quantity, unit, added_at
### Интеграция с API
- Endpoints Spoonacular API:
    - Поиск рецептов
    - Детали рецепта
    - Рецепты по ингредиентам
    - Поиск ингредиентов
    - Информация о питательной ценности
- Кеширование ответов API
- Обработка ошибок API
- Управление rate limit
### Frontend (SPA-подобный Опыт)
- **HTMX**:
    - Динамическая загрузка контента без перезагрузки страницы
    - Отправка форм через AJAX
    - Бесконечная прокрутка для списка рецептов
    - Поиск в реальном времени
    - Частичные обновления страницы
- **Alpine.js**:
    - Клиентская интерактивность
    - Выпадающие меню
    - Модальные окна
    - Валидация форм
    - Управление состоянием
- **Tailwind CSS**:
    - Адаптивный дизайн (mobile-first)
    - Консистентная стилизация
    - Поддержка темной темы (опционально)
    - Кастомные компоненты
### Инфраструктура
#### Конфигурация Docker
- **Сервисы**:
    - Контейнер Django приложения
    - Контейнер MySQL
    - Контейнер Nginx
    - Redis (для кеширования)
- **docker-compose.yml** с:
    - Маппингом volumes
    - Конфигурацией сети
    - Переменными окружения
    - Маппингом портов
#### Конфигурация Nginx
- Раздача статических файлов
- Раздача медиа файлов
- Reverse proxy к Django
- Gzip сжатие
- Security headers
- Готовность к SSL/TLS
### Конфигурация Окружения
- Development настройки
- Production настройки
- Переменные окружения:
    - Credentials базы данных
    - Secret key
    - Spoonacular API key
    - Debug режим
    - Allowed hosts
## Структура Проекта

```

smart-food-constructor/

│

├── docker/

│   ├── nginx/

│   │   ├── Dockerfile

│   │   └── nginx.conf

│   ├── django/

│   │   └── Dockerfile

│   └── mysql/

│       └── init.sql

│

├── config/

│   ├── __init__.py

│   ├── settings/

│   │   ├── __init__.py

│   │   ├── base.py

│   │   ├── development.py

│   │   └── production.py

│   ├── urls.py

│   ├── wsgi.py

│   └── asgi.py

│

├── apps/

│   ├── __init__.py

│   │

│   ├── users/

│   │   ├── __init__.py

│   │   ├── models.py

│   │   ├── views.py

│   │   ├── forms.py

│   │   ├── urls.py

│   │   ├── managers.py

│   │   ├── admin.py

│   │   └── tests.py

│   │

│   ├── recipes/

│   │   ├── __init__.py

│   │   ├── models.py

│   │   ├── views.py

│   │   ├── forms.py

│   │   ├── urls.py

│   │   ├── serializers.py

│   │   ├── services/

│   │   │   ├── __init__.py

│   │   │   ├── recipe_service.py

│   │   │   ├── spoonacular_service.py

│   │   │   └── ingredient_matcher.py

│   │   ├── utils/

│   │   │   ├── __init__.py

│   │   │   └── helpers.py

│   │   ├── admin.py

│   │   └── tests.py

│   │

│   ├── ingredients/

│   │   ├── __init__.py

│   │   ├── models.py

│   │   ├── views.py

│   │   ├── forms.py

│   │   ├── urls.py

│   │   ├── services/

│   │   │   ├── __init__.py

│   │   │   └── ingredient_service.py

│   │   ├── admin.py

│   │   └── tests.py

│   │

│   ├── categories/

│   │   ├── __init__.py

│   │   ├── models.py

│   │   ├── views.py

│   │   ├── urls.py

│   │   ├── admin.py

│   │

│   └── favorites/

│       ├── __init__.py

│       ├── models.py

│       ├── views.py

│       ├── urls.py

│       ├── admin.py

│       └── tests.py

│

├── templates/

│   ├── base.html

│   ├── partials/

│   │   ├── header.html

│   │   ├── footer.html

│   │   ├── navbar.html

│   │   └── pagination.html

│   │

│   ├── users/

│   │   ├── login.html

│   │   ├── register.html

│   │   ├── profile.html

│   │   └── password_reset.html

│   │

│   ├── recipes/

│   │   ├── recipe_list.html

│   │   ├── recipe_detail.html

│   │   ├── recipe_create.html

│   │   ├── recipe_edit.html

│   │   └── partials/

│   │       ├── recipe_card.html

│   │       └── recipe_filters.html

│   │

│   ├── ingredients/

│   │   ├── my_ingredients.html

│   │   ├── ingredient_search.html

│   │   └── partials/

│   │       └── ingredient_item.html

│   │

│   ├── favorites/

│   │   ├── favorites_list.html

│   │   └── partials/

│   │       └── favorite_card.html

│   │

│   └── matcher/

│       ├── matcher_page.html

│       └── partials/

│           └── matched_recipe.html

│

├── static/

│   ├── css/

│   │   ├── input.css

│   │   └── output.css

│   ├── js/

│   │   ├── main.js

│   │   └── alpine-components.js

│   └── images/

│       ├── logo.png

│       └── placeholder.jpg

│

├── media/

│   └── recipes/

│       └── user_uploads/

│

├── core/

│   ├── __init__.py

│   ├── mixins.py

│   ├── decorators.py

│   ├── middleware.py

│   └── exceptions.py

│

├── utils/

│   ├── __init__.py

│   ├── cache.py

│   ├── validators.py

│   └── constants.py

│

├── api/

│   ├── __init__.py

│   ├── urls.py

│   ├── views.py

│   └── serializers.py

│

├── logs/

│   └── .gitkeep

│

├── docker-compose.yml

├── docker-compose.prod.yml

├── Dockerfile

├── .dockerignore

├── .env.example

├── .gitignore

├── requirements.txt

├── requirements-dev.txt

├── manage.py

├── tailwind.config.js

├── package.json

└── README.md

```
## Описание Структуры

### Корневая Директория


- **docker/** - конфигурации Docker для всех сервисов

- **config/** - основные настройки Django проекта

- **apps/** - Django приложения (модульная структура)

- **templates/** - HTML шаблоны

- **static/** - статические файлы (CSS, JS, изображения)

- **media/** - пользовательские загрузки

- **core/** - общие утилиты и базовые классы

- **utils/** - вспомогательные функции

- **api/** - API endpoints (если нужен отдельный REST API)

- **logs/** - логи приложения
### Apps Структура

Каждое приложение следует стандартной Django структуре:

- **models.py** - модели базы данных

- **views.py** - представления (class-based и function-based)

- **forms.py** - формы Django

- **urls.py** - URL маршруты

- **serializers.py** - сериализаторы данных

- **services/** - бизнес-логика (Service Layer)

- **utils/** - вспомогательные функции приложения

- **admin.py** - конфигурация Django Admin

### Templates Структура

- **base.html** - базовый шаблон с общей структурой

- **partials/** - переиспользуемые компоненты (header, footer и т.д.)

- Директории для каждого приложения с соответствующими шаблонами

- **partials/** внутри каждого приложения для HTMX компонентов
### Static Структура
- **css/** - Tailwind CSS файлы (input и output)

- **js/** - JavaScript файлы (Alpine.js компоненты)

- **images/** - статические изображения
## Язык Интерфейса
- Весь UI текст на английском языке
- Комментарии в коде не требуются
## Результаты Разработки
1. Полная структура Django проекта

2. Файлы конфигурации Docker

3. Конфигурация Nginx

4. Файлы миграций базы данных

5. requirements.txt

6. README с инструкциями по установке

7. Шаблон переменных окружения (.env.example)
## Требования к Производительности

- Время загрузки страницы < 2 секунд

- Кеширование ответов API

- Оптимизация запросов к БД

- Ленивая загрузка изображений

- Эффективная пагинация
## Соображения по Масштабируемости

- Возможность перехода на микросервисную архитектуру

- Версионирование API

- Интеграция Elasticsearch для продвинутого поиска

- Поддержка API для мобильного приложения

- Инфраструктура для мультиязычности
## Дополнительные Требования
- Responsive дизайн для всех устройств

- Кроссбраузерная совместимость

- SEO оптимизация

- Accessibility стандарты (WCAG)

- Unit тесты для критичных компонентов

- Integration тесты для API endpoints