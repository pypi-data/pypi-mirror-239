# -*- coding:utf-8 -*-

import os
import re
import h5py
import shutil

import pandas as pd
from datetime import datetime

from .localAbstract import _DbManager, _DbBase, _TableBase
import cscdata
from .utils import remove_file_in_directory, read_h5, list_keys, find_file

class DbManager(_DbManager):
    """
    manage db as blow:
    parquet
    h5
    """
    # local_data_path = cscdata.LOCAL_DATA_PATH
    
    def __init__(self,
                 ) -> None:
        self.exists(self.local_data_path)

    @property
    def local_data_path(self):
        return cscdata.LOCAL_DATA_PATH

    def exists(self, repo_path):
        if not os.path.exists(repo_path):
            raise Exception(f"{repo_path} repo path not exists!")
    
    def parse_db(self, db_name):
        """get parquet db or h5 db"""
        db_path = os.path.join(self.local_data_path, db_name)
        if os.path.isdir(db_name):
            # support outer path here
            db_path = db_name
        if os.path.isdir(db_path):
            return 'parquet'
        elif db_name.endswith('.h5'):
            return 'h5'
        else:
            return 'others'
    
    def use_db(self, db_name):
        self.db_engine = self.parse_db(db_name)
        if self.db_engine == 'parquet':
            self.db = ParquetDB(db_name)
        elif self.db_engine == 'h5':
            self.db = H5DB(db_name)
        else:
            raise Exception("default parquet file db, support 'h5' and 'parquet', check your database create or not.")
        return self.db

    def create_db(self, db_name):
        """create dbm support directory and h5"""
        table_path = os.path.join(self.local_data_path, db_name)
        if not os.path.exists(table_path) and (db_name.endswith('.h5') or db_name.endswith(".hdf5")):
            with h5py.File(table_path, 'w') as f:
                pass
        elif not os.path.exists(table_path):
            os.mkdir(table_path)
        

class DbBase(_DbBase):
    def __init__(self,
                 db_name:str = None
                 ) -> None:
        self.db_name = db_name
        self.db_path = None
        self.exists() #check db_name and get db_path
        self.table_path = None

    @property
    def local_data_path(self):
        return cscdata.LOCAL_DATA_PATH
    
    def exists(self):
        """check db's file_name or h5_file_name whether in work path"""
        self.db_path = find_file(self.db_name , self.local_data_path)

    def show_path(self,):
        """show db path"""
        return self.db_path

    def show_tables(self):
        """show tables in db"""
        # return os.listdir(self.db_path)
        pass

    def parse_table(self):
        """parse table in db"""
        pass

    def use_table(self):
        """use db's table"""
        pass

    def create_table(self):
        """create table"""
        pass
    

class TableBase(_TableBase):
    def __init__(self,
                 table_path,
                 ) -> None:
        self.table_path = table_path

    @property
    def table_name(self):
        """get name by abs path"""
        return re.split("[\\\/]", self.table_path)[-1]
    
    def show_path(self):
        return  self.table_path

    def show_table_list(self):
        """different table struct"""
        pass

    def get_partitions_list(self, df, base_path, partition_cols):
        """检查已存在的partition路径"""
        partition_list = []
        if partition_cols is None or len(partition_cols) == 0:
            return partition_list
        for _, partition_df in df.groupby(partition_cols):
        # 生成每个分区的路径
            partition_path = base_path
            for col in partition_cols:
                partition_path = os.path.join(partition_path, f"{col}={partition_df.iloc[0][col]}")

            partition_list.append(partition_path)
            # 如果分区路径存在，则删除
            # if os.path.exists(partition_path):
            #     shutil.rmtree(partition_path)
        return partition_list

    def write_with_mode(self, df, base_path, partition_by: list = None, write_mode = 'w',**kwargs):
        """
        选择模式来写入数据
        备注:
            这里包括两个层面的写入模式，一种是本身table的直接写入，一种是带有partition的写入
        """
        partition_list = self.get_partitions_list(df, base_path, partition_by)
        if write_mode == 'w':
            for path in partition_list:
                if os.path.exists(path):
                    shutil.rmtree(path)
            if len(partition_by) == 0 or len(partition_list) == 0:
                # 如果不是按照分区保存的数据则删除table文件夹下的文件内容（目前不限制，删除全部非文件夹）
                remove_file_in_directory(base_path)
            df.to_parquet(base_path, partition_cols= partition_by,**kwargs)

        elif write_mode == 'a':
            df.to_parquet(base_path, partition_cols= partition_by,**kwargs)

        elif write_mode == 'e':
            if len(partition_by) ==0 and os.path.exists(base_path):
                raise Exception(f"exists duplicate table")
            if len(partition_by) !=0 and len(partition_list) != 0:
                raise Exception(f"exists duplicate partitions.")
            df.to_parquet(base_path, partition_cols= partition_by,**kwargs)

        elif write_mode == 'i':
            if len(partition_by) == 0 and len([os.path.join(base_path, i) for i in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, i)) ]) !=0 :
                # 文件层面，文件夹内的废文件夹内容不是0个 则忽略
                return 
            
            if len(partition_by) ==0 :
                df.to_parquet(base_path,**kwargs)
            else:
                for _, partition_df in df.groupby(partition_by):
                    partition_path = base_path
                    # 生成每个分区的路径
                    for col in partition_by:
                        partition_path = os.path.join(partition_path, f"{col}={partition_df.iloc[0][col]}")

                    # 检查分区路径是否存在，如果不存在则写入数据
                    if not os.path.exists(partition_path):
                        os.makedirs(partition_path, exist_ok=True)
                        partition_df.to_parquet(partition_path, index=False ,partition_cols = [], **kwargs)
                            
        else:
            raise Exception(f"write_mode = '{write_mode}' is error!")

    def to_narrow_parquet(self, df: pd.DataFrame, keys:list[str]= None, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        """
        提供生成窄表的方法
        备注:
            1. 保证传入的df为dataframe的格式
            2. keys为必须传入的参数, 通过keys来确定每个窄表中包含的字段 [*kyes, fea]
            3. partition_by可选
        """
        if self.table_path is None:
            raise Exception(f"please use function 'use_table' to init your target table first")

        if keys is None:
            raise Exception(f"please define 'keys'")

        if partition_by is None:
            partition_by = []

        columns = df.columns.to_list()
        feature_list = [i for i in columns if i not in keys]

        for fea in feature_list:
            if set(partition_by)&set(keys) != set(partition_by):
                raise Exception(f"make sure your folder '{partition_by}' in keys '{keys}'.")
            df_feature = df[keys+[fea]]
            base_path = os.path.join(self.table_path, fea)
            self.write_with_mode(df_feature, base_path, partition_by, write_mode= write_mode, **kwargs)

        print(f"save to {self.table_path}")

    def to_wide_parquet(self, df:pd.DataFrame, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        """保存为宽表"""
        if self.table_path is None:
            raise Exception(f"please use function 'use_table' to init your target table first")
        
        if partition_by is None:
            partition_by = []
        
        self.write_with_mode(df, self.table_path, partition_by, write_mode= write_mode, **kwargs)
        
        print(f"save to {self.table_path}")

    
    def update_time(self):
        """get file last update time in talbe_name"""
        table_list = self.show_table_list()
        last = 0
        for table_ in table_list:
            last_modified_time = os.path.getmtime(table_)
            last = max(last, last_modified_time)
        
        last_modified_time_readable = datetime.fromtimestamp(last)

        return last_modified_time_readable

    
 

class ParquetTable(TableBase):
    def __init__(self,
                 table_path,
                 ) -> None:
        super(ParquetTable, self).__init__(table_path)
        self.hist_idx_begin = 0

    @property
    def table_name(self):
        return super().table_name
    
    def show_path(self):
        return super().show_path()
    
    def show_table_list(self):
        """show file name start with table_name"""
        # return [os.path.join(os.path.dirname(self.table_path), i) for i in os.listdir(os.path.dirname(self.table_path)) if i.startswith(self.table_name)]
        return [os.path.join(os.path.dirname(self.table_path), self.table_name + 'parquet')]

    def update_time(self):
        return super().update_time()

    def pandas_read(self, filters: list[tuple] = None, **kwargs):
        """
        read by pandas
        """
        table_list = self.show_table_list()
        df = pd.read_parquet(table_list, filters=filters, **kwargs)
        return df

    def spark_read(self, spark_session, filters= None):
        """
        read by spark
        """
        table_list = self.show_table_list()
        sdf = spark_session.read.parquet(*table_list)

        here_condition_filter = []
        for col, rel, val in filters:
            here_condition_filter.append(f'df[{col}]' + rel + val)
        sdf = sdf.filter(eval("&".join(here_condition_filter)))
        
        return sdf

    def read_df(self, feature_col = None, engine = None, filters: list[tuple] = None, **kwargs):
        """ return df by engine"""
        if isinstance(feature_col, str):
            feature_col = [feature_col]
        if engine is None :
            # default pandas
            if feature_col is None:
                feature_col = slice(None)
            df = self.pandas_read(filters = filters, **kwargs)[feature_col]
        else:
            #default spark
            if feature_col is None:
                feature_col = ["*"]
            df = self.spark_read(engine, filters= filters).select(*feature_col)
            
        return df


    def hist(self, n_day ,day_col = None, feature_col = None, engine = None):
        """ get history data"""
        date_filters = []
        _date_list = cscdata._TRADE_DTS.sort(reversed = True)
        for _i in range(n_day):
            date_filters.append((f"{day_col}", "==", _date_list[self.hist_idx_begin]))
            self.hist_idx_begin += 1
        # here get df by trade_dts(data_filters), if trade_dt not in df --> skip this day
        df = self.read_df(engine= engine, feature_col = feature_col, filters = date_filters)
        # total day
        return df

class DirectoryTable(TableBase):
    def __init__(self,
                 table_path,
                 ) -> None:
        super(DirectoryTable, self).__init__(table_path)
        self.hist_idx_begin =0

    @property
    def table_name(self):
        """show directory table name"""
        return super().table_name
    
    def show_path(self):
        """show directory table's abs path"""
        return super().show_path()
    
    def show_table_list(self):
        """show file name start with table_name"""
        return [os.path.join(os.path.dirname(self.table_path), i) for i in os.path.dirname(self.table_path) if i.startswith(self.table_name)]
    
    def update_time(self):
        """get file last update time in talbe_name"""
        super().update_time()

    def pandas_read(self, filters: list[tuple] = None, **kwargs):
        """
        read by pandas
        """
        # table_list = self.show_table_list()
        df = pd.read_parquet(self.table_path, filters=filters, **kwargs)
        return df

    def spark_read(self, spark_session, filters):
        """
        read by spark
        """
        # table_list = self.show_table_list()
        sdf = spark_session.read.parquet(self.table_path)

        here_condition_filter = []
        for col, rel, val in filters:
            here_condition_filter.append(f'df[{col}]' + rel + val)
        sdf = sdf.filter(eval("&".join(here_condition_filter)))

        return sdf


    def read_df(self, feature_col = None, engine = None, filters: list[tuple] = None, **kwargs):
        """ return df by engine"""
        if isinstance(feature_col, str):
            feature_col = [feature_col]
        if engine is None :
            # default pandas
            if feature_col is None:
                feature_col = slice(None)
            df = self.pandas_read(filters = filters, **kwargs)[feature_col]
        else:
            #default spark
            if feature_col is None:
                feature_col = ["*"]
            df = self.spark_read(engine, filters= filters).select(*feature_col)
            
        return df


    def hist(self, n_day, day_col = None, engine = None):
        """ get history data"""
        date_filters = []
        _date_list = cscdata._TRADE_DTS.sort(reversed = True)
        for _i in range(n_day):
            date_filters.append((f"{day_col}", "==", _date_list[self.hist_idx_begin]))
            self.hist_idx_begin += 1
        df = self.read_df(engine= engine, filters = date_filters)
        return df


class H5DB(DbBase):
    """consider usual 'dataset' structure, like -> {key: data}"""
    def __init__(self,
                 db_name) -> None:
        super(H5DB, self).__init__(db_name)
        self.db  = self.db_init()

    def db_init(self):
        """init db with h5py"""
        return h5py.File(self.db_path, 'r')
    
    def show_path(self):
        return super().show_path()
    
    def show_tables(self):
        """list table name in h5"""
        # keys = list_keys(self.db_path)
        table_names = self.db.keys()
        return table_names
    
    def parse_table(self):
        """table name here in keys list"""
        pass

    def use_table(self, table_name):
        """use h5 db's talbe by h5py keys"""
        # self.table = self.db[table_name]
        self.table = H5Table(self, table_name)
        return self.table

    def create_table(self, table_name, maxshape, chunks, **kwargs):
        """create h5 table with none"""
        with h5py.File(self.db_path , 'a') as f:
            if table_name not in f:
                f.create_dataset(table_name, maxshape = maxshape, chunks = chunks ,dtype ='i', **kwargs) #here maxshape best assign as a default value
            # else:
            #     # if exists, retrieve  
            #     f[table_name]
    def to_h5(self, table_name, df: pd.DataFrame, index = None, columns = None):
        """gen h5 in db from base df"""
        self.use_table(table_name).to_h5(df, index= index, columns= columns)
        

class H5Table:
    """write table base on db"""
    def __init__(self, db_inst , table_name) -> None:
        self.table_name = table_name
        self.db_inst = db_inst
    
    def table_name(self,):
        """get table name in h5db"""
        return self.table_name

    def show_path(self):
        """return the db path and db-key"""
        return self.db_inst.db_path, self.table_name

    def show_table_list(self):
        """list table name in h5"""
        return self.db_inst.show_tables()
    
    def update_time(self):
        """get file last update time """
        last = os.path.getmtime(self.db_inst.db_path)

        last_modified_time_readable = datetime.fromtimestamp(last)
        
        return last_modified_time_readable
    
    def as_numpy(self):
        """get h5 dataset with key, output as numpy array"""
        return self.db_inst.db[self.table_name][...]
    
    def to_narrow_parquet(self, *args, **kwargs):
        raise NotImplementedError("not implement here.")

    def to_wide_parquet(self, *args, **kwargs):
        raise NotImplementedError("not implement here.")
    
    def to_h5(self, df: pd.DataFrame, index = None, columns = None):
        """gen h5 file from base df"""
        #deal pandas as numpy array
        self.db_inst.db.close()
        if index is not None and columns is not None:
            df = df.pivot(index=index, columns=columns)
        
        with h5py.File(self.db_inst.db_path, 'a') as f:
            if self.table_name in f:
                dset = f[self.table_name]
                dataset_shape = dset.shape
                shape = df.values.shape

                if len(shape) != len(dataset_shape):
                    raise Exception("Shapes do not match.")
                # Calculate new shape after appending
                new_shape = (dataset_shape[0] + shape[0],) + dataset_shape[1:]
                dset.resize(new_shape)  # Resize dataset
                
                # Define the slice for the new data
                slices = (slice(dataset_shape[0], new_shape[0]),) + tuple(slice(None) for _ in shape[1:])
                dset[slices] = df.values

                dset[tuple(slices)] = df.values
            else:
                f.create_dataset(self.table_name,
                                data= df.values,
                                maxshape=(None,) + df.values.shape[1:],
                                chunks=(1,) + df.values.shape[1:])
                
        self.db_inst.db_init()


class ParquetDB(DbBase):
    def __init__(self,
                 db_name:str = None
                 ) -> None:
        super(ParquetDB, self).__init__(db_name)
    
    def show_path(self):
        """show parquet database path"""
        return super().show_path()
    
    def show_tables(self):
        """show parquet file in parquet dataset directory"""
        return os.listdir(self.db_path)

    def parse_table(self, table_name):
        """
        parse table
        note:
            read and save use the same parse method
        """
        self.table_path = os.path.join(self.db_path, table_name)
        # if not os.path.exists(self.table_path):
        #     os.mkdir(self.table_path)
        if os.path.isfile(self.table_path + '.parquet'):
            # only support parquet file here
            return 'file'
        else:
            return 'directory'
    
    def use_table(self, table_name):
        """use parquet db's table"""
        table_engine = self.parse_table(table_name)
        if table_engine == 'directory':
            self.table = DirectoryTable(self.table_path)
        elif table_engine == 'file':
            self.table = ParquetTable(self.table_path)
        else:
            raise Exception("no table init here!")
        return self.table

    def create_table(self, table_name):
        """create table as directory, no content here"""
        table_path = os.path.join(self.db_path, table_name)
        if not os.path.exists(table_path):
            os.mkdir(table_path)

class DataAPI(DbManager):
    def __init__(self,
                 db_name: str = None,
                 ) -> None:
        super().__init__()
        self.db_name = db_name
        self.db_engine = None
        self.db = None

        self.db_none()
        self.use_db(self.db_name)
    
    def db_none(self):
        """if db_name is none, create new db"""
        if self.db_name is None:
            self.db_name = 'default'
            self.create_db(self.db_name)

    def use_db(self, db_name):
        """
        change dataset to db_name
        NOTE:
            1. here's db_name support 'outer path'
            2. if you want change base outer path, using cscdata.init
        """
        self.db = super().use_db(db_name)
        return self.db

    def use_table(self, table_name):
        """"""
        return self.db.use_table(table_name)
    
    def pandas_read(self, table_name, filters = None, **kwargs):
        """pandas read_method"""
        df = self.db.use_table(table_name).pandas_read(filters, **kwargs)
        return df
    
    def spark_read(self, table_name,  sparksession):
        """spark read method"""
        dfs = self.db.use_table(table_name).spark_read(sparksession)
        return dfs

    def to_narrow_parquet(self, table_name, df: pd.DataFrame, keys:list[str]= None, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        """save as narrow parquet"""
        self.db.use_table(table_name).to_narrow_parquet(df, keys = keys, partition_by = partition_by, write_mode = write_mode, **kwargs)

    def to_wide_parquet(self, table_name, df: pd.DataFrame, partition_by: list[str] = None, write_mode = 'w', **kwargs):
        self.db.use_table(table_name).to_wide_parquet(df,  partition_by= partition_by, write_mode= write_mode, **kwargs)



    
