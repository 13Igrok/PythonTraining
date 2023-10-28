import Models.DBDAO

class DAO():
	def __init__(self, app):
		self.db = DBDAO(app)