import psycopg2
import glob
import os


class ConnectMethods():
    def connectDB(self):
        self.connection = psycopg2.connect(user="postgres",
                                    password="shetty",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="nse")


    def populate_data(self, insert_Query, path):
        try:
            log_file = open('query.log', 'w')
            self.connectDB()
            cursor = self.connection.cursor()
            for filename in glob.glob(path):
                try:
                    cursor.execute(insert_Query%filename)
                    self.connection.commit()
                except (Exception, psycopg2.Error) as err:
                    cursor.execute('rollback;')
                    if 'duplicate key value violates unique constraint' in str(err):
                        log_file.write('Already exists - %s\n'%filename)
                    else:
                        log_file.write('Pending - %s\n'%filename)
                    print(err, filename)
        except (Exception, psycopg2.Error) as error:
            print(error)

        finally:
            log_file.close()
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()


    def retrieve_data(self, select_Query):
        try:
            self.connectDB()
            cursor = self.connection.cursor()
            cursor.execute(select_Query)
            db_data = cursor.fetchall()
            return db_data
        except (Exception, psycopg2.Error) as err:
            print(err)
            return ''

        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()


    def delete_data(self, delete_Query):
        try:
            self.connectDB()
            cursor = self.connection.cursor()
            cursor.execute(delete_Query)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print(error)

        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()


    def insert_data(self, insert_Query):
        try:
            log_file = open('query.log', 'w')
            self.connectDB()
            cursor = self.connection.cursor()
            try:
                cursor.execute(insert_Query)
                self.connection.commit()
            except (Exception, psycopg2.Error) as err:
                cursor.execute('rollback;')
                if 'duplicate key value violates unique constraint' in str(err):
                    print('duplicate')
                else:
                    log_file.write('Pending - %s\n'%insert_Query)
                print(err)
        except (Exception, psycopg2.Error) as err:
            print(err)

        finally:
            log_file.close()
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
