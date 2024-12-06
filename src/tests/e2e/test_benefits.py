import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_benefit(client: AsyncClient, clear):
    response = await client.post(
        '/categories',
        data={"title": "Здоровье"}
    )
    category = response.json()
    assert {
        "id": 1,
        "title": "Здоровье",
        "icon": None
    } == category

    response = await client.post(
        '/benefits',
        json={
            "title": "Скидка на ДМС от \"Альфа-Страхование\"",
            "provider": "Альфа-Страхование",
            "description": "Выбирайте оптимальный уровень медицинского страхования в зависимости от ваших нужд. ДМС от \"Альфа-Страхование\" предлагает три уровня покрытия, от базового до премиального, чтобы каждый нашел вариант для себя.",
            "picture": "https://storage.yandexcloud.net/udv-benefits-bucket/benefits/default/health/%D0%94%D0%9C%D0%A1_%D0%BE%D0%B1%D1%89%D0%B8%D0%B9.jpg",
            "price": 1000,
            "requiredExperience": None,
            "childsRequired": False,
            "categoryId": category.get('id'),
            "isActive": True,
            "content": {
                "instructions": "1) Выберите уровень ДМС<br> Определите подходящий для себя уровень покрытия: Базовый, Продвинутый или Премиум. Обратите внимание на различия в услугах и выберите грейд, который соответствует вашим потребностям.<br> 2) Подтвердите согласие с условиями и нажмите кнопку «Отправить заявку».<br> 3) Ожидайте подтверждение от \"Альфа-Страхование\"<br> После отправки заявки сотрудники \"Альфа-Страхование\" свяжутся с вами для подтверждения и уточнения деталей.<br> 4) Получите свой полис и начните пользоваться<br> После подтверждения и активации полиса вы получите его электронную версию на указанный e-mail, а также инструкцию по использованию ДМС и список медицинских учреждений. Теперь вы можете пользоваться своим полисом, обращаясь в клиники по мере необходимости.",
                "period": "one_year",
                "isCancellable": False
            },
            "options": [
                {
                    "title": "Базовый",
                    "description": "Базовый уровень ДМС включает в себя услуги неотложного стационара, включая вызов скорой помощи, а также бесплатную телемедицину.",
                    "requiredExperience": None
                },
                {
                    "title": "Продвинутый",
                    "description": "Продвинутый уровень ДМС включает в себя не только услуги скорой помощи и телемедицины, но и стоматологические услуги, а также услуги поликлиники бизнес-класса. Обратите внимание, что стоматология и поликлиника предоставляются за дополнительную плату.",
                    "requiredExperience": "three_months"
                },
                {
                    "title": "Премиум",
                    "description": "Премиум уровень включает в себя услуги скорой помощи, телемедицины, стоматологию и поликлинику бизнес-класса.",
                    "requiredExperience": "four_years"
                }
            ]
        }
    )
    benefit = response.json()
    del benefit['createdAt']
    assert {
        "id": benefit.get('id'),
        "title": "Скидка на ДМС от \"Альфа-Страхование\"",
        "provider": "Альфа-Страхование",
        "description": "Выбирайте оптимальный уровень медицинского страхования в зависимости от ваших нужд. ДМС от \"Альфа-Страхование\" предлагает три уровня покрытия, от базового до премиального, чтобы каждый нашел вариант для себя.",
        "picture": "https://storage.yandexcloud.net/udv-benefits-bucket/benefits/default/health/%D0%94%D0%9C%D0%A1_%D0%BE%D0%B1%D1%89%D0%B8%D0%B9.jpg",
        "price": 1000,
        "requiredExperience": None,
        "childsRequired": False,
        "categoryId": category.get('id'),
        "isActive": True,
        "category": {
            "id": 1,
            "title": "Здоровье",
            "icon": None
        }
    } == benefit

@pytest.mark.asyncio
async def test_get_benefit(client: AsyncClient, tokens_1, category_1, benefit_1, clear):
    response = await client.get(
        f'benefits/{benefit_1.id}',
        headers={
            'Authorization': f'Bearer {(await tokens_1).access_token}'
        }
    )
    benefit = response.json()
    del benefit['createdAt']
    assert {
            "id": benefit_1.id,
            "title": "Скидка на ДМС от \"Альфа-Страхование\"",
            "provider": "Альфа-Страхование",
            "description": "Выбирайте оптимальный уровень медицинского страхования в зависимости от ваших нужд. ДМС от \"Альфа-Страхование\" предлагает три уровня покрытия, от базового до премиального, чтобы каждый нашел вариант для себя.",
            "picture": "https://storage.yandexcloud.net/udv-benefits-bucket/benefits/default/health/%D0%94%D0%9C%D0%A1_%D0%BE%D0%B1%D1%89%D0%B8%D0%B9.jpg",
            "price": 1000,
            "requiredExperience": None,
            'requiredConditions': None,
            "childsRequired": False,
            "categoryId": category_1.id,
            "isActive": True,
            'category': {
                'icon': None,
                'id': category_1.id,
                'title': 'Здоровье',
             },
            "content": {
                "instructions": "1) Выберите уровень ДМС<br> Определите подходящий для себя уровень покрытия: Базовый, Продвинутый или Премиум. Обратите внимание на различия в услугах и выберите грейд, который соответствует вашим потребностям.<br> 2) Подтвердите согласие с условиями и нажмите кнопку «Отправить заявку».<br> 3) Ожидайте подтверждение от \"Альфа-Страхование\"<br> После отправки заявки сотрудники \"Альфа-Страхование\" свяжутся с вами для подтверждения и уточнения деталей.<br> 4) Получите свой полис и начните пользоваться<br> После подтверждения и активации полиса вы получите его электронную версию на указанный e-mail, а также инструкцию по использованию ДМС и список медицинских учреждений. Теперь вы можете пользоваться своим полисом, обращаясь в клиники по мере необходимости.",
                "period": "one_year",
                "isCancellable": False
            },
            "options": [
                {
                    "id": 1,
                    "title": "Базовый",
                    "description": "Базовый уровень ДМС включает в себя услуги неотложного стационара, включая вызов скорой помощи, а также бесплатную телемедицину.",
                    "requiredExperience": None,
                    'requiredCondition': None,
                },
                {
                    "id": 2,
                    "title": "Продвинутый",
                    "description": "Продвинутый уровень ДМС включает в себя не только услуги скорой помощи и телемедицины, но и стоматологические услуги, а также услуги поликлиники бизнес-класса. Обратите внимание, что стоматология и поликлиника предоставляются за дополнительную плату.",
                    "requiredExperience": "three_months",
                    'requiredCondition': 'Вариант «Продвинутый» доступен сотрудникам со стажем от 3-х месяцев',
                },
                {
                    "id": 3,
                    "title": "Премиум",
                    "description": "Премиум уровень включает в себя услуги скорой помощи, телемедицины, стоматологию и поликлинику бизнес-класса.",
                    "requiredExperience": "four_years",
                    'requiredCondition': 'Вариант «Премиум» доступен сотрудникам со стажем от 4-х лет',
                }
            ]
        } == benefit
