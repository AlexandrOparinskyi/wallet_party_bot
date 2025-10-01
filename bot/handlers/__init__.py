from aiogram import Router

from .wallet import wallet_router

def register_handlers(router: Router):
    router.include_router(wallet_router)
