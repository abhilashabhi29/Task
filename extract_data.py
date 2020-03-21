import pandas as pd
import os
import glob
from db_settings import Settings


class ExtraData():


    def get_df(self):
        """ create a dataframe combining  multiple .csv files in the folder
        :param
        :return: pandas Dataframe
        """
        extension = 'csv'
        all_filenames = [i for i in glob.glob('files/*.{}'.format(extension))]
        cols_to_use = ['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TIMESTAMP']


        #combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
        #export to csv
        combined_csv.to_csv( "combined_csv2.csv", index=False, encoding='utf-8-sig')

        # create dataframe from csv files
        df = pd.read_csv('combined_csv2.csv', usecols= cols_to_use)
        os.remove("combined_csv2.csv")
        return df


    def remove_files(self):
        """ remove .csv files from the folder
        :param
        :return:
        """

        files = glob.glob('files/*.{}'.format('csv'))
        for f in files:
            os.remove(f)





    def push_df_to_db(self,conn,table):
        """ inserts the csv file in to sql table
        :param
         conn: Database connection
         table : Table where data needs to be inserted
        :return:
        """

        global df
        if table:
            conn.execute("DELETE  FROM users")
            df = self.get_df()
        query = ''' insert or replace into users ('SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TIMESTAMP') values (?,?,?,?,?,?,?,?,?,?) '''
        conn.executemany(query, df.to_records(index=False))
        conn.commit()
        self.remove_files()

