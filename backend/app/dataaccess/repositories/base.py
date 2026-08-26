from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def entity2model(self, entity, pydantic):
        model = pydantic.model_validate(entity)
        return model
