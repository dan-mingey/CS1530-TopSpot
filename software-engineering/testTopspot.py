import os
import unittest

from topspot import app, db

TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False

		db.drop_all()
		db.create_all()
	def tearDown(self):
		pass

#### helper methods #####

def register(self, email, password, confirm):
	return self.app.post(
		'/register', data=dict(usr=usr, password=password, confirm=confirm), follow_redirects=True
		)

def login(self, email, password):
	return self.app.post(
		'/login', data=dict(usr=usr, password=password), follow_redirects=True
		)


###### unit tests ########
def testValidUser(self):
	response = self.register('jenni')
	self.assertEqual(response.status_code, 200)

def testInvalidUser(self):
	response = self.register('william')
	self.assertEqual(response.status_code, 200)
	self.assertIn('Wrong username or password', response.data)

def testCaseValidUser(self):
	response = self.register('JENNI')
	self.assertEqual(response.status_code, 200)

def testCasePassword(self):
	response = self.login('jenni', 'PASS')
	self.assertEqual(response.status_code, 200)
	self.assertIn('Wrong username or password', response.data)

def testValidUserDb(self):
	response = self.login('jenni', 'pass')
	user = db.retrieveUser('jenni', 'pass')
	self.assertEqual(user, response)

def testInvalidUserDb(self):
	response = self.login('jenni', 'PASS')
	user = db.retrieveUser('jenni', 'PASS')
	self.assertNotEqual(user, response)

def testValidSessionUser(self):
	response = self.login('jenni', 'pass')
	user = session.usr
	self.assertEqual(user, response)

def testNewValidUserDb(self):
	response = self.login('erik', 'pass')
	user = db.retrieveUser('erik', 'pass')
	self.assertEqual(user, response)

def testNewValidUserDb(self):
	response = self.login('erik', 'pass')
	user = db.retrieveUser('erik', 'password')
	self.assertNotEqual(user, response)




if __name__ == '__main__':
	unittest.main()
