#####################################################################################
#
#  Copyright (c) 2017 Eric Burger, Wallflower.cc
#
#  GNU Affero General Public License Version 3 (AGPLv3)
#
#  Should you enter into a separate license agreement after having received a copy of
#  this software, then the terms of such license agreement replace the terms below at
#  the time at which such license agreement becomes effective.
#
#  In case a separate license agreement ends, and such agreement ends without being
#  replaced by another separate license agreement, the license terms below apply
#  from the time at which said agreement ends.
#
#  LICENSE TERMS
#
#  This program is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License, version 3, as published by the
#  Free Software Foundation. This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU Affero General Public License Version 3 for more details.
#
#  You should have received a copy of the GNU Affero General Public license along
#  with this program. If not, see <http://www.gnu.org/licenses/agpl-3.0.en.html>.
#
#####################################################################################

__version__ = '0.1.1'

import json
import datetime
#import uuid
from sqlalchemy import Column, Integer, Float, String, Boolean, Table, DateTime

from wallflower_atto_db import Base

class Network(Base):
    __tablename__ = 'networks'
    id = Column(Integer(), primary_key=True)
    network_id = Column(String(80), unique=True)
    network_details = Column(String(1000))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    
    def __init__(self, network_id, network_details):
        self.network_id = network_id
        self.network_details = network_details
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = self.created_at
        
    def __repr__(self):
        return '<Network %r>' % self.network_id
    
    def loadFromRow( self, row ):
        self.id = row[0]
        self.network_id = row[1]
        self.network_details = row[2]
        self.created_at = row[3]
        self.updated_at = row[4]
        
    def dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        
    def network_details_dict(self):
        return json.loads( self.network_details )
        
class Object(Base):
    __tablename__ = 'objects'
    id = Column(Integer(), primary_key=True)
    network_id = Column(String(80), unique=False)
    object_id = Column(String(80), unique=False)
    object_details = Column(String(1000))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    
    def __init__(self, network_id, object_id, object_details):
        self.network_id = network_id
        self.object_id = object_id
        self.object_details = object_details
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = self.created_at
        
    def __repr__(self):
        return '<Object %r>' % self.network_id+'.'+self.object_id

    def loadFromRow( self, row ):
        self.id = row[0]
        self.network_id = row[1]
        self.object_id = row[2]
        self.object_details = row[3]
        self.created_at = row[4]
        self.updated_at = row[5]

    def dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        
class Stream(Base):
    __tablename__ = 'streams'
    id = Column(Integer(), primary_key=True)
    network_id = Column(String(80), unique=False)
    object_id = Column(String(80), unique=False)
    stream_id = Column(String(80), unique=False)
    stream_details = Column(String(1000))
    points_details = Column(String(1000))
    points_current = Column(String(1000))
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    
    def __init__(self, network_id, object_id, stream_id, stream_details, points_details):
        self.network_id = network_id
        self.object_id = object_id
        self.stream_id = stream_id
        self.stream_details = stream_details
        self.points_details = points_details
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = self.created_at
        
    def __repr__(self):
        return '<Stream %r>' % self.network_id+'.'+self.object_id+'.'+self.stream_id

    def loadFromRow( self, row ):
        self.id = row[0]
        self.network_id = row[1]
        self.object_id = row[2]
        self.stream_id = row[3]
        self.stream_details = row[4]
        self.points_details = row[5]
        self.points_current = row[6]
        self.created_at = row[7]
        self.updated_at = row[8]
        
    def dict(self):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        
        
def createPointsTable( table_name, data_type, data_length=0 ):
    if 0 == data_length:
        if data_type is basestring:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                 Column('value', String(255))
            )
        elif data_type is int:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                 Column('value', Integer())
            )
        elif data_type is float:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                 Column('value', Float())
            )
        elif data_type is bool:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                 Column('value', Boolean())
            )
    else:
        if data_type is basestring:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                *(Column('value'+str(i), String(255)) for i in range(data_length))
            )
        elif data_type is int:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                *(Column('value'+str(i), Integer()) for i in range(data_length))
            )
        elif data_type is float:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                *(Column('value'+str(i), Float()) for i in range(data_length))
            )
        elif data_type is bool:
            return Table(table_name, Base.metadata,
                 Column('timestamp', DateTime(), primary_key=True),
                *(Column('value'+str(i), Boolean()) for i in range(data_length))
            )

def getPointsTable( table_name, data_type, data_length=0 ):
    if table_name in Base.metadata.tables:
        return Base.metadata.tables[table_name]
    else:
        return createPointsTable( table_name, data_type, data_length=0 )