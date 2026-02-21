from fastapi import Depends
from typing import Annotated
from src.services.billing.base import BaseBillingService,  TransactionRepository
from src.services.llm import OllamaLLMService, LLMService
from src.services.billing.service import BillingService
from src.services.billing.repositories.in_memory import InMemoryTransactionRepository
import os
from dotenv import load_dotenv
from src.api.transactions.dependencies import BillingServiceDependency
from src.services.message.repositories.in_memory import InMemoryMessageRepository
from src.services.message.base import MessageRepository, BaseMessageService
from src.services.message.service import MessageService


load_dotenv()

def get_message_repo() -> MessageRepository:
    return InMemoryMessageRepository()


def get_message_service(message_repo: MessageRepository = Depends(get_message_repo)) -> BaseMessageService:
    return MessageService(message_repo)


def get_llm_service() -> LLMService:
    model_name = os.getenv("LLM_MODEL", "llama3.2:3b")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    return OllamaLLMService(model_name, ollama_base_url)


MessageServiceDependency = Annotated[BaseMessageService, Depends(get_message_service)]
LLMServiceDependency = Annotated[LLMService, Depends(get_llm_service)]