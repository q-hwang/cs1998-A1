import os
import json
import sqlite3
from datetime import datetime

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


# noinspection SqlNoDataSourceInspection
class DB(object):
    """
  DB driver for the Todo app - deals with writing entities
  to the DB and reading entities from the DB
  """

    def __init__(self):
        self.conn = sqlite3.connect("todo.db", check_same_thread=False)
        self.conn.execute('''PRAGMA foreign_keys = ON;''')
        #self.create_task_table()
        # self.example_create_table()
        # TODO - Create all other tables here

    def create_task_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE task
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                DESCRIPTION TEXT NOT NULL, 
                CREATED_AT,
                DUE_DATE DATE);
               """)
        except Exception as e:
            print e
        try:
            self.conn.execute("""
                CREATE TABLE tags
                (TAG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT NOT NULL,
                TASK_ID INTEGER,
                FOREIGN KEY (TASK_ID) REFERENCES task(ID) 
                                      ON DELETE CASCADE
                )
              """)
        except Exception as e:
            print e

        try:
            self.conn.execute("""
                CREATE TABLE relations
                (TASK__ID INTEGER NOT NULL,
                TAG__ID INTEGER NOT NULL,
                FOREIGN KEY (TASK__ID) REFERENCES task(ID) 
                                        ON DELETE CASCADE,
                FOREIGN KEY (TAG__ID) REFERENCES tags(TAG_ID) 
                                        ON DELETE CASCADE,
                PRIMARY KEY (TASK__ID, TAG__ID));
                          """)
        except Exception as e:
            print e


    def delete_task_table(self):
        self.conn.execute("""
                                        DROP TABLE relations
                                        """)
        self.conn.execute("""
                                        DROP TABLE tags
                                        """)

        self.conn.execute("""
                                        DROP TABLE task
                                        """)
        #self.__init__()


    def add_task(self, data):
        name = data["name"]
        description = data['description']
        due_date = data["due_date"]
        tags = str(data["tags"])

        cursor = self.conn.cursor()
        cursor.execute("""
                INSERT INTO task (NAME, DESCRIPTION, CREATED_AT, DUE_DATE) 
                VALUES (?, ?, ?, ?);  
                      """, (name, description,datetime.now(), due_date))
        self.conn.commit()

        task_id = cursor.lastrowid
        #print task_id

        tags = tags.split(",")
        for tag in tags:
            #print tag
            cursor.execute("""
                  INSERT INTO tags (tag, TASK_ID) VALUES (?,?);  
                            """, (tag,task_id))
            tag_id = cursor.lastrowid
            self.conn.commit()

            cursor.execute("""
                  INSERT INTO relations (TAG__ID, TASK__ID) VALUES (?,?);  
                            """, (tag_id, task_id))
            self.conn.commit()

        result_cursor = self.conn.execute("""
                SELECT * FROM task WHERE task.ID = ?
                """, (task_id,))
        return self.to_list_dic(result_cursor)[0]

    def get_all_tasks(self):
        result_cursor = self.conn.execute("""
                        SELECT * FROM task 
                        """)
        return self.to_list_dic(result_cursor,'caps')

    def get_in_name(self,data):
        name = data['name']
        result_cursor = self.conn.execute("""
                        SELECT * FROM task WHERE task.NAME = ?
                        """, (name,))
        return self.to_list_dic(result_cursor,'caps')

    def get_in_tag(self,data):
        tag = data['tag']
        result_cursor = self.conn.execute("""
                        SELECT * FROM task WHERE task.ID IN (
                        SELECT DISTINCT TASK__ID FROM relations r, tags t WHERE r.TAG__ID = t.TAG_ID AND t.tag = ?
                        )
                        """, (tag,))
        # result_cursor = self.conn.execute("""
        #                         SELECT * FROM task ta, tags t
        #                         WHERE ta.ID = t.TASK_ID AND t.tag = ?
        #                         """, (tag,))
        return self.to_list_dic(result_cursor,'caps')

    def delete_task(self,data):
        id = data['id']
        result_cursor = self.conn.execute("""
                SELECT * FROM task WHERE task.ID = ?
                """,(id,))
        self.conn.execute("""
                DELETE FROM task WHERE task.ID = ?
                """, (id,))
        return self.to_list_dic(result_cursor)[0]


    def print_tables(self):
        print "task"
        c = self.conn.execute("""
                                                    SELECT *  FROM task
                                                    """)
        for row in c:
            print row

        print
        c = self.conn.execute("""
                                                    SELECT *  FROM relations 
                                                    """)
        for row in c:
            print row

        c = self.conn.execute("""
                                                    SELECT *  FROM tags 
                                                    """)
        for row in c:
            print row


    def to_list_dic(self,result_cursor,form = 'low'):
        columns = [column[0] for column in result_cursor.description]
        results = []

        for row in result_cursor:
            #print row
            tags = self.conn.execute("""
                            SELECT DISTINCT TAG FROM tags WHERE tags.TASK_ID = ?
                            """, (row[0],))

            t = ''
            for tag in tags:
                #print tag[0]
                t += ',' + tag[0]

            dic = {}
            if form == "low":
                dic = {'id': row[0], 'name': row[1], 'description': row[2],
                    'created_at': row[3], 'due_date': row[4], "tags": t[1:]}
            if form == 'caps':
                dic = dict(zip(columns, row))
                dic['TAGS'] = t[1:]
            results.append(dic)
        return results



    def delete_all_tasks(self):
        self.conn.execute("""
                DELETE FROM task
                """)


    def example_create_table(self):
        """
    Demonstrates how to make a table. Silently error-handles
    (try-except) because the table might already exist.
    """
        try:
            self.conn.execute("""
        CREATE TABLE example
        (ID INT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        ADDRESS CHAR(50) NOT NULL);
      """)
        except Exception as e:
            print e

    def example_query(self):
        """
    Demonstrates how to execute a query.
    """
        cursor = self.conn.execute("""
      SELECT * FROM example;
    """)

        for row in cursor:
            print "ID = ", row[0]
            print "NAME = ", row[1]
            print "ADDRESS = ", row[2], "\n"

    def example_insert(self):
        """
    Demonstrates how to perform an insert operation.
    """
        self.conn.execute("""
      INSERT INTO example (ID,NAME,ADDRESS)
      VALUES (1, "Joe", "Ithaca, NY");
    """)
        self.conn.commit()


# Only <=1 instance of the DB driver
# exists within the app at all times
DB = singleton(DB)
