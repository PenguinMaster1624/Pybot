from .S3KitModels import S3Kits, S3Classes, S3Specials, S3Subs
from .OverwatchHeroModels import OWHeroes, OWRoles, OWSubroles
from .MK8DXTrackModels import MK8DXTracks, MK8DXCups
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///utils/Game Stuff.db')
Session = sessionmaker(engine)