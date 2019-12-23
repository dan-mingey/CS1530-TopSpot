def newUserValidPassword(self):
	response = self.register('erik', 'password')
	self.login('erik', 'password')
	self.assertEquals(response.status_code, 200)

def newUserInvalidPass(self):
	response = self.register('erik', 'password')
	self.login('erik', 'incorrect')
	self.assertNotEquals(response.status_code, 200)

def userChangedPasswordAndValid(self):
	response = self.register('erik', 'password')
	self.password = "pw"
	self.login('erik', 'pw')
	self.assertEqual(response.status_code, 200)

def userChangedPassAndInvalid(self):
	response = self.register('erik', 'password')
	self.password = "pw"
	self.login('erik', 'password')
	self.assertNotEqual(response.status_code, 200)

def usernameExistsInDB(self):
	response = self.register('erik', 'password')
	self.login('erik', 'password')
	self.assertEqual(response.status_code, 200)