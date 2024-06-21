import datetime
import sqlalchemy as sa
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.database import Base
from typing import Annotated, Optional

intpk = Annotated[int, mapped_column(primary_key=True)]


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    user_id: Mapped[Optional[int]] = mapped_column(sa.BIGINT, unique=True)
    username: Mapped[Optional[str]]
    topic: Mapped[Optional[str]]
    target: Mapped[Optional[str]]
    product: Mapped[Optional[str]]
    type_post: Mapped[Optional[str]]
    idea: Mapped[Optional[str]]
    history: Mapped[Optional[str]] = mapped_column(sa.Text)
    has_active: Mapped[Optional[bool]]
    created_date: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.sql.func.now()
    )
    user_data_rel: Mapped['UsersPosts'] = relationship(back_populates='category_rel')
    user_data_rels: Mapped['GenPosts'] = relationship(back_populates='category_rels')


class UsersPosts(Base):
    __tablename__ = "users_data"

    id: Mapped[intpk]
    user_id: Mapped[Optional[int]] = mapped_column(sa.BIGINT, sa.ForeignKey('users.user_id'))
    post: Mapped[Optional[str]] = mapped_column(sa.Text)
    created_date: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.sql.func.now()
    )
    category_rel: Mapped['Users'] = relationship(back_populates='user_data_rel')


class GenPosts(Base):
    __tablename__ = "gen_posts"

    id: Mapped[intpk]
    user_id: Mapped[Optional[int]] = mapped_column(sa.BIGINT, sa.ForeignKey('users.user_id'))
    post: Mapped[Optional[str]] = mapped_column(sa.Text)
    rate: Mapped[Optional[int]]
    created_date: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.sql.func.now()
    )
    category_rels: Mapped['Users'] = relationship(back_populates='user_data_rels')


class Criteria(Base):
    __tablename__ = "criteria"

    id: Mapped[intpk]
    criteria: Mapped[Optional[str]]
    criteria_rel: Mapped['CriteriaData'] = relationship(back_populates='criteria_rel')


class CriteriaData(Base):
    __tablename__ = "criteria_data"

    id: Mapped[intpk]
    criteria_data: Mapped[Optional[str]]
    criteria_id: Mapped[Optional[int]] = mapped_column(sa.ForeignKey('criteria.id'))
    criteria_rel: Mapped['Criteria'] = relationship(back_populates='criteria_rel')
