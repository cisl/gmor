"""
test_model.py

__author__ = "David Bristow"
__copyright__ = "Copyright 2016"
__credits__ = []
__maintainer__ = "David Bristow"
__status__ = "Development"
"""
#pylint: disable=trailing-whitespace
#pylint: disable=global-variable-undefined
#from nose2.tools import *
import nose2
from gmor.util import lists_equal, ordered_lists_equal
from gmor.model import get_bin_list
from gmor.model import get_bin_lists
from gmor.model import get_dec_from_bin_arr
from gmor.model import valid_state
from gmor.model import is_all_non_neg

def test_get_bin_list():
	"""
	test_get_bin_list
	"""
	print 'test_get_bin_list'

	assert lists_equal(get_bin_list(0,1), [0])
	assert lists_equal(get_bin_list(0,2), [0,0])
	assert ordered_lists_equal(get_bin_list(1,2), [0,1])
	assert lists_equal(get_bin_list(3,2), [1,1])

def test_get_bin_lists():
	"""
	test_get_bin_lists
	"""
	print 'test_get_bin_lists'

	assert lists_equal(get_bin_lists(1), [[0],[1]])
	assert lists_equal(get_bin_lists(2), [[0, 0], [0, 1], [1, 0], [1, 1]])
	
def test_get_dec_from_bin_arr():
	"""
	test_get_dec_from_bin_arr
	"""
	print 'test_get_dec_from_bin_arr'

	assert get_dec_from_bin_arr([0]) == 0
	assert get_dec_from_bin_arr([1]) == 1
	assert get_dec_from_bin_arr([0,1]) == 1
	assert get_dec_from_bin_arr([1,1]) == 3
	
def test_valid_state():
	"""
	test_valid_state
	"""
	print 'test_valid_state'

	assert not valid_state([0],0)
	try:
		valid_state([0],0,verbose=True)
		assert False
	except ValueError:
		assert True
		
	assert valid_state([0],1)
	assert valid_state([1],1)
	
	assert not valid_state([2],1)
	try:
		valid_state([2],1,verbose=True)
		assert False
	except ValueError:
		assert True
		
	assert not valid_state([0,1],1)
	assert not valid_state([0,1],3)
	assert valid_state([0,1],2)
	
def test_is_all_non_neg():
	"""
	test_is_all_non_neg
	"""
	print 'test_is_all_non_neg'
	
	assert is_all_non_neg([0])
	assert is_all_non_neg([0,0])
	assert is_all_non_neg([1])
	assert is_all_non_neg([1,0])
	assert not is_all_non_neg([-1])
	assert not is_all_non_neg([0,-1])
