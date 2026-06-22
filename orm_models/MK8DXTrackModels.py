from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, BLOB, Integer


class Base(DeclarativeBase):
  pass

class MK8DXCups(Base):
  __tablename__ = 'mk8dx_cups'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(11), nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  track: Mapped[list['MK8DXTracks']] = relationship(back_populates='cup')

class MK8DXTracks(Base):
  __tablename__ = 'mk8dx_tracks'

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(20), nullable=False)
  cup_id: Mapped[int] = mapped_column(ForeignKey('mk8dx_cups.id'), nullable=False)
  image: Mapped[bytes] = mapped_column(BLOB, nullable=False)

  cup: Mapped['MK8DXCups'] = relationship(back_populates='track')