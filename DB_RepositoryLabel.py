#!/usr/bin/python
# -*- coding: UTF-8 -*-

import github
import datetime
import db_operation

class DB_RepositoryLabel:
    """
        This class represents DB_RepositoryLabel as a database operating class for github.Label.Label
    """

    repo = None
    label = None
    db = None
    table = "RepositoryLabel"


    def __init__(self, repo, label, db):
        self.repo = repo
        self.label = label
        self.db = db

    
    def open_if_connection_closed(self):
        try:

            if self.db is None:
                return False

            if self.db.open == 0:
                self.db = db_operation.connect_to_db_simple()
            
                if self.db is None:
                    return False
        
            return True

        except Exception, e:
            print e
            return False


    def save(self):
        try:

            if self.open_if_connection_closed() == False:
                return False

            if self.exist():
                return True

            sql = "insert into %s (color, name, url, repository) values ('%s', '%s', '%s', %d);" \
                    %(self.table, self.label.color, self.label.name, self.label.url.replace("'", "\\'").replace('"', '\\"'), self.repo.id)
            
            cursor = self.db.cursor()

            cursor.execute(sql)

            self.db.commit()

            return True
        
        except Exception as e:
            print e
            return False



    def exist(self):
        try:

            if self.open_if_connection_closed() == False:
                return False
            
            cursor = self.db.cursor()

            sql = "select count(*) from %s where url='%s';"%(self.table, self.label.url)

            cursor.execute(sql)

            result = cursor.fetchall()

            if result[0][0] == 0:
                return False
            
            return True

        except Exception as e:
            print e
            return False

