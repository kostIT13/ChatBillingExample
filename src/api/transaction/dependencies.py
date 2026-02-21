from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.database.database import get_db
from fastapi import Depends
from src.services.billing.repositories.repository import SQLAlchemyTransactionRepository
from src.services.billing.service import BillingService
from src.services.billing.base import TransactionRepository
from typing import Annotated


def get_transaction_repo(session: AsyncSession = Depends(get_db)) -> TransactionRepository:
    return SQLAlchemyTransactionRepository(session)


def get_billing_service(trans_repo: TransactionRepository = Depends(get_transaction_repo)) -> BillingService:
    return BillingService(trans_repo)


BillingServiceDependency = Annotated[BillingService, Depends(get_billing_service)]
TransactionRepoDependency = Annotated[SQLAlchemyTransactionRepository, Depends(get_transaction_repo)]
