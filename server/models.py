"""Module for defining the database models."""

from datetime import datetime

from sqlalchemy import DateTime, func

# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Mixin for adding created_at and updated_at timestamps to a model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


# Example model definitions
# class Item(Base, TimestampMixin):
#     """Model for an item in the inventory."""

#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)

#     # category_id = Column(Integer, ForeignKey("categories.id"))

#     # Example relationship definitions
#     # category = relationship("Category", backref="items", lazy="joined")
