from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import CheckConstraint
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import *

import settings
import re

DeclarativeBase = declarative_base()

def db_connect():
	return create_engine(URL(**settings.DATABASE))

def create_HKResults_Table(engine):
	DeclarativeBase.metadata.create_all(engine)

class HKResults(DeclarativeBase):
    __tablename__ = "HKresults"
    

    id = Column(Integer, primary_key=True)
    Url = Column('url', String)
    Racecoursecode = Column('Racecoursecode', String, CheckConstraint('Racecoursecode.in_(["HV", "ST"])'), nullable=False)
    RaceDate = Column('RaceDate', String, nullable=False)
    RaceNumber = Column('RaceNumber', String, nullable=False)
    RaceIndex = Column('RaceIndex', String, nullable=False)
    ##
    HorseNo= Column('HorseNo', String, nullable=False)
    Horse= Column('Horse', String, nullable=False)
    HorseCode= Column('HorseCode', String, nullable=False)
    Jockey= Column('Jockey', String, nullable=False)
    Trainer= Column('Trainer', String, nullable=False)
    
    ActualWt= Column('ActualWt', String, nullable=False)
    DeclarHorseWt= Column('DeclarHorseWt', String, nullable=False)
    Draw= Column('Draw', String, nullable=False)
    LBW= Column('LBW', String, nullable=False)
    ##SECTIONALS
    #runstyle?
    RunningPosition= Column('RunningPosition', String, nullable=False)
    Sec1DBL = Column('Sec1DBL', String, nullable=False)
    Sec2DBL = Column('Sec2DBL', String, nullable=False)
    Sec3DBL = Column('Sec3DBL', String, nullable=False)
    Sec4DBL = Column('Sec4DBL', String, nullable=False)
    Sec5DBL = Column('Sec5DBL', String, nullable=False)
    Sec6DBL = Column('Sec6DBL', String, nullable=False)
    

    #TIMES
    #convert! Time
    FinishTime= Column('FinishTime', String, nullable=False)
    Sec1Time = Column('Sec1Time', String, nullable=False)
    Sec2Time = Column('Sec2Time', String, nullable=False)
    Sec3Time = Column('Sec3Time', String, nullable=False)
    Sec4Time = Column('Sec4Time', String, nullable=False)
    Sec5Time = Column('Sec5Time', String, nullable=False)
    Sec6Time = Column('Sec6Time', String, nullable=False)


    #used to identify data from sectionals
    # SecPlace 
    # SecHorseNo
    # SecHorseName


    WinOdds= Column('WinOdds', String, nullable=False)
   	

    #format for videos, images?
    # images= Column('images', BYTEA, nullable=False)
    # image_urls = Column('images', String, nullable=False)
    # files= Column('files', LargeBinary, nullable=False)

    WinDiv= Column('WinDiv', String, nullable=False)
    
    #incident report split on horsename returns list of occurences- 
    # [el for el in re.findall('[A-Z][A-Z].*', report[0]) if item["Horse"] in el]
    # one string: ' '.join([el for el in re.findall('[A-Z][A-Z].*', report[0]) if horses[0] in el])
    HorseReport = Column('HorseReport', String, nullable=True)
    #used to match up data from 2 pages
    # SecPlace = scrapy.Field()
    # SecHorseNo = scrapy.Field()
    # SecHorseName = scrapy.Field()
    ###############
