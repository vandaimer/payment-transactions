from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db import async_session
from payments.views import Healthcheck, Restaurant, Transaction
from payments.schemas import RestaurantSchema, \
    ListOfTransactionSchema, NewTransactionSchema, \
    ReturnNewTransactionSchema, RestaurantResponseSchema


router = APIRouter()


@router.get("/healthcheck")
def healthcheck(db: Session = Depends(async_session)):
    try:
        return Healthcheck.status(db)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail='I am not live! :(',
        )


@router.post("/restaurant", response_model=RestaurantResponseSchema,
             status_code=201, tags=["Restaurant"])
def restaurante(restaurant: RestaurantSchema,
                db: Session = Depends(async_session)):
    try:
        return Restaurant.create(restaurant, db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Error to create a new restaurant.",
        )


@router.get("/transacoes/estabelecimento",
            response_model=ListOfTransactionSchema, tags=["Transaction"])
def transacoes(cnpj: int, db: Session = Depends(async_session)):
    try:
        return Transaction.all(cnpj, db)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Restaurant not found with cnpj: {cnpj}",
        )
    except Exception:
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
    except NoResultFound:
        raise HTTPException(
            status_code=400,
            detail=f"Restaurant not found with cnpj: {cnpj}",
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Error to retrieve transactions with cnpj: {cnpj}",
        )
