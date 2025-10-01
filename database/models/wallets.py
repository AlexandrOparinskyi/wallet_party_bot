from sqlalchemy import BigInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = (
        UniqueConstraint("chat_id", "name", name="uq_name_chat"),
    )

    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    transactions = relationship("Transaction",
                                back_populates="wallet",
                                lazy="selectin")

    @property
    def get_total(self):
        return sum([t.amount for t in self.transactions])
