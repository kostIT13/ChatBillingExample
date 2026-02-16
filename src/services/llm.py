from typing import Literal, cast
from abc import ABC, abstractmethod
from dataclasses import dataclass
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


@dataclass
class MessageDTO:
    role: Literal["system", "human"]
    text: str 


@dataclass
class QuestionDTO:
    text: str 
    history: list[MessageDTO]


HistoryType = list[tuple[Literal["assistant", "human"], str]]

@dataclass
class AnswerDTO:
    text: str 
    used_tokens: int 


class LLMService(ABC):
    @abstractmethod
    async def execute(self, text: str, history: HistoryType) -> AnswerDTO: 
        raise NotImplementedError 
    


class OllamaLLMService(LLMService):
    _MESSAGE = [
        ("system", "You are friendly assistant"),
        MessagesPlaceholder("history"),
        ("human", "{question}")    
    ]

    def __init__(self, model_name: str, ollama_base_url: str):
        llm = ChatOpenAI(
            model = model_name,
            base_url=f"{ollama_base_url}/v1"    
        )
        prompt = ChatPromptTemplate(self._MESSAGE)
        self._chain = prompt | llm 

    async def execute(self, data: QuestionDTO) -> AnswerDTO:
        response = await self._chain.ainvoke({
            "question": data.text,
            "history": [(message.role, message.text) for message in data.history]
        })
        response = cast(AIMessage, response)
        return AnswerDTO(
            text=response.content,
            used_tokens=response.usage_metadata.get("total_tokens", 0)    
        )
    