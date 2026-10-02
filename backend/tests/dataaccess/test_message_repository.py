from datetime import datetime, timezone as tz

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.dataaccess.db import Base
from app.dataaccess.models.message import Messages
from app.dataaccess.repositories.conversation import ConversationRepository
from app.dataaccess.repositories.message import MessageRepository
from app.models.conversation import ConversationCreateDTO
from app.models.message import MessageCreateFullDTO, Role


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
async def test_save_persists_message_in_database(session: AsyncSession):
    conversation_repo = ConversationRepository(session)
    conversation = await conversation_repo.save(
        ConversationCreateDTO(title="Roadmap planning")
    )

    repo = MessageRepository(session)
    dto = MessageCreateFullDTO(
        conversation_id=conversation.id,
        role=Role.USER,
        content="Can you summarize the backlog?",
        created_at=datetime(2026, 8, 30, 12, 0, tzinfo=tz.utc),
    )

    saved = await repo.save(dto)

    assert saved.id is not None
    assert saved.conversation_id == conversation.id
    assert saved.role == Role.USER
    assert saved.content == "Can you summarize the backlog?"
    assert saved.created_at == dto.created_at.replace(tzinfo=None)

    persisted = await session.get(Messages, saved.id)
    assert persisted is not None
    assert persisted.conversation_id == conversation.id
    assert persisted.role == Role.USER.value
    assert persisted.content == "Can you summarize the backlog?"
    assert persisted.created_at == dto.created_at.replace(tzinfo=None)


@pytest.mark.asyncio
async def test_get_by_conversation_id_returns_messages_in_order(session: AsyncSession):
    conversation_repo = ConversationRepository(session)
    conversation = await conversation_repo.save(
        ConversationCreateDTO(title="Sprint review")
    )

    repo = MessageRepository(session)
    first = MessageCreateFullDTO(
        conversation_id=conversation.id,
        role=Role.USER,
        content="First message",
        created_at=datetime(2026, 8, 30, 9, 0, tzinfo=tz.utc),
    )
    second = MessageCreateFullDTO(
        conversation_id=conversation.id,
        role=Role.ASSISTANT,
        content="Second message",
        created_at=datetime(2026, 8, 30, 10, 0, tzinfo=tz.utc),
    )

    await repo.save(first)
    await repo.save(second)

    messages = await repo.get_by_conversation_id(conversation.id)

    assert [message.content for message in messages] == [
        "First message",
        "Second message",
    ]
    assert [message.role for message in messages] == [Role.USER, Role.ASSISTANT]
    assert [message.conversation_id for message in messages] == [
        conversation.id,
        conversation.id,
    ]


@pytest.mark.asyncio
async def test_get_by_id_returns_message_or_none(session: AsyncSession):
    conversation_repo = ConversationRepository(session)
    conversation = await conversation_repo.save(
        ConversationCreateDTO(title="Message lookup")
    )
    repo = MessageRepository(session)
    saved = await repo.save(
        MessageCreateFullDTO(
            conversation_id=conversation.id,
            role=Role.USER,
            content="Find me",
        )
    )

    assert await repo.get_by_id(saved.id) == saved
    assert await repo.get_by_id(404) is None
