import unittest
from floor import get_current_capacity
from floor import get_max_capacity


class TestFloor(unittest.TestCase):
	def test_floor_number0_capacity(self):
		floor = 1
		result = get_max_capacity()
		self.assertEqual(result, 63)
	def test_floor_number1_capacity(self):
		floor = 1
		result = get_max_capacity()
		self.assertEqual(result, 52)
	def test_floor_number2_capacity(self):
		floor = 2
		result = get_max_capacity()
		self.assertEqual(result, 21)
	def test_floor_number2_capacity(self):
		floor = 3
		result = get_max_capacity()
		self.assertEqual(result, None)
	def test_floor_number2_capacity(self):
		floor = 4
		result = get_max_capacity()
		self.assertEqual(result, 42)

	def test_floor_number1_curr_capacity(self):
		floor = 1
		result = get_current_capacity()
		self.assertEqual(result, 5)

	def test_floor_number2_curr_capacity(self):
		floor = 2
		result = get_current_capacity()
		self.assertEqual(result, 5)
	def test_floor_number3_curr_capacity(self):
		floor = 3
		result = get_current_capacity()
		self.assertEqual(result, 5)
	def test_floor_number4_curr_capacity(self):
		floor = 4
		result = get_current_capacity()
		self.assertEqual(result, 5)

if __name__ == '__main__':
	unittest.main()
