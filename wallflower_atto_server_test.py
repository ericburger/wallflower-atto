#####################################################################################
#
#  Copyright (c) 2016 Eric Burger, Wallflower.cc
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

__version__ = '0.0.1'

import json

from flask import Flask, request, jsonify, make_response, send_from_directory, render_template
import numpy as np

#import re
import datetime
import time
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
from sqlalchemy.sql import select 
from sqlalchemy.dialects import sqlite, postgresql

engine = create_engine('sqlite:///tmptest.db', convert_unicode=True, )
engine.dialect = sqlite.dialect(paramstyle="named")

metadata = MetaData(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

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
        
Base.metadata.create_all(bind=engine)

# Load config
config = {
    'network-id': 'local',
    'http_port': 5000,
    'database': {
        'name': 'wallflower_db_test',
        'type': 'sqlite'
    }
}


app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    return jsonify(**{'server-message':'An unknown internal error occured','server-code':500})

@app.errorhandler(404)
def not_found(error):
    return jsonify(**{'server-message':'Not a valid endpoint','server-code':404})
            
# Check if the network exists and create, if necessary
with app.app_context():
    t1 = []
    t2 = []
    t3 = []
    
    con = engine.connect()
    
    for i in range(100):
        
        t0 = time.time()
        con.execute(Network.__table__.insert(), network_id='admin'+str(time.time()), network_details='admin@localhost'+str(time.time()))
        t1.append( time.time()-t0 )
    
        t0 = time.time()
        create_network = Network(str(time.time()), str(time.time()))
        statement = create_network.__table__.insert().values(create_network.dict())
        con.execute( statement )
        t2.append( time.time()-t0 )
        
        
        create_network = Network(str(time.time()), str(time.time()))
        statement = create_network.__table__.insert().values(create_network.dict())
        query = statement.compile()
        query_str = str(query)
        query_params = query.params
        t0 = time.time()
        con.execution_options(sqlite_raw_colnames=True).execute( query_str, query_params )
        t3.append( time.time()-t0 )
        
    print np.mean(t1)
    print np.mean(t2)
    print np.mean(t3)
    
    
    # Generate raw SQL request with SQLAlchemy
    statement = select(['*']).\
        where( Network.id == 1 ).\
        limit(1).offset(0)
    print statement
    query = statement.compile(dialect=engine.dialect)
    query_str = str(query)
    query_params = query.params
    print con.execute( query ).first()
    
    print con.execute( statement ).first()
    
    print con.execute( 'select * from users where id = :1', [1] ).first()
    con.close()
    
if __name__ == '__main__':
    # Start the Flask app
    app.run(host='0.0.0.0',port=config["http_port"])
