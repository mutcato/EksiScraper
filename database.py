import config
import pymysql.cursors


class Database(object):
	"""docstring for Database"""
	def __init__(self):
		self.connection = pymysql.connect(host=config.hostname,
	                             user=config.username,
	                             password=config.password,
	                             db=config.database,
	                             charset='utf8mb4',
	                             cursorclass=pymysql.cursors.DictCursor)
	

	def query_insert(self, sql, data):
		"""
		sql is sql query (string)
		data is inserted data (array)
		"""
		try:
		    with self.connection.cursor() as cursor:
		        # Run the sql command
		        result = cursor.execute(sql, data)

		    # connection is not autocommit by default. So you must commit to save
		    # your changes.
		    self.connection.commit()
		    return cursor.lastrowid
		finally:
			x=1	   

	def query_select(self, sql, data):
		"""
		sql is sql query (string)
		data is in WHERE clause (array)
		"""
		try:
		    with self.connection.cursor() as cursor:
		        # Run the sql command
		        cursor.execute(sql, data)
		        result = cursor.fetchall()

		    # connection is not autocommit by default. So you must commit to save
		    # your changes.
		    self.connection.commit()
		    return result
		finally:
		    x=1

	def close_db_connection(self):
		self.connection.close()


