# Style guide

[Вдохновился по большей части от сюда](https://github.com/HackSoftware/Django-Styleguide)

<!-- MarkdownTOC autolink="true" -->

- [Введение](#%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5)
- [FAQ?](#faq)
- [Модели](#%D0%9C%D0%BE%D0%B4%D0%B5%D0%BB%D0%B8)
  - [Базовая модель](#%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C)
  - [Валидация](#%D0%92%D0%B0%D0%BB%D0%B8%D0%B4%D0%B0%D1%86%D0%B8%D1%8F)
  - [Валидация - constraints](#%D0%92%D0%B0%D0%BB%D0%B8%D0%B4%D0%B0%D1%86%D0%B8%D1%8F---constraints)
  - [Свойства](#%D0%A1%D0%B2%D0%BE%D0%B9%D1%81%D1%82%D0%B2%D0%B0)
  - [Методы](#%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D1%8B)
- [Сервисы](#%D0%A1%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B)
  - [Соглашение об именовании](#%D0%A1%D0%BE%D0%B3%D0%BB%D0%B0%D1%88%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D0%B1-%D0%B8%D0%BC%D0%B5%D0%BD%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B8)
  - [Расширение логики сервисов](#%D0%A0%D0%B0%D1%81%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BB%D0%BE%D0%B3%D0%B8%D0%BA%D0%B8-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BE%D0%B2)
  - [Селекторы](#%D0%A1%D0%B5%D0%BB%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D1%8B)
  - [Тестирование](#%D0%A2%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)
- [APIs & Serializers](#apis--serializers)
- [Serializers](#serializers)
  - [Соглашение об именовании](#%D0%A1%D0%BE%D0%B3%D0%BB%D0%B0%D1%88%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D0%B1-%D0%B8%D0%BC%D0%B5%D0%BD%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B8-1)
  - [Фильтры](#%D0%A4%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D1%8B)
- [Ошибки и обработка исключений](#%D0%9E%D1%88%D0%B8%D0%B1%D0%BA%D0%B8-%D0%B8-%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0-%D0%B8%D1%81%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B9)
  - [Как работает обработка исключений \(в контексте DRF\)](#%D0%9A%D0%B0%D0%BA-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82-%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0-%D0%B8%D1%81%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D0%B9-%D0%B2-%D0%BA%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%B5-drf)
    - [DRF's `ValidationError`.](#drfs-validationerror)
    - [Django's `ValidationError`.](#djangos-validationerror)
  - [Как должны выглядеть идеальные ошибки в нашем проекте \(пока не внедрять, на согласовании фронтами\)](#%D0%9A%D0%B0%D0%BA-%D0%B4%D0%BE%D0%BB%D0%B6%D0%BD%D1%8B-%D0%B2%D1%8B%D0%B3%D0%BB%D1%8F%D0%B4%D0%B5%D1%82%D1%8C-%D0%B8%D0%B4%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D0%B8-%D0%B2-%D0%BD%D0%B0%D1%88%D0%B5%D0%BC-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B5-%D0%BF%D0%BE%D0%BA%D0%B0-%D0%BD%D0%B5-%D0%B2%D0%BD%D0%B5%D0%B4%D1%80%D1%8F%D1%82%D1%8C-%D0%BD%D0%B0-%D1%81%D0%BE%D0%B3%D0%BB%D0%B0%D1%81%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B8-%D1%84%D1%80%D0%BE%D0%BD%D1%82%D0%B0%D0%BC%D0%B8)
- [Тестирование](#%D0%A2%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-1)
  - [Соглашения об именовании](#%D0%A1%D0%BE%D0%B3%D0%BB%D0%B0%D1%88%D0%B5%D0%BD%D0%B8%D1%8F-%D0%BE%D0%B1-%D0%B8%D0%BC%D0%B5%D0%BD%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B8)
- [Celery](#celery)
  - [Структура](#%D0%A1%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0)
    - [Конфигурация](#%D0%9A%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%D1%83%D1%80%D0%B0%D1%86%D0%B8%D1%8F)
    - [Tasks или же задачи](#tasks-%D0%B8%D0%BB%D0%B8-%D0%B6%D0%B5-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8)
    - [Celery beat или запуск задачи по расписанию](#celery-beat-%D0%B8%D0%BB%D0%B8-%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8-%D0%BF%D0%BE-%D1%80%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D1%8E)

<!-- /MarkdownTOC -->

## Введение

**В Django бизнес-логика должна жить в:**.

- Сервисы - функции, которые в основном занимаются записью в базу данных.
- Селекторы - функции, которые в основном заботятся о получении информации из базы данных.
- Функции модели (если логика затрагивает только этот объект, без использования связи с другими моделями).

**В Django бизнес-логика не должна жить в:**.

- API и представлениях.
- Сериализаторах и формах.
- Метод `save` модели.
- Пользовательские менеджеры или наборы запросов.
- Сигналы.

**Функции модели против селекторов:**

- Если функция охватывает несколько связей с моделями, то лучше использовать селектор.
- Если функция нетривиальна, занимает больше 10 строк или может легко вызвать проблему `N + 1` запросов при сериализации, то лучше воспользоваться селектором.

Общая идея состоит в том, чтобы "разделить зоны ответственности", чтобы они были поддерживаемы и тестируемы.

## FAQ?

> 🤔 Почему бы не разместить бизнес-логику в API / представлениях / сериализаторах / формах? Сейчас же норм вроде все!

Я просмотрел несколько проектов, и по факту у нас используется везде 1 паттерн: логика обычно описана в `actions`, в `serializers` или в `querysets`.
Это приводит к проблеме: что бы понять логику, условно, вывода хода строительства, тебе нужно пробежаться по 3-4 файлам.

Плюс бизнес логика часто пляшет между этими файлами, т.е. тебе приходиться возвращаться к уже прочитанным файлам, что приводит к 7-8 прыжкам между файлами.

Generic APIs & Views, в сочетании с сериализаторами, действительно отлично подходит для обычного CRUD.
Но часто у нас логика реализована "внутри" CRUD, так плюсом еще идут `actions`.
И вот тут уже программист может писать как хочет, причем по-разному на разных проектах(я сам так делал, каюсь...).
Это вызывает часто скрытый негатив, у разработчиков, которые потом правят такой код. Что бы этого было поменьше, решено было написать данный style guide.

> 🤔 Почему бы не поместить нашу бизнес-логику в пользовательские менеджеры(Manager) и/или наборы запросов(QuerySets)?
> Сейчас же на некоторых проектах так и есть, удобно же!

На самом деле мы этот делаем по факту на всех проектах, это очень удобно, когда такая логика реализована для маленьких модулей(например requests).

Проблемы начинаются когда мы начинаем реализовывать средне-большие модули, с тонной логики(например пользователи или объекты недвижимости).

Поэтому пытаться поместить всю бизнес-логику в пользовательский менеджер - не всегда самая лучшая идея, потому что:

1. Бизнес-логика имеет свой собственный домен, который не всегда напрямую сопоставлен с вашей моделью данных (моделями).
2. Бизнес-логика чаще всего охватывает несколько моделей, поэтому очень сложно выбрать, где что разместить.
   1. Допустим, у вас есть пользовательская часть логики, которая затрагивает модели `A`, `B`, `C` и `D`. Куда вы его поместите?
3. Могут быть обращения к сторонним системам(CRM, mailgun и etc).

**Идея состоит в том, чтобы позволить вашей логике приложения жить отдельно от вашей модели данных и слоя API.**.

Если мы возьмем идею создания пользовательских наборов запросов/менеджеров и объединим ее с идеей позволить логике жить отдельно, мы получим то, что мы называем "слой сервисов".

**Сервисы могут быть функциями, классами, модулями или чем угодно, что имеет смысл для вашего конкретного случая.**

Учитывая все это, пользовательские менеджеры и наборы запросов являются очень мощными инструментами и должны использоваться для создания лучших интерфейсов для ваших моделей.

> 🤔 Почему бы не поместить нашу бизнес-логику в сигналы? По факту это может перекрыть реализацию сервисов.

Как показала практика реализации бизнес логики на сигналах: это превращается пальбой по коленям.
Рекурсивные вызовы сигналов, сложность отладки и иногда странное поведение сигналов pre_save - это оч сильно мешает написать правильную и чистую логику.

Но все же:

1. Сигналы также являются отличным инструментом **для обработки кэша** вне уровня бизнес-логики.
2. Сигналы являются довольно хорошим функционалом для реализации callback фукнции при изменении **одного** объекта.

Поэтому в общем виде использовать сигналы нужно, но всегда нужно **исходить из здравого смысла**.

## Модели

Модели должны заботиться о модели данных и не более того.

### Базовая модель

Хорошей идеей будет определить `BaseModel`, которую вы можете унаследовать.

Обычно такие поля, как `created_at` и `updated_at` являются идеальными кандидатами для включения в `BaseModel`.

Определение первичного ключа также может попасть туда. Потенциальным кандидатом для этого является [`UUIDField`](https://docs.djangoproject.com/en/dev/ref/models/fields/#uuidf).

Вот пример `BaseModel`:

```python
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

Затем, когда вам понадобится новая модель, просто наследуйте `BaseModel`:

```python
class SomeModel(BaseModel):
    pass
```

### Валидация

Давайте посмотрим на пример модели:

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Конечная дата не может быть раньше начальной даты")
```

Мы определяем метод `clean` модели, потому что мы хотим убедиться, что мы получаем верные данные.

Теперь, чтобы метод `clean` был вызван, кто-то должен вызвать `full_clean` для экземпляра нашей модели перед сохранением.

**Наша рекомендация - сделать это в сервисе, прямо перед вызовом clean:**.

```python
def course_create(*, name: str, start_date: date, end_date: date) -> Course:
    obj = Course(name=name, start_date=start_date, end_date=end_date)

    obj.full_clean()
    obj.save()

    return obj
```

Это также хорошо работает с админкой Django, потому что формы, используемые там, будут вызывать `full_clean` на экземпляре.

**Есть несколько общих правил, когда добавлять валидацию в метод `clean` модели:**.

1. Если мы проверяем на основе нескольких **несвязанных полей**, т.е. это не должны быть ForeignKey и ManyToMany.
2. Если сама валидация достаточно проста.

**Валидация должна быть перенесена на сервисный уровень, если:**

1. Логика валидации сложная.
2. Требуется данные из связанных моделей или получение дополнительных данных(из CRM например).

### Валидация - constraints

Меньше кода нужно писать, меньше кода нужно поддерживать, база данных позаботится о данных, даже если они будут вставлены из другого места.

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ограничения = [
            constraints.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
```

Теперь, если мы попытаемся создать новый объект через `course.save()` или через `Course.objects.create(...)`, мы получим `IntegrityError`, а не `ValidationError`.

На самом деле это может быть недостатком подхода, потому что теперь нам придется иметь дело с `IntegrityError`, который не всегда имеет нормальное сообщение об ошибке.

Документация Django по ограничениям довольно скудная, поэтому вы можете ознакомиться со следующими статьями Адама Джонсона, где приведены примеры их использования:

1. [Using Django Check Constraints to Ensure Only One Field Is Set](https://adamj.eu/tech/2020/03/25/django-check-constraints-one-field-set/)
2. [Django's Field Choices Don't Constrain Your Data](https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/)
3. [Using Django Check Constraints to Prevent Self-Following](https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/)

> Примечание: Constraint конечно же мощная штука, но с ней нужно быть довольно осторожным, можно легко себе по ногам пальнуть.
> Поэтому если вы решили использовать это, то не поленитесь затестировать)

### Свойства

Свойства модели - это отличный способ быстрого доступа к полю из объекта модели.

Например, давайте посмотрим на свойства `has_started` и `has_finished` нашей модели `Course`:

```python
from django.utils import timezone
from django.core.exceptions import ValidationError


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Конечная дата не может быть раньше начальной даты")

    @property
    def has_started(self) -> bool:
        now = timezone.now()

        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()

        return self.end_date <= now.date()
```

Эти свойства удобны, потому что теперь мы можем ссылаться на них в сериализаторах или использовать их в шаблонах.

**Есть несколько общих правил, когда следует добавлять свойства в модель:**.

1. Если нам нужно простое значение, основанное на **несвязанных моделях**.
2. Если расчет значения достаточно прост (меньше 10 строк).

**Свойства должны быть чем-то другим (сервисом, селектором, утилитой) в следующих случаях:**.

1. Если нам нужно охватить связанные модели или получить дополнительные данные(из CRM например).
2. Если вычисления сложные.

Имейте в виду, что эти правила расплывчаты, потому что контекст вашей задачи тоже очень важен. Кароч применяйте **здравый смысл.**

### Методы

Методы модели также являются очень мощным инструментом, но использовать их нужно без особого фанатизма.

Рассмотрим пример с методом `is_within(self, x)`:

```python
from django.core.exceptions import ValidationError
from django.utils import timezone


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Конечная дата не может быть раньше начальной даты")

    @property
    def has_started(self) -> bool:
        now = timezone.now()

        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()

        return self.end_date <= now.date()

    def is_within(self, x: date) -> bool:
        return self.start_date <= x <= self.end_date
```

`is_within` не может быть свойством, так как требует аргумента. Поэтому вместо него используется метод.

Еще один отличный способ использования методов в моделях - это использование их для **установки атрибутов**, когда установка одного атрибута всегда должна сопровождаться установкой другого атрибута с производным значением.

Пример:

```python
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone


class Token(BaseModel):
    secret = models.CharField(max_length=255, unique=True)
    expiry = models.DateTimeField(blank=True, null=True)

    def set_new_secret(self):
        now = timezone.now()

        self.secret = get_random_string(255)
        self.expiry = now + settings.TOKEN_EXPIRY_TIMEDELTA

        return self
```

Теперь мы можем смело вызывать `set_new_secret`, который выдаст правильные значения для `secret` и `expiry`.

**Есть несколько общих правил, когда добавлять методы в модель:**.

1. Если нам нужно простое производное значение, требующее аргументов, основанное на **несвязанных моделях**, добавьте для этого метод.
2. Если расчет или установка производного значения достаточна проста(меньше 10 строк).
3. Если установка одного атрибута всегда требует установки значений других атрибутов, используйте метод для этого.

**Метод должн быть чем-то другим (сервисом, селектором, утилитой) в следующих случаях:**.

1. Если нам нужно использовать связанные модели или получить дополнительные данные.
2. Если вычисления сложные(больше 10 строк).

Имейте в виду, что эти правила расплывчаты, потому что часто важна ваша конкретная задача. Кароч применяйте **здравый смысл.**

## Сервисы

Сервисы - это место, где живет бизнес-логика, и обитает несметное количество багов.

Сервисный уровень говорит на специфическом языке домена программного обеспечения, может обращаться к базе данных и другим ресурсам, а также взаимодействовать с другими частями вашей системы.

Вот очень простая диаграмма, позиционирующая сервисный уровень в наших приложениях Django:

![Service layer](https://user-images.githubusercontent.com/387867/134778130-be168592-b953-4b74-8588-a3dbaa0b6871.png)

Сервис может быть:

- Простая функция.
- Классом.
- Целым модулем.
- Все, что имеет смысл в вашем случае.

В большинстве случаев сервис может быть простой функцией, которая:

- Находится в модуле `<ваше_приложение>/services.py`.
- Принимает аргументы только в виде ключевых слов, если не требует ни одного или одного аргумента.
- Аннотирована по типу (даже если вы не используете [`mypy`](https://github.com/python/mypy) в данный момент).
- Взаимодействует с базой данных, другими ресурсами и другими частями вашей системы.
- Выполняет бизнес-логику - от простого создания модели до сложных сквозных задач, вызова внешних сервисов и задач.

Пример сервиса, создающего пользователя:

```python
def user_create(*, email: str, name: str) -> User:
    user = User(email=email)
    user.full_clean()
    user.save()

    profile_create(user=user, name=name)
    confirmation_email_send(user=user)

    return user
```

Как вы видите, эта служба вызывает 2 другие службы - `profile_create` и `confirmation_email_send`.

В этом примере все, что связано с созданием пользователя, находится в одном месте и может быть отслежено.

### Соглашение об именовании

Если взять пример выше, то наш сервис называется `user_create`. Шаблон - `<сущность>_<действие>`.

Если сервис не используется "во вне", т.е. он используется только внутри сервисов, и напрямую нигде больше не используется,
то лучше поставить `_` перед названием метода. Например `def _user_create()`

В итоге мы получим:

1. Единородный нейминг
2. Быстрой поиск функционала через ctrl+shift+f

### Расширение логики сервисов

Если у вас достаточно простое приложение Django с кучей сервисов, все они могут счастливо жить в модуле `service.py`.

Но когда все становится большим, вы можете захотеть разделить `services.py` на папку с подмодулями, в зависимости от различных поддоменов, с которыми вы имеете дело в вашем приложении.

Например, допустим, у нас есть приложение `authentication`, где у нас есть 1 подмодуль в модуле `services`, который имеет дело с `jwt`, и один подмодуль, который имеет дело с `oauth`.

Структура может выглядеть следующим образом:

```
services
├── __init__.py
├── jwt.py
└── oauth.py
```

> Тут единственное замечание: если сервис используется в другом месте, то нужно его прокинуть в `__init__.py`.
> Если сервис используется внутри модуля `services`, то нейминг сервиса должен быть `_` перед названием, пример: `def _user_create()`

### Селекторы

В большинстве наших проектов мы различаем "Добавление данных в базу данных" и "Получение данных из базы данных":

1. О добавлении данных заботятся сервисы.
2. **Селекторы заботятся об извлечении данных**.
3. Селекторы можно рассматривать как "разновидностью" сервисов, которые специализируются на получении данных.

Селектор подчиняется тем же правилам, что и сервис.

Например, в модуле `<ваше_приложение>/selectors.py`, мы можем иметь следующее:

```python
def user_list(*, fetched_by: User) -> Iterable[User]:
    user_ids = user_get_visible_for(user=fetched_by)

    query = Q(id__in=user_ids)

    return User.objects.filter(query)
```

Как вы видите, `user_get_visible_for` - это один селектор.

Вы можете возвращать наборы запросов, или списки, или все, что имеет смысл в вашем конкретном случае.

### Тестирование

Поскольку сервисы содержат нашу бизнес-логику, они являются идеальным кандидатом для тестов.

Если вы решили покрыть сервисный уровень тестами, у есть несколько общих правил, которым следует придерживаться:

1. Тесты **должны исчерпывающим образом охватывать бизнес-логику**. Вообще идеально будет, если еще будет дополнительно 1 тест, который покрывает весь пользовательский путь использования какого нибудь функционала.
2. Тесты **должны затрагивать базу данных** - создание и чтение из нее.
3. Тесты **должны имитировать вызовы асинхронных задач и все, что выходит за пределы проекта**.

При создании необходимого состояния для конкретного теста можно использовать комбинацию из:

- Фейков [faker](https://github.com/joke2k/faker)
- Фабрики [factory_boy](https://factoryboy.readthedocs.io/en/latest/orms.html)

**Давайте посмотрим на наш сервис из примера:**.

```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from project.payments.selectors import items_get_for_user
from project.payments.models import Item, Payment
from project.payments.tasks import payment_charge


def item_buy(
    *,
    item: Item,
    user: User,
) -> Payment:
    if item in items_get_for_user(user=user):
        raise ValidationError(f'Item {item} already in {user} items.')

    payment = Payment.objects.create(
        item=item,
        user=user,
        successful=False
    )

    payment_charge.delay(payment_id=payment.id)

    return payment
```

Сервис:

- Вызывает селектор для валидации.
- Создает объект.
- И запускает celery таску.

**Это наши тесты:**

```python
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django_styleguide.payments.services import item_buy
from django_styleguide.payments.models import Payment, Item


class ItemBuyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Test User')
        self.item = Item.objects.create(
            name='Test Item',
            description='Описание тестового товара',
            цена=10.15
        )

    @patch('project.payments.services.items_get_for_user')
    def test_buying_item_that_is_already_bought_fails(self, items_get_for_user_mock):
        """
        Поскольку у нас уже есть тесты для `items_get_for_user`,
        мы можем безопасно поиздеваться над ним здесь и дать ему соответствующее возвращаемое значение.
        """
        items_get_for_user_mock.return_value = [self.item]

        with self.assertRaises(ValidationError):
            item_buy(user=self.user, item=self.item)

    @patch('project.payments.services.payment_charge.delay')
    def test_buying_item_creates_a_payment_and_calls_charge_task(
        self,
        payment_charge_mock
    ):
        self.assertEqual(0, Payment.objects.count())

        payment = item_buy(user=self.user, item=self.item)

        self.assertEqual(1, Payment.objects.count())
        self.assertEqual(payment, Payment.objects.first())

        self.assertFalse(payment.successful)

        payment_charge_mock.assert_called()
```

## APIs & Serializers

> Примечание: вот здесь я сильно порезал исходную документацию, т.к. не совсеми вещами согласен. У них получает очень много лишнего кода.
> Нам для нормального построения документации в OpenAPI3.0, нужно использовать примерно наш текущий подход.

## Serializers

**Вот правила для сериализации API:**.

- Должен быть специальный **входной сериализатор** и специальный **выходной сериализатор**.
- **Входной сериализатор** заботится о входящих данных.
- **Выходной сериализатор** заботится о выходных данных.
- Для сериализаторов лучше создать папку `serializers` в корне модуля. И там хранить сериализаторы для каждой API в отдельной папке.

**В случае использования сериализаторов DRF, вот правила:**

- Сериализатор должен быть называться либо `InputSerializer`, либо `OutputSerializer`.
- Повторное использование сериализаторов может привести к неожиданному поведению, когда что-то изменится в базовых сериализаторах. Поэтому лучше для каждого случая заводить свой сериализатор, но без фанатизма.
- Сериализаторы, в идеале, должны выполнять роль валидации, но не создания объектов.

### Соглашение об именовании

Для API используем следующее соглашение об именовании: `<Entity><Action>Api`.

Вот несколько примеров: `UserCreateApi`, `UserSendResetPasswordApi`, `UserDeactivateApi` и т.д.

### Фильтры

**Вот правила для фильтрации API:**.

- Для фильтров лучше создать папку `filters` в корне модуля. И там хранить фильтры для каждой API в отдельной папке.
- Для реализации `specs` и `facets`, нужно наследоваться от FacetFilterSet.

> Если не знаете что такое `specs` и `facets`, попросите своего ментора или лида рассказать про это. Это важно.

## Ошибки и обработка исключений

Обработка ошибок и исключений - это большая тема и довольно часто - детали специфичны для конкретного проекта.

Поэтому мы разделим все на две части - **общие рекомендации**, а затем некоторые **специфические подходы** для обработки ошибок.

** Общие рекомендации таковы:**

1. Изучите, как работает обработка исключений (в контексте для Django Rest Framework).
2. Согласуйте, как должны выглядеть ваши ошибки API с вашими фронтами, либо с вашим лидом

**Есть несколько конкретных подходов:**.

1. Использовать исключения DRF по умолчанию с очень небольшими изменениями.
2. Подход, который должен использоваться в больших бизнес процессах (например в Онлайн бронировании).

### Как работает обработка исключений (в контексте DRF)

В DRF есть отличное руководство о том, как обрабатываются исключения, поэтому обязательно прочитайте его - <https://www.django-rest-framework.org/api-guide/exceptions/>.

Кроме того, вот аккуратная диаграмма с обзором процесса:

![Exception handler (1)](https://user-images.githubusercontent.com/387867/142426205-2c0356e6-ce20-425e-a811-072c3334edb0.png)

В основном, если обработчик исключений не может обработать данное исключение и возвращает `None`, это приведет к необработанному исключению и `500 Server Error`. Это часто хорошо, потому что вы не будете замалчивать ошибки, на которые нужно обратить внимание.

**Некоторые причуды, на которые нам нужно обратить внимание.**

#### DRF's `ValidationError`.

Например, если мы просто поднимем `rest_framework.exceptions.ValidationError` вот так:

```python
from rest_framework import exceptions


def some_service():
    raise ValidationError("Сообщение об ошибке здесь.")
```

Ответ будет выглядеть следующим образом:

```json
[
    "Некоторое сообщение"
]
```

Это выглядит странно, потому что если мы сделаем это следующим образом:

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.ValidationError({"error": "Some message"})
```

Ответ будет выглядеть следующим образом:

```json
{
    "error": "Some message"
}
```

В основном это то, что мы передали в качестве `detail` для `ValidationError`. Но это структура данных, отличная от исходного массива.

Теперь, если мы решим поднять еще одно из встроенных исключений DRF:

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.NotFound()
```

Ответ будет выглядеть следующим образом:

```json
{
    "detail": "Не найдено"
}
```

Это полностью отличается от того, что мы видели как поведение от `ValidationError`, и это может вызвать проблемы.

Пока что, поведение DRF по умолчанию может дать нам:

- Массив.
- Дикционарий.
- Конкретный `{"detail": "О боже мой, как я задолбался переводить и переписывать это стайл гайд!!!"}`

**Так что если нам нужно использовать поведение DRF по умолчанию, мы должны позаботиться об этом несоответствии.**.

#### Django's `ValidationError`.

Теперь, обработка исключений по умолчанию в DRF не в ладах с `ValidationError` в Django.

Вот этот фрагмент кода:

```python
from django.core.exceptions import ValidationError as DjangoValidationError


def some_service():
    raise DjangoValidationError("Некоторое сообщение об ошибке")
```

Приведет к необработанному исключению, вызывающему `500 Server Error`.

Это также произойдет, если эта `ValidationError` возникает при валидации модели, например:

```python
def some_service():
    user = BaseUser()
    user.full_clean() # Выбрасывает ValidationError
    user.save()
```

Это также приведет к `500 Server Error`.

Если мы хотим начать обрабатывать это, как если бы это была `rest_framework.exceptions.ValidationError`, нам нужно развернуть наш собственный [custom exception handler](https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling):

```python
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import exception_handler
from rest_framework.serializers import as_serializer_error
from rest_framework import exceptions


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    return response
```

Это, по сути, реализация по умолчанию, с добавлением этого фрагмента кода:

```python
if isinstance(exc, DjangoValidationError):
    exc = exceptions.ValidationError(as_serializer_error(exc))
```

Поскольку нам нужно сопоставить `django.core.exceptions.ValidationError` и `rest_framework.exceptions.ValidationError`, мы используем DRF `as_serializer_error`, который используется внутри сериализатора.

Таким образом, теперь мы можем получить Django's `ValidationError`, с нормальным обработчиком исключений DRF.

### Как должны выглядеть идеальные ошибки в нашем проекте (пока не внедрять, на согласовании фронтами)

Это очень важно и должно быть сделано как можно раньше в любом конкретном проекте.

По сути, это описание интерфейса ваших ошибок API - **Как ошибка будет выглядеть в виде ответа API?**.

**Вот основные идеи:**.

1. **Ваше приложение будет иметь свою собственную иерархию исключений**, которые будут выбрасываться бизнес-логикой.
2. Допустим, для простоты, что у нас будет только одна ошибка - `ApplicationError`.
   1. Она будет определена в специальном приложении `core`, в модуле `exceptions`. По сути, у нас будет `project.core.exceptions.ApplicationError`.
3. Мы хотим позволить DRF обрабатывать все остальное по умолчанию.
4. `ValidationError` теперь специальный и будет обрабатываться по-другому.
   1. Ошибка `ValidationError` должна возникать только при сериализации или валидации модели.

---

**Мы собираемся определить следующую структуру для наших ошибок:**

```json
{
    "message": "Сообщение об ошибке здесь",
    "extra": {}
}
```

Ключ `extra` может содержать произвольные данные для передачи информации фронтенду.

Например, когда у нас есть `ValidationError` (обычно исходящая от сериализатора или модели), мы собираемся представить ошибку следующим образом:

```json
{
    "message": "Ошибка валидации",
    "extra": {
        "fields": {
              "password": [
                  "Это поле не может быть пустым"
              ],
              "email": [
                   "Это поле не может быть пустым"
              ]
        }
    }
}
```

Это может быть передано во фронтенд, чтобы они могли искать `extra.fields`, чтобы представить эти специфические ошибки пользователю.

Для этого пользовательский обработчик исключений будет выглядеть следующим образом:

```python
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response

from styleguide_example.core.exceptions import ApplicationError


def custom_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # Если произошла непредвиденная ошибка (ошибка сервера и т.д.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra
            }
            return Response(data, status=400)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response
```

Посмотрите на этот код и попытайтесь понять, что происходит. **Стратегия такова - повторно использовать как можно больше из DRF и затем корректировать.**

Теперь мы будем иметь следующее поведение:

Код:

```python
from styleguide_example.core.exceptions import ApplicationError


def trigger_application_error():
    raise ApplicationError(message="Something is not correct", extra={"type": "RANDOM"})
```

Response:

```json
{
    "message": "Something is not correct",
    "extra": {
        "type": "RANDOM"
    }
}
```

---

Код:

```python
def some_service():
    raise DjangoValidationError("Некоторое сообщение об ошибке")
```

Response:

```json
{
    "message": "Ошибка валидации",
    "extra": {
        "fields": {
            "non_field_errors": [
                "Некоторое сообщение об ошибке"
            ]
        }
    }
}
```

---

Код:

```python
from django.core.exceptions import PermissionDenied

def some_service():
    raise PermissionDenied()
```

Response:

```json
{
    "message": "У вас нет разрешения на выполнение этого действия",
    "extra": {}
}
```

---

Код:

```python
from django.http import Http404

def some_service():
    raise Http404()
```

## Тестирование

В наших Django проектах мы разделяем наши тесты в зависимости от типа кода, который они представляют.

То есть, обычно у нас есть тесты для моделей, сервисов, селекторов и API / представлений.

Структура файлов обычно выглядит следующим образом:

```
имя_проекта
├── имя_приложения
│ ├── __init__.py
│ └── tests
│ ├──── __init__.py
│ ├──── models
│ │ │ └── __init__.py
│ │ └──── test_some_model_name.py
│ ├──── selectors
│ │ └── __init__.py
│ │ └──── test_some_selector_name.py
│ └──── services
│ │ └── __init__.py
│ │ └── test_some_service_name.py
│ └──── user_story - пользовательские сценарии
│ │ └── __init__.py
│ │ └── user_online_booking.py - полный сценарий бронирования помещения
└── __init__.py
```

### Соглашения об именовании

Мы следуем двум общим соглашениям об именовании:

- Имена тестовых файлов должны быть `test_the_name_of_the_thing_that_that_is_tested.py`.
- Тестовый пример должен быть `class TheNameOfTheThingThatIsTestedTests(TestCase):`.

Например, если у нас есть:

```python
def a_very_neat_service(*args, **kwargs):
    pass
```

Мы получим следующее имя файла:

```
project_name/app_name/tests/services/test_a_very_neat_service.py
```

И следующее для тестового случая:

```python
class AVeryNeatServiceTests(TestCase):
    pass
```

Для тестов служебных функций мы следуем аналогичной схеме.

Например, если у нас есть `project_name/common/utils.py`, то мы собираемся иметь `project_name/common/tests/test_utils.py` и поместить различные тестовые случаи в этот файл.

Если мы разделим модуль `utils.py` на подмодули, то то же самое произойдет и с тестами:

- `project_name/common/utils/files.py`
- `project_name/common/tests/utils/test_files.py`.

## Celery

Мы используем [Celery](http://www.celeryproject.org/) для следующих общих случаев:

- Общение со сторонними сервисами (отправка писем, уведомлений и т.д.)
- Разгрузка более тяжелых вычислительных задач вне HTTP-цикла.
- Периодические задачи (с использованием Celery beat).

Мы стараемся обращаться с Celery так, как будто это просто еще один интерфейс к нашей основной логике - это означает - \*_не размещайте там бизнес-логику_.

Пример задачи может выглядеть следующим образом:

```python
from celery import shared_task

from project.app.services import some_service_name as service


@shared_task
def some_service_name(*args, **kwargs):
    service(*args, **kwargs)
```

Это задача, имеющая то же имя, что и сервис, который содержит фактическую бизнес-логику.

**Конечно, могут быть и более сложные ситуации**, например, цепочка или связка задач, каждая из которых выполняет свою логику, связанную с доменом. В этом случае трудно изолировать все в сервисе, потому что теперь у нас есть зависимости между задачами.

**Более сложные сценарии зависят от контекста. Убедитесь, что вы знаете архитектуру и уверены в решении, которые вы принимаете. Всегда можно обратиться к лиду за помощью, или в backend в mattermost**.

### Структура

#### Конфигурация

Конфигурация `celery` в нашем приложении в папке settings (она может называться по другому, но крч рядом с файлом settings.py).
Там описаны все настройки для подключения, управления очередями и настройкой `Celery beat`

Примерная конфигурация:

```python
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()
if not settings.DEBUG:
    app.conf.beat_schedule = {
        "scrape_all_accounts": {
            "task": "instagram.tasks.all_accounts_parse_instagram_posts_task",
            "schedule": crontab(day_of_week=1),
        },
        "update_stocks": {
            "task": "common.tasks.stock_expire_date",
            "schedule": crontab(day_of_week=1),
        },
        "update_mortgage": {
            "task": "common.tasks.update_mortgage",
            "schedule": crontab(minute=0, hour=0),
        },

    }


app.conf.task_annotations = {
    "common.tasks.save_remote_image": {"rate_limit": "300/m", "time_limit": 2}
}

if __name__ == "__main__":
    app.start()

```

#### Tasks или же задачи

Они у нас размещаются в файле tasks.py, в каждом модуле отдельно.

#### Celery beat или запуск задачи по расписанию

- Для запуска celery beat в продакшене, **всегда используете отдельный контейнер**. [Почему?](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html#starting-the-scheduler)
