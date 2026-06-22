from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, BLOB, Text, Integer


class Base(DeclarativeBase):
  pass

class OWRoles(Base):
  __tablename__ = 'ow_roles'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(8), nullable=False)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  subrole: Mapped[list['OWSubroles']] = relationship(back_populates='role')
  hero: Mapped[list['OWHeroes']] = relationship(back_populates='role')

class OWSubroles(Base):
  __tablename__ = 'ow_subroles'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(12), nullable=False)
  passive: Mapped[str] = mapped_column(Text, nullable=False)
  role_id: Mapped[int] = mapped_column(ForeignKey('ow_roles.id'), nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  role: Mapped['OWRoles'] = relationship(back_populates='subrole')
  hero: Mapped[list['OWHeroes']] = relationship(back_populates='subrole')

class OWHeroes(Base):
  __tablename__ = 'ow_heroes'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(15), nullable=False)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  role_id: Mapped[int] = mapped_column(ForeignKey('ow_roles.id'), nullable=False)
  subrole_id: Mapped[int] = mapped_column(ForeignKey('ow_subroles.id'), nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  role: Mapped['OWRoles'] = relationship(back_populates='hero')
  subrole: Mapped['OWSubroles'] = relationship(back_populates='hero')