from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, BLOB, Integer


class Base(DeclarativeBase):
  pass

class S3Kits(Base):
  __tablename__ = 's3_kits'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  main: Mapped[str] = mapped_column(String(19), nullable=False)
  sub_id: Mapped[int] = mapped_column(ForeignKey('s3_subs.id'), nullable=False)
  special_id: Mapped[int] = mapped_column(ForeignKey('s3_specials.id'), nullable=False)
  class_id: Mapped[int] = mapped_column(ForeignKey('s3_classes.id'), nullable=False)
  points_for_special: Mapped[int] = mapped_column(Integer, nullable=False)
  introduced: Mapped[str] = mapped_column(String(35), nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  sub: Mapped["S3Subs"] = relationship(back_populates='kit')
  special: Mapped["S3Specials"] = relationship(back_populates='kit')
  s3_class: Mapped["S3Classes"] = relationship(back_populates='kit')

class S3Subs(Base):
  __tablename__ = 's3_subs'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(10), nullable=False)
  ink_consumption: Mapped[int] = mapped_column(Integer, nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  kit: Mapped[list["S3Kits"]] = relationship(back_populates='sub')

class S3Specials(Base):
  __tablename__ = 's3_specials'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(9), nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  kit: Mapped[list["S3Kits"]] = relationship(back_populates='special')

class S3Classes(Base):
  __tablename__ = 's3_classes'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(8), nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  kit: Mapped[list['S3Kits']] = relationship(back_populates='s3_class')