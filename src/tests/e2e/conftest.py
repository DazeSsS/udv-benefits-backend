import pytest
import asyncio

from datetime import timedelta

from app.internal.factories import AuthFactory, BenefitFactory, CategoryFactory, OrderFactory, UserFactory
from app.internal.schemas import BenefitSchemaAdd, CategorySchemaAdd, OrderSchemaAdd, UserSchemaAdd


@pytest.fixture
async def auth_service(session):
    auth_service = AuthFactory.get_auth_service(session=session)
    return auth_service

@pytest.fixture
async def benefit_service(session):
    benefit_service = BenefitFactory.get_benefit_service(session=session)
    return benefit_service

@pytest.fixture
async def category_service(session):
    category_service = CategoryFactory.get_category_service(session=session)
    return category_service

@pytest.fixture
async def order_service(session):
    order_service = OrderFactory.get_order_service(session=session)
    return order_service

@pytest.fixture
async def user_service(session):
    user_service = UserFactory.get_user_service(session=session)
    return user_service

@pytest.fixture
async def user_1(user_service):
    user_schema = UserSchemaAdd(
        email='example@gmail.com',
        first_name="Иван",
        last_name="Иванов",
        middle_name="Иванович",
        birth_date="2004-04-29",
        phone="89573456195",
        has_children="true",
        work_start_date="2024-09-18",
        legal_entity="UDV",
        position="hr",
        department="HR",
        is_admin=True,
        is_verified=True,
    )
    user = await user_service.add_user(user_schema)
    return user

@pytest.fixture
async def user_2(user_service):
    user_schema = UserSchemaAdd(
        email='example2@gmail.com',
        first_name="Иван",
        last_name="Иванов",
        middle_name="Иванович",
        birth_date="2004-04-29",
        phone="89573456195",
        has_children="true",
        work_start_date="2023-09-18",
        legal_entity="UDV",
        position="backend",
        department="Backend"
    )
    user = await user_service.add_user(user_schema)
    return user

@pytest.fixture
async def category_1(category_service):
    category_schema = CategorySchemaAdd(
        title="Здоровье"
    )
    category = await category_service.add_category(category=category_schema, icon=None)
    return category

@pytest.fixture
async def benefit_1(benefit_service, category_1):
    benefit_schema = BenefitSchemaAdd(
        **{
            "title": "Скидка на ДМС от \"Альфа-Страхование\"",
            "provider": "Альфа-Страхование",
            "description": "Выбирайте оптимальный уровень медицинского страхования в зависимости от ваших нужд. ДМС от \"Альфа-Страхование\" предлагает три уровня покрытия, от базового до премиального, чтобы каждый нашел вариант для себя.",
            "picture": "https://storage.yandexcloud.net/udv-benefits-bucket/benefits/default/health/%D0%94%D0%9C%D0%A1_%D0%BE%D0%B1%D1%89%D0%B8%D0%B9.jpg",
            "price": 1000,
            "requiredExperience": None,
            "childsRequired": False,
            "categoryId": category_1.id,
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
    benefit = await benefit_service.add_benefit(benefit_schema)
    return benefit

@pytest.fixture
async def order_1(order_service, user_1, user_2, benefit_1):
    order_schema = OrderSchemaAdd(
        benefit_id=benefit_1.id,
        option_id=1
    )
    order = await order_service.add_order(order=order_schema, user_id=user_2.id)
    return order

@pytest.fixture
async def login_token_1(auth_service, user_1):
    token = auth_service.create_jwt(payload={'user_id': user_1.id}, lifetime=timedelta(minutes=5))
    return token

@pytest.fixture
async def tokens_1(auth_service, login_token_1):
    tokens = auth_service.login(token=login_token_1)
    return tokens

@pytest.fixture
async def login_token_2(auth_service, user_2):
    token = auth_service.create_jwt(payload={'user_id': user_2.id}, lifetime=timedelta(minutes=5))
    return token

@pytest.fixture
async def tokens_2(auth_service, login_token_2):
    tokens = auth_service.login(token=login_token_2)
    return tokens
