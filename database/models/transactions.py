from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    amount: Mapped[float] = mapped_column(Numeric(20, 2), nullable=False)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id",
                                                      ondelete="CASCADE"),
                                           nullable=True)

    wallet = relationship("Wallet",
                          back_populates="transactions",
                          lazy="joined")
