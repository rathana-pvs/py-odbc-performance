import pyodbc
import time


class ODBC:

    def __init__(self):
        self.report_sampling = {}
        self.table_name = "python_odbc_table"
        self.report = {}
        self.stress_load = 100
        self.conn = pyodbc.connect("driver={CUBRID Driver};server=localhost;port=33000;uid=dba;pwd=;db_name=demodb;")
        self.cur = self.conn.cursor()
        # self.cur.fast_executemany = True
        self.cur.execute("SET NAMES utf8;")
        self.initialize()
        # self.test()

    def initialize(self):
        self.cur.execute("drop table if exists " + self.table_name)
        sql = f"""
                CREATE TABLE {self.table_name} (
                    id INT PRIMARY KEY, 
                    name VARCHAR(255), 
                    descript VARCHAR(255));
                """
        self.cur.execute(sql)
        self.conn.commit()

    def insert(self):
        sql = f'insert into {self.table_name} values (?, ?, ?)'
        insert_data = [(i, f"Name_{i}", f"Value_{i}") for i in range(self.stress_load)]
        start = time.time()
        self.cur.executemany(sql, insert_data)
        self.conn.commit()
        end = time.time()
        return end - start

    def select(self):
        sql = f'select * from {self.table_name} limit {self.stress_load}'
        start = time.time()
        self.cur.execute(sql)
        end = time.time()
        return end - start

    def update(self):
        sql = f'update {self.table_name} set name = ? where id = ?'
        update_data = [(f"Name_{i + 1}", i) for i in range(self.stress_load)]
        start = time.time()
        self.cur.executemany(sql, update_data)
        self.conn.commit()
        end = time.time()
        return end - start

    def delete(self):
        sql = f'delete from {self.table_name} where id = ?'
        delete_data = [(i, ) for i in range(self.stress_load)]
        start = time.time()
        self.cur.executemany(sql, delete_data)
        self.conn.commit()
        end = time.time()
        return end - start

    def test(self):
        insert = self.insert()
        select = self.select()
        update = self.update()
        delete = self.delete()

        self.report = {
            'insert': insert,
            'select': select,
            'update': update,
            'delete': delete,
        }
        self.report = {key: value * 1000 for key, value in self.report.items()}
        print(self.report)

    def sample_test(self, sampling, stress_load):
        self.stress_load = stress_load
        for i in range(sampling):
            self.test()
            for key in self.report.keys():
                if key not in self.report_sampling:
                    self.report_sampling[key] = []
                self.report_sampling[key].append(self.report[key])
                time.sleep(1)
