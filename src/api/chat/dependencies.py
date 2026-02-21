from fastapi import Depends
from typing import Annotated
from src.services.llm import OllamaLLMService, LLMService
from src.services.billing.service import BillingService
import os
from dotenv import load_dotenv
from src.services.message.base import MessageRepository, BaseMessageService
from src.services.message.service import MessageService
from src.services.message.repositories.repository import SQLAlchemyMessageRepository
from src.apps.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.transactions.dependencies import BillingServiceDependency


load_dotenv()

def get_message_repo(session: AsyncSession = Depends(get_db)) -> MessageRepository:
    return SQLAlchemyMessageRepository(session)


def get_message_service(message_repo: MessageRepository = Depends(get_message_repo)) -> BaseMessageService:
    return MessageService(message_repo)


def get_llm_service() -> LLMService:
    model_name = os.getenv("LLM_MODEL", "llama3.2:3b")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    return OllamaLLMService(model_name, ollama_base_url)


MessageServiceDependency = Annotated[BaseMessageService, Depends(get_message_service)]
LLMServiceDependency = Annotated[LLMService, Depends(get_llm_service)]