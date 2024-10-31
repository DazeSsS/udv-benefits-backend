from pydantic import BaseModel, ConfigDict


class BenefitSchemaAdd(BaseModel):
    title: str
    description: str
    price: int
    instructions: str
    category_id: int
    period: str # TODO: change type of period field
    is_cancellable: bool


class BenefitSchema(BenefitSchemaAdd):
    model_config = ConfigDict(from_attributes=True)

    id: int


class GroupedBenefitSchema(BaseModel):
    category_id: int
    category_title: str
    benefits: list['BenefitSchema']
