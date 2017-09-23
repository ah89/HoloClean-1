import pandas as pd
import numpy as np
import sqlalchemy as sqla
import getpass
import logging


class dataengine:

    """Connects our program to the database

    """
    ################ Members ############
    
    
    
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    def __init__(self,meta_filepath):
        logging.basicConfig(filename='dataengine.log', level=logging.DEBUG)
        self.connect_metadb(meta_filepath)
        
    
    @staticmethod
    def connect_datadb(dt_filepath):
        """create a connection with the database"""
        dt_file = open(dt_filepath,"r")
        
        # Connection part for the data 
        addressdt = dt_file.readline()
        dbnamedt = dt_file.readline()
        userdt = dt_file.readline()
        passworddt = dt_file.readline()
        
        
        con_str_data="mysql+mysqldb://" + userdt[:-1] +":"+passworddt[:-1]+"@"+addressdt[:-1]+"/"+dbnamedt[:-1]
        
        data_engine = sqla.create_engine(con_str_data)
        
        try:
            data_engine.connect()      
        except:
            print("No connection to data database")  
        return data_engine
            
    def connect_metadb(self,meta_filepath):
        """create a connection with the database"""
        meta_file = open(meta_filepath,"r")
        
        
        # Connection part for the meta 
        addressmt = meta_file.readline()
        dbnamemt = meta_file.readline()
        usermt = meta_file.readline()
        passwordmt = meta_file.readline()
        
        con_str_meta="mysql+mysqldb://" + usermt[:-1] +":"+passwordmt[:-1]+"@"+addressmt[:-1]+"/"+dbnamemt[:-1]
        

        self.meta_engine = sqla.create_engine(con_str_meta)
        
        try:
            self.meta_engine.connect()       
        except:
            print("No connection to meta database")
               

    def register(self, chunk):
        """for the first chunk, create the table and return
        the name of the table"""
        name_table = raw_input("please write the name of the table for" +
                               "the mysql database: ")
        try:
            chunk.to_sql(name_table, con=self.engine, if_exists='append',
                         index=True, index_label=None)
            logging.info("correct insertion for" + name_table)
        except sqla.exc.IntegrityError:
            logging.warn("failed to insert values")
        return name_table

    def add(self, chunk, name_table):
        """adding the information from the chunk to the table"""
        try:
            chunk.to_sql(name_table, con=self.engine, if_exists='append',
                         index=True, index_label=None)
            logging.info("correct insertion for" + name_table)
        except sqla.exc.IntegrityError:
            logging.warn("failed to insert values")
            
    def add_meta(self,db_engine,dataset_id,table_name,table_meta):
        dbcur = db_engine.cursor()
        stmt = "SHOW TABLES LIKE 'metatable'"
        dbcur.execute(stmt)
        result = dbcur.fetchone()
        add_row="INSERT INTO 'metatable' ('dataset_id','tablename','schema') VALUES("+str(dataset_id)+","+str(table_name)+","+str(table_meta)+");"
        if result:
            # there is a table named "metatable"
            db_engine.execute(add_row)              
        else:
            #create db with columns 'dataset_id' , 'tablename' , 'schema'
            # there are no tables named "metatable"
            create_table=0

d=dataengine("metadb-config.txt")
dataengine.connect_datadb('datadb-config.txt')
print("Done!")

