from datetime import datetime, timezone as tz

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.dataaccess.db import Base
from app.dataaccess.models.conversation import Conversations
from app.dataaccess.repositories.conversation import ConversationRepository
from app.models.conversation import ConversationCreateDTO


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as db_session:
        yield db_session

    await engine.dispose()


@pytest.mark.asyncio
async def test_save_persists_conversation_in_database(session: AsyncSession):
    repo = ConversationRepository(session)
    now = datetime(2026, 8, 30, 12, 0, tzinfo=tz.utc)
    dto = ConversationCreateDTO(title="Weekly sync", created_at=now)

    saved = await repo.save(dto)

    assert saved.id is not None
    assert saved.title == "Weekly sync"
    assert saved.created_at == now.replace(tzinfo=None)
    assert saved.updated_at == now.replace(tzinfo=None)

    persisted = await session.get(Conversations, saved.id)
    assert persisted is not None
    assert persisted.title == "Weekly sync"
    assert persisted.created_at == now.replace(tzinfo=None)
    assert persisted.updated_at == now.replace(tzinfo=None)


@pytest.mark.asyncio
async def test_repository_reads_and_updates_persisted_data(session: AsyncSession):
    repo = ConversationRepository(session)

    first = await repo.save(ConversationCreateDTO(title="First conversation"))
    second = await repo.save(ConversationCreateDTO(title="Second conversation"))

    fetched_by_id = await repo.get_by_id(first.id)
    assert fetched_by_id is not None
    assert fetched_by_id.title == "First conversation"

    all_conversations = await repo.get_all()
    titles = {conversation.title for conversation in all_conversations}
    assert titles == {"First conversation", "Second conversation"}

    updated_at = datetime(2026, 8, 30, 15, 45, tzinfo=tz.utc)
    await repo.update_updated_at(first.id, updated_at)

    refreshed = await session.get(Conversations, first.id)
    assert refreshed is not None
    assert refreshed.updated_at == updated_at.replace(tzinfo=None)

    updated_record = await repo.get_by_id(first.id)
    assert updated_record is not None
    assert updated_record.updated_at == updated_at.replace(tzinfo=None)
