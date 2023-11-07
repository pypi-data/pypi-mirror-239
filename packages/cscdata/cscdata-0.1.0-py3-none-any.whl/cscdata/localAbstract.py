from abc import ABC, abstractmethod
import cscdata

class _DbManager(ABC):
    """
    通过解析不同的db来调用不同的实例
    """
    @abstractmethod
    def parse_db(self):
        """parse different db type"""
        pass

    @abstractmethod
    def use_db(self):
        """use db, return instance"""
        pass
    
    @abstractmethod
    def create_db(self):
        """create db if not exists"""

class _DbBase(ABC):
    @abstractmethod
    def exists(self):
        """judge file is exists"""
        pass

    @abstractmethod
    def show_path(self):
        """show db abs path"""
        pass

    @abstractmethod
    def show_tables(self):
        """show tables in db"""
        pass

    @abstractmethod
    def parse_table(self):
        """parse db name. file or abs path"""
        pass

    @abstractmethod
    def use_table(self):
        """use db's table"""
        pass

    @abstractmethod
    def create_table(self):
        """create new table"""
        pass

class _TableBase(ABC):
    # @abstractmethod
    # def check_table(self):
    #     """check table path exists status"""
    #     pass

    @abstractmethod
    def table_name(self):
        """get table name"""
        pass

    @abstractmethod
    def show_path(self):
        """show table abs path"""
        pass

    @abstractmethod
    def show_table_list(self):
        """show details in table path"""
        pass

    # @abstractmethod
    # def to_narrow_parquet(self):
    #     """save as narrow parquet"""
    #
    # @abstractmethod
    # def to_wide_parquet(self):
    #     """save as wide parquet"""
    #     pass

    @abstractmethod
    def update_time(self):
        """get table's update time"""

