import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db import async_session
from payments.views import Healthcheck, Restaurant, Transaction
from payments.schemas import RestaurantSchema, \
    ListOfTransactionSchema, NewTransactionSchema, \
    ReturnNewTransactionSchema, RestaurantResponseSchema


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/healthcheck")
def healthcheck(db: Session = Depends(async_session)):
    try:
        return Healthcheck.status(db)
    except Exception as e:
        log.exception(e)
        raise HTTPException(
            status_code=503,
            detail='I am not live! :(',
        )


@router.post("/restaurant", response_model=RestaurantResponseSchema,
             status_code=201, tags=["Restaurant"])
def restaurante(restaurant: RestaurantSchema,
                db: Session = Depends(async_session)):
    try:
        return Restaurant.create(restaurant, db)
    except ValueError as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail="Error to create a new restaurant.",
        )


@router.get("/transacoes/estabelecimento",
            response_model=ListOfTransactionSchema, tags=["Transaction"])
def transacoes(cnpj: int, db: Session = Depends(async_session)):
    try:
        return Transaction.all(cnpj, db)
    except NoResultFound as e:
        logger.error(e)
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant not found with cnpj: {cnpj}",
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail=f"Error to retrieve transactions with cnpj: {cnpj}",
        )


@router.post("/transacao", response_model=ReturnNewTransactionSchema,
             tags=["Transaction"], status_code=201)
def nova_transacoes(transaction: NewTransactionSchema,
                    db: Session = Depends(async_session)):
    cnpj = transaction.estabelecimento

    try:
        return Transaction.create(transaction, db)
    except NoResultFound as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail=f"Restaurant not found with cnpj: {cnpj}",
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=400,
            detail=f"Error to retrieve transactions with cnpj: {cnpj}",
        )
