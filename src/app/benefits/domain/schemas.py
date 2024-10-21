from pydantic import BaseModel


class BenefitSchemaAdd(BaseModel):
    title: str
    description: str
    price: int
    instructions: str
    category_id: int
    period: str # TODO: change type of period field
    is_cancellable: bool


class BenefitSchema(BenefitSchemaAdd):
    id: int
