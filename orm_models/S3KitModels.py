from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, ForeignKey, BLOB


class Base(DeclarativeBase):
  pass

class S3Kits(Base):
  __tablename__ = 's3_kits'

  id: Mapped[int] = mapped_column(primary_key=True)
  main: Mapped[str] = mapped_column(String(19))
  sub_id: Mapped[int] = mapped_column(ForeignKey('s3_subs.id'))
  special_id: Mapped[int] = mapped_column(ForeignKey('s3_specials.id'))
  class_id: Mapped[int] = mapped_column(ForeignKey('s3_classes.id'))
  points_for_special: Mapped[int] = mapped_column()
  introduced: Mapped[str] = mapped_column(String(35))
  image: Mapped[bytes] = mapped_column(BLOB)

  sub: Mapped["S3Subs"] = relationship(back_populates='kit')
  special: Mapped["S3Specials"] = relationship(back_populates='kit')
  s3_class: Mapped["S3Classes"] = relationship(back_populates='kit')

class S3Subs(Base):
  __tablename__ = 's3_subs'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(10))
  ink_consumption: Mapped[int] = mapped_column()
  image: Mapped[bytes] = mapped_column(BLOB)

  kit: Mapped[list["S3Kits"]] = relationship(back_populates='sub')

class S3Specials(Base):
  __tablename__ = 's3_specials'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(9))
  image: Mapped[bytes] = mapped_column(BLOB)

  kit: Mapped[list["S3Kits"]] = relationship(back_populates='special')

class S3Classes(Base):
  __tablename__ = 's3_classes'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(8))
  image: Mapped[bytes] = mapped_column(BLOB)

  kit: Mapped[list['S3Kits']] = relationship(back_populates='s3_class')