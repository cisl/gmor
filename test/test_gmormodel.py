"""
test_gmormodel.py

__author__ = "David Bristow"
__copyright__ = "Copyright 2016"
__credits__ = "Alison Goshulak"
__maintainer__ = "David Bristow"
__status__ = "Development"
"""
#pylint: disable=trailing-whitespace
#pylint: disable=global-variable-undefined
#from nose2.tools import *
import nose2
from gmor.model import GMORModel #import gmor
import numpy as np
from gmor.util import lists_equal, ordered_lists_equal


def setup():
	"""
	setup for single entity model
	"""
	#print "SETUP!"
	global model

	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels

	model = GMORModel()
	
	entities = ['Entity A']
	ent_types = {'Entity A':'function'}
	parents = {'Entity A':'function'}
	dependencies = {'Entity A':['Entity A']}
	resultant_states = {'Entity A':np.array([0, 1])}
	resource_limits = {}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies,
                     resultant_states, resource_limits, op_performance_levels)



def setup2():
	"""
	setup for two entity model
	"""
	#print "SETUP!"
	global model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	model = GMORModel()
	
	entities = ['Entity A', 'Entity B']
	ent_types = {'Entity A':'function', 'Entity B':'system'}
	parents = {'Entity A':'function', 'Entity B':'system'}
	dependencies = {'Entity A':['Entity B'], 'Entity B':['Entity B']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 1])}
	resource_limits = {}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies,
                     resultant_states, resource_limits, op_performance_levels)	

def setup3():
	"""
	setup for three entity model, including a resource entity
	"""
	#print "SETUP!"
	global model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	model = GMORModel()
	
	entities = ['Entity A', 'Entity B', 'Entity C']
	ent_types = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	parents = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	dependencies = {'Entity A':['Entity B'], 'Entity B':['Entity B', 'Entity C'], 'Entity C':['Entity C']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 0, 0, 1]), 'Entity C':np.array([0, 1])}
	resource_limits = {'Entity C':1.0}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies,
                     resultant_states, resource_limits, op_performance_levels)
					 
def setupjson():
	"""
	setup for json string test
	"""
	global jsonText
	
	jsonText = ('{'+
             '"entities": ["Entity A", "Entity B"], ' +
             '"ent_types": {"Entity A":"function", "Entity B":"resource"}, ' +
             '"parents": {"Entity A":"function", "Entity B":"resource"}, ' +
             '"dependencies": {"Entity A":["Entity B"], "Entity B":["Entity B"]}, ' +
             '"resultant_states": {"Entity A":[0, 1], "Entity B":[0, 1]}, ' +
             '"resource_limits": {"Entity B":1}, ' +
             '"op_performance_levels": {"Entity A":1.0}'+
             '}')
	
def teardown():
	"""
	teardown
	"""
	#print "TEAR DOWN!"
	model = GMORModel()

	
def test_gmormodel_init():
	"""
	"""
	print 'test_gmormodel_init'

	model = GMORModel()
	
	assert not model.entities # []
	assert not model.ent_types # {}
	assert not model.parents # {}
	assert not model.dependencies # {}
	assert not model.resultant_states # {}
	assert not model.resource_limits # {}
	assert not model.op_performance_levels # {}


def test_gmormodel_set_and_check_json():
	"""
	"""
	print 'test_gmormodel_set_and_check_json'
	result = model.set_and_check_json(jsonText)
	assert result
	
	try:
		result = model.set_and_check_json('')
		assert False
	except ValueError:
		assert True
	
	try:
		result = model.set_and_check_json('{"entities":[]}')
		assert False
	except ValueError:
		assert True
test_gmormodel_set_and_check_json.setup = setupjson
test_gmormodel_set_and_check_json.teardown = teardown
	
	
def test_gmormodel_set_and_check():
	"""
	"""
	print 'test_gmormodel_set_and_check'
	#model = GMORModel()
	result = model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
                              resource_limits, op_performance_levels)
	assert result
	
	result = model.set_and_check(entities, ent_types, parents, {'Entity A':[]}, resultant_states,
                              resource_limits, op_performance_levels)
	assert not result
test_gmormodel_set_and_check.setup = setup
test_gmormodel_set_and_check.teardown = teardown


def test_gmormodel_formatted_json_text():
	print 'test_gmormodel_formatted_json_text'
	
	result = model.formatted_json_text()
	assert model.set_and_check_json(result)
test_gmormodel_formatted_json_text.setup = setup2
test_gmormodel_formatted_json_text.teardown = teardown


def test_gmormodel_is_ent(): 
	"""
	returns true if the entity string name is in self.entities
	"""
	print 'test_gmormodel_is_ent'
	ent = 'Entity A'
	assert model.is_ent(ent)
	assert not model.is_ent(ent+ent)
test_gmormodel_is_ent.setup = setup
test_gmormodel_is_ent.teardown = teardown

def test_gmormodel_are_ents():
	"""
	"""
	print 'test_gmormodel_are_ents'
	assert model.are_ents(['Entity A', 'Entity B'])
	assert not model.are_ents(['Entity A', 'Entity C'])
test_gmormodel_are_ents.setup = setup2
test_gmormodel_are_ents.teardown = teardown


def test_gmormodel_is_dep():
	"""
	"""
	print 'test_gmormodel_is_dep'
	ent = 'Entity A'
	dep = 'Entity A'
	assert model.is_dep(ent, dep)
	assert not model.is_dep(ent, dep+dep)
test_gmormodel_is_dep.setup = setup
test_gmormodel_is_dep.teardown = teardown


def test_gmormodel_valid_res_sts():
	"""
	"""
	print 'test_gmormodel_valid_res_sts'
	ent = 'Entity A'
	assert model.valid_res_sts(ent, np.array([0, 1]))
	assert not model.valid_res_sts(ent, np.array([0, 2]))
	assert not model.valid_res_sts(ent, np.array([0]))
	
	try:
		model.valid_res_sts('not_an_ent', np.array([0, 1]), verbose=True)
		assert False
	except ValueError:
		assert True
		
	try:
		model.valid_res_sts(ent, [0, 1], verbose=True)
		assert False
	except ValueError:
		assert True
test_gmormodel_valid_res_sts.setup = setup
test_gmormodel_valid_res_sts.teardown = teardown


def test_gmormodel_n_dep_of_ent():
	"""
	"""
	print 'test_gmormodel_n_dep_of_ent'
	ent = 'Entity A'
	assert model.n_dep_of_ent(ent) == 1
	try:
		model.n_dep_of_ent(ent+ent)
		assert False # shouldn't execute
	except ValueError as ve:
		assert True
test_gmormodel_n_dep_of_ent.setup = setup
test_gmormodel_n_dep_of_ent.teardown = teardown


def test_gmormodel_num_res_sts():
	"""
	"""
	print 'test_gmormodel_num_res_sts'
	ent = 'Entity A'
	assert model.num_res_sts(ent) == 2
	try:
		model.num_res_sts(ent+ent)
		assert False # shouldn't execute
	except ValueError as ve:
		assert True
test_gmormodel_num_res_sts.setup = setup
test_gmormodel_num_res_sts.teardown = teardown


def test_gmormodel_num_ents():
	"""
	"""
	print 'test_gmormodel_num_ents'
	assert model.num_ents() == 1
test_gmormodel_num_ents.setup = setup
test_gmormodel_num_ents.teardown = teardown


def test_gmormodel_get_ents_with_internal_dep():
	"""
	"""
	print 'test_gmormodel_get_ents_with_internal_dep'
	assert lists_equal(model.get_ents_with_internal_dep(), ['Entity B', 'Entity C'])
test_gmormodel_get_ents_with_internal_dep.setup = setup3
test_gmormodel_get_ents_with_internal_dep.teardown = teardown


def test_gmormodel__valid_parent():
	"""
	"""
	print 'test_gmormodel__valid_parent'
	assert model._valid_parent('function')
	assert model._valid_parent('Entity B')
	assert model._valid_parent('')
	assert not model._valid_parent('Entity X')
test_gmormodel__valid_parent.setup = setup2
test_gmormodel__valid_parent.teardown = teardown
	
	
def test_gmormodel_valid_parent():
	try:
		print model.valid_parent('Entity A', 'Entity A')
		assert False # shouldn't execute
	except ValueError as ve:
		assert True
		
	try:
		print model.valid_parent('Entity X', '')
		assert False # shouldn't execute
	except ValueError as ve:
		assert True
		
	assert model.valid_parent('Entity A', 'function')
test_gmormodel_valid_parent.setup = setup2
test_gmormodel_valid_parent.teardown = teardown


def test_gmormodel__are_functions():
	"""
	"""
	print 'test_gmormodel__are_functions'
	assert model._are_functions(['Entity A'])
	assert not model._are_functions(entities)  # not all entities functions
test_gmormodel__are_functions.setup = setup2
test_gmormodel__are_functions.teardown = teardown


def test_gmormodel_ents_ready():
	"""
	"""
	print 'test_gmormodel_ents_ready'
	assert model.ents_ready()
	
	model.ent_types['Entity A'] = 'resource'
	assert not model.ents_ready()  # no functions	
	try:
		model.ents_ready(verbose=True)
		assert False
	except ValueError:
		assert True
	
	model.entities.append('Ill\egal')
	assert not model.ents_ready()  # illegal entity name
	
	model.entities[-1] = 'Illegal?'
	try:
		model.ents_ready(verbose=True)
		assert False
	except ValueError:
		assert True
		
	model2 = GMORModel()
	assert not model2.ents_ready()  # no entities	
	try:
		model2.ents_ready(verbose=True)
		assert False
	except ValueError:
		assert True
test_gmormodel_ents_ready.setup = setup
test_gmormodel_ents_ready.teardown = teardown


def test_gmormodel_deps_ready():
	"""
	"""
	print 'test_gmormodel_deps_ready'
	assert model.deps_ready()
	
	model.entities.append('Entity B')
	model.ent_types['Entity B'] = 'system'
	model.dependencies['Entity B'] = []
	assert not model.deps_ready()  # B has no dependencies
	try:
		model.deps_ready(verbose=True)
		assert False
	except ValueError:
		assert True
		
	model.dependencies['Entity B'] = ['Entity A']
	model.dependencies['Entity A'] = ['Entity B']
	assert not model.deps_ready()  # no internal dependencies	
	try:
		model.deps_ready(verbose=True)
		assert False
	except ValueError:
		assert True
		
	model2 = GMORModel()
	assert not model2.deps_ready()
test_gmormodel_deps_ready.setup = setup
test_gmormodel_deps_ready.teardown = teardown


def test_gmormodel_deps_ready2():
	"""
	"""
	print 'test_gmormodel_deps_ready2'
	assert model.deps_ready()  # resource can depend on itself
	
	model.entities.append('Entity D')
	model.ent_types['Entity D'] = 'resource'
	model.dependencies['Entity D'] = ['Entity D']
	model.dependencies['Entity C'].append('Entity D')
	assert not model.deps_ready()  # resource can't depend on different resource

	try:
		model.deps_ready(verbose=True)
		assert False
	except ValueError:
		assert True
test_gmormodel_deps_ready2.setup = setup3
test_gmormodel_deps_ready2.teardown = teardown


def test_gmormodel_res_sts_ready():
	"""
	"""
	print 'test_gmormodel_res_sts_ready'
	assert model.res_sts_ready()
	
	model.entities.append('Entity B')
	try:
		model.res_sts_ready()
		assert False # shouldn't execute
	except KeyError as ke:
		assert True
	model.dependencies['Entity B'] = 'Entity B'
	try: 
		model.res_sts_ready()
		assert False # shouldn't execute
	except KeyError as ke:
		assert True
	model.dependencies['Entity B'] = ['Entity B']
	model.resultant_states['Entity B'] = []
	assert not model.res_sts_ready()
	
	model.resultant_states['Entity B'] = [0, 1]
	try:
		model.res_sts_ready(verbose=True)
		assert False  # states are not numpy array type
	except ValueError:
		assert True
		
	model2 = GMORModel()
	assert model2.res_sts_ready() # the states are fine for empty model
test_gmormodel_res_sts_ready.setup = setup
test_gmormodel_res_sts_ready.teardown = teardown


def test_gmormodel_res_lm_ready():
	"""
	"""
	print 'test_gmormodel_res_lm_ready'
	assert model.res_lm_ready()
	
	# not a resource
	model.resource_limits['Entity A'] = 1
	assert not model.res_lm_ready()
	try:
		model.res_lm_ready(verbose=True)
		assert False
	except ValueError:
		assert True
	model.resource_limits = {}
	
	# not an entity
	model.resource_limits['Entity B'] = 1
	model.ent_types['Entity B'] = 'resource'
	assert not model.res_lm_ready()
	try:
		model.res_lm_ready(verbose=True)
		assert False
	except ValueError:
		assert True
		
	# should work
	model.entities.append('Entity B')
	assert model.res_lm_ready()
	
	# negative
	model.resource_limits['Entity B'] = -1
	assert not model.res_lm_ready()
	try:
		model.res_lm_ready(verbose=True)
		assert False
	except ValueError:
		assert True
test_gmormodel_res_lm_ready.setup = setup
test_gmormodel_res_lm_ready.teardown = teardown	


def test_gmormodel_op_p_ready():
	"""
	"""
	print 'test_gmormodel_op_p_ready'
	assert model.op_p_ready()
	
	model.op_performance_levels['Entity A'] = 0.5
	assert not model.op_p_ready()  # sum of levels is too small
	try:
		model.op_p_ready(verbose=True)
		assert False
	except ValueError:
		assert True
		
	model.entities.append('Entity B')
	model.ent_types['Entity B'] = 'resource'
	model.op_performance_levels['Entity B'] = 0.5
	assert not model.op_p_ready()  # not all functions
	try:
		model.op_p_ready(verbose=True)
		assert False
	except ValueError:
		assert True
test_gmormodel_op_p_ready.setup = setup
test_gmormodel_op_p_ready.teardown = teardown	

def test_gmormodel_ready():
	"""
	minimum entry requirements complete
	"""
	print 'test_gmormodel_ready'
	assert model.ready()
	
	model2 = GMORModel()
	assert not model2.ready()
test_gmormodel_ready.setup = setup
test_gmormodel_ready.teardown = teardown	


def test_gmormodel_add_entity():
	"""
	"""
	print 'test_gmormodel_add_entity'
	
	name = 'Entity A'
	entType = 'function'
	result = model.add_entity(name, entType)	
	assert not result
	
	name = 'Entity B'
	entType = 'system'
	result = model.add_entity(name, entType)
	
	assert result
	assert name in model.entities
	assert model.ent_types[name] == entType
	assert model.parents[name] == entType
	assert not model.ready()
	
	name = 'Entity C'
	entType = 'system'
	parent = 'Entity B'
	result = model.add_entity(name, entType, parent)
	
	assert result
	assert name in model.entities
	assert model.ent_types[name] == entType
	assert model.parents[name] == parent
	assert not model.ready()
	
	name = 'Entity D'
	entType = 'resource'
	parent = 'Entity D'
	result = model.add_entity(name, entType, parent)
	assert not result
	
	name = 'Entity E'
	entType = 'not a type'
	result = model.add_entity(name , entType)
	assert not result
test_gmormodel_add_entity.setup = setup
test_gmormodel_add_entity.teardown = teardown


def test_gmormodel_add_dep():
	"""
	"""
	print 'test_gmormodel_add_dep'
	
	assert not model.add_dep('Entity D', 'Entity A')
	
	assert not model.add_dep('Entity B', 'Entity D')
	
	assert not model.add_dep('Entity A', 'Entity B')
	
	model.entities.append('Entity D')
	model.ent_types['Entity D'] = 'resource'
	model.dependencies['Entity D'] = []
	assert not model.add_dep('Entity D', 'Entity C')
	
	assert model.add_dep('Entity D', 'Entity A')
	assert lists_equal(model.resultant_states['Entity D'], [0, 0])
test_gmormodel_add_dep.setup = setup3
test_gmormodel_add_dep.teardown = teardown


def test_gmormodel_merge_models():
	"""
	"""
	print 'test_gmormodel_merge_models'
	
	model2 = GMORModel()
	
	try:
		model.merge_models(model2)
		assert False
	except ValueError:
		assert True
		
	entities2 = ['Entity A', 'Entity B', 'Entity C']
	ent_types2 = {'Entity A':'system', 'Entity B':'function', 'Entity C':'resource'}
	parents2 = {'Entity A':'system', 'Entity B':'function', 'Entity C':'resource'}
	dependencies2 = {'Entity A':['Entity A'], 'Entity B':['Entity B', 'Entity C'], 'Entity C':['Entity C']}
	resultant_states2 = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 0, 0, 1]), 'Entity C':np.array([0, 1])}
	resource_limits2 = {'Entity C':1.0}
	op_performance_levels2 = {'Entity B':1.0}
	
	model2.set_and_check(entities2, ent_types2, parents2, dependencies2,
                     resultant_states2, resource_limits2, op_performance_levels2)
	try:
		model.merge_models(model2)
		assert False  # A in both models
	except ValueError:
		assert True
		
	entities2 = ['Entity B', 'Entity C']
	ent_types2 = {'Entity B':'function', 'Entity C':'resource'}
	parents2 = {'Entity B':'function', 'Entity C':'resource'}
	dependencies2 = {'Entity B':['Entity B', 'Entity C'], 'Entity C':['Entity C']}
	resultant_states2 = {'Entity B':np.array([0, 0, 0, 1]), 'Entity C':np.array([0, 1])}
	
	model2.set_and_check(entities2, ent_types2, parents2, dependencies2,
                     resultant_states2, resource_limits2, op_performance_levels2)
	model.merge_models(model2)
	for ent in ['Entity A', 'Entity B', 'Entity C']:
		assert ent in model.entities
		assert ent in model.ent_types.keys()
		assert ent in model.parents.keys()
		assert ent in model.dependencies.keys()
		assert ent in model.resultant_states.keys()
		if ent == 'Entity A' or ent == 'Entity B':
			assert ent in model.op_performance_levels.keys()
			assert model.op_performance_levels[ent] == 0.5
		else:
			assert ent in model.resource_limits.keys()
	assert model.ready()
test_gmormodel_merge_models.setup = setup
test_gmormodel_merge_models.teardown = teardown


def test_gmormodel_set_default_res_sts():
	"""
	"""
	print 'test_gmormodel_set_default_res_sts'
	
	try:
		model._set_default_res_sts('Entity C')
		assert False
	except ValueError:
		assert True
	
	model._set_default_res_sts('Entity B')
	assert lists_equal(model.resultant_states['Entity B'], [0, 0])
	assert model.res_sts_ready()
test_gmormodel_set_default_res_sts.setup = setup2
test_gmormodel_set_default_res_sts.teardown = teardown


def test_gmormodel_set_res_sts():
	"""
	"""
	print 'test_gmormodel_set_res_sts'
	
	assert not model.set_res_sts('Entity A', np.array([1, 2]))
	assert not ordered_lists_equal(model.resultant_states['Entity A'], [1, 2])

	assert not model.set_res_sts('Entity B', np.array([1, 0]))
	
	assert not model.set_res_sts('Entity A', np.array([1, 0, 0, 1]))
	assert not ordered_lists_equal(model.resultant_states['Entity A'], [1, 0, 0, 1])
	
	assert not model.set_res_sts('Entity A', ([1, 0]))
	
	assert model.set_res_sts('Entity A', np.array([1, 1]))
	assert lists_equal(model.resultant_states['Entity A'], [1, 1])
test_gmormodel_set_res_sts.setup = setup
test_gmormodel_set_res_sts.teardown = teardown


def test_gmormodel_set_op_perf_levs():
	"""
	"""
	print 'test_gmormodel_set_op_perf_levs'
	
	assert not model.set_op_perf_levs({'Entity A':0.5})
	assert not model.op_performance_levels == {'Entity A':0.5}
	
	model.entities.append('Entity B')
	model.ent_types['Entity B'] = 'resource'
	assert not model.set_op_perf_levs({'Entity A':0.5, 'Entity B':0.5})
	assert not model.op_performance_levels == {'Entity A':0.5, 'Entity B':0.5}
	
	model.ent_types['Entity B'] = 'function'
	assert model.set_op_perf_levs({'Entity A':0.5, 'Entity B':0.5})
	assert model.op_performance_levels == {'Entity A':0.5, 'Entity B':0.5}
test_gmormodel_set_op_perf_levs.setup = setup
test_gmormodel_set_op_perf_levs.teardown = teardown


def test_gmormodel_set_res_lim():
	"""
	"""
	print 'test_gmormodel_set_res_lim'
	
	# not a resource
	assert not model.set_res_lim({'Entity A':1})
	assert not model.resource_limits == {'Entity A':1}
	
	# not an entity	
	model.ent_types['Entity B'] = 'resource'
	assert not model.set_res_lim({'Entity B':1})
	assert not model.resource_limits == {'Entity B':1}
	
	# should work
	model.entities.append('Entity B')
	assert model.set_res_lim({'Entity B':1})
	assert model.resource_limits == {'Entity B':1}
	
	# negative
	assert not model.set_res_lim({'Entity B':-1})
	assert not model.resource_limits == {'Entity B':-1}
test_gmormodel_set_res_lim.setup = setup
test_gmormodel_set_res_lim.teardown = teardown


def test_gmormodel_del_entity():
	"""
	"""
	print 'test_gmormodel_del_entity'
	
	ent = 'Entity A'
	result = model.del_entity(ent)

	assert len(result) == 0
	assert ent not in model.entities
	assert ent not in model.ent_types.keys()
	assert ent not in model.dependencies.keys()
	assert ent not in model.parents.keys()
	assert ent not in model.resultant_states.keys()
	assert ent not in model.op_performance_levels.keys()
	for ent2 in model.entities:
		assert ent not in model.dependencies[ent2]
		assert len(model.resultant_states[ent2]) == 2**len(model.dependencies[ent2])
	
	ent = 'Entity C'
	result = model.del_entity(ent)

	assert len(result) == 1
	assert result[0] == 'Entity B'
	assert ent not in model.entities
	assert ent not in model.ent_types.keys()
	assert ent not in model.dependencies.keys()
	assert ent not in model.parents.keys()
	assert ent not in model.resultant_states.keys()
	assert ent not in model.resource_limits.keys()
	for ent2 in model.entities:
		assert ent not in model.dependencies[ent2]
		assert len(model.resultant_states[ent2]) == 2**len(model.dependencies[ent2])
		
	try:
		result = model.del_entity(ent)
		assert False
	except ValueError as ve:
		assert True
test_gmormodel_del_entity.setup = setup3
test_gmormodel_del_entity.teardown = teardown


def test_gmormodel_del_dep():
	"""
	"""
	print 'test_gmormodel_del_dep'
	
	assert not model.del_dep('Entity C', 'Entity A')	
	assert not model.del_dep('Entity A', 'Entity C')	
	assert not model.del_dep('Entity B', 'Entity A')
	
	assert model.del_dep('Entity B', 'Entity B')
	assert lists_equal(model.resultant_states['Entity B'], [0])
	assert not model.ready()
test_gmormodel_del_dep.setup = setup2
test_gmormodel_del_dep.teardown = teardown


def test_gmormodel__edit_ent_type():
	"""
	"""
	print 'test_gmormodel__edit_ent_type'
	
	assert not model._edit_ent_type('Entity D', 'function')
	assert not model._edit_ent_type('Entity A', 'not a type')
	assert not model._edit_ent_type('Entity A', 'function')
	assert not model._edit_ent_type('Entity B', 'resource')
	
	assert model._edit_ent_type('Entity C', 'function')
	assert model.ent_types['Entity C'] == 'function'
	assert 'Entity C' in model.op_performance_levels.keys()
	assert 'Entity C' not in model.resource_limits.keys()
	
	assert model._edit_ent_type('Entity A', 'resource')
	assert model.ent_types['Entity A'] == 'resource'
	assert 'Entity A' in model.resource_limits.keys()
	assert 'Entity A' not in model.op_performance_levels.keys()
test_gmormodel__edit_ent_type.setup = setup3
test_gmormodel__edit_ent_type.teardown = teardown


def test_gmormodel__edit_parent():
	"""
	"""
	print 'test_gmormodel__edit_parent'
	
	assert not model._edit_parent('Entity A', 'parent')
	assert not model._edit_parent('Entity A', 'function')
	
	assert model._edit_parent('Entity A', '')
	assert model.parents['Entity A'] == ''
test_gmormodel__edit_parent.setup = setup3
test_gmormodel__edit_parent.teardown = teardown


def test_gmormodel_edit_entity():
	"""
	"""
	print 'test_gmormodel_edit_entity'
	
	assert not model.edit_entity('Entity A', 'not a type', 'parent')
	assert not model.ent_types['Entity A'] == 'not a type'
	assert not model.parents['Entity A'] == 'parent'	
	
	assert model.edit_entity('Entity A', 'system', '')
	assert model.parents['Entity A'] == ''
	assert model.ent_types['Entity A'] == 'system'
	
	assert model.edit_entity('Entity A', 'not a type', 'system')
	assert model.parents['Entity A'] == 'system'	
	
	assert model.edit_entity('Entity A', 'function', 'parent')
	assert model.ent_types['Entity A'] == 'function'	
test_gmormodel_edit_entity.setup = setup
test_gmormodel_edit_entity.teardown = teardown