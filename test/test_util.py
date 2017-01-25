"""
test_util.py

__author__ = "Alison Goshulak"
__copyright__ = "Copyright 2016"
__credits__ = "David Bristow"
__maintainer__ = "David Bristow"
__status__ = "Development"
"""
import nose2
import numpy as np
import copy
from gmor.util import *
from gmor.model import GMORModel

def setup():
	"""
	set up for two models, one with four entities and one with two entities
	"""
	global model
	global model2
		
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global entities2
	global ent_types2
	global parents2
	global dependencies2
	global resultant_states2
	global resource_limits2
	global op_performance_levels2
		
	model = GMORModel()
	
	entities = ['Entity A', 'Entity B', 'Entity C', 'Entity D']
	ent_types = {'Entity A':'time', 'Entity B':'event', 'Entity C':'function', 'Entity D':'resource'}
	parents = {'Entity A':'time', 'Entity B':'event', 'Entity C':'function', 'Entity D':'resource'}
	dependencies = {'Entity A':['Entity C', 'Entity D'], 'Entity B':['Entity D'], 'Entity C':['Entity B', 'Entity C'], 'Entity D':['Entity C', 'Entity D']}
	resultant_states = {'Entity A':np.array([0, 0, 0, 1]), 'Entity B':np.array([0, 1]), 'Entity C':np.array([0, 0, 0, 1]), 'Entity D':np.array([0, 0, 0, 1])}
	resource_limits = {'Entity D':1.0}
	op_performance_levels = {'Entity C':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)
	
	model2 = GMORModel()
	
	entities2 = ['Entity E', 'Entity F']
	ent_types2 = {'Entity E':'function', 'Entity F':'resource'}
	parents2 = {'Entity E':'function', 'Entity F':'resource'}
	dependencies2 = {'Entity E':['Entity F'], 'Entity F':['Entity F']}
	resultant_states2 = {'Entity E':np.array([0, 1]), 'Entity F':np.array([0, 1])}
	resource_limits2 = {'Entity F':1.0}
	op_performance_levels2 = {'Entity E':1.0}
	
	model2.set_and_check(entities2, ent_types2, parents2, dependencies2, resultant_states2,
	                            resource_limits2, op_performance_levels2)

def teardown():
	model = GMORModel()
	model2 = GMORModel()

def test_lists_equal():
	print 'test_lists_equal'
	
	assert lists_equal([1, 2.0, 3], [3.0, 2, 1])
	assert lists_equal([1, 2, 3, 4], np.array([1, 2, 3, 4]))
	assert lists_equal(['A', 'B', 'C'], ['B', 'C', 'A'])
	assert not lists_equal([1, 2], [1, 2, 2, 2])
	assert not lists_equal([4, 3, 2, 1], [4, 3, 2, 2])
	
def test_sts_lists_equal():
	print 'test_sts_lists_equal'
	
	assert ordered_lists_equal(resultant_states['Entity A'], [0, 0, 0, 1])
	assert not ordered_lists_equal(resultant_states['Entity A'], [1, 0, 0, 0]) # wrong order
	assert not ordered_lists_equal(resultant_states['Entity B'], [0, 0, 0, 1]) # wrong length
test_sts_lists_equal.setup = setup
test_sts_lists_equal.teardown = teardown

def test_get_curr_int_states():
	print 'test_get_curr_int_states'
	
	ents_to_do = {'A':1, 'B':0}
	defaults = {'A':2, 'B':1}
	results = get_curr_int_states(ents_to_do, defaults)
	assert len(results) == 2
	assert ordered_lists_equal(results[0].values(), [0, 1])
	assert lists_equal(results[1].values(), [1, 1])
	
	ents_to_do = {'A':1, 'B':0, 'C':1}
	defaults = {'A':2, 'B':0, 'C':2}
	results = get_curr_int_states(ents_to_do, defaults)
	assert len(results) == 4
	assert lists_equal(results[0].values(), [0, 0, 0])
	assert results[1] == {'A':0, 'B':0, 'C':1}
	assert results[2] == {'A':1, 'B':0, 'C':0}
	assert results[3] == {'A':1, 'B':0, 'C':1}
	
def test_update_res_sts_after_treatment():
	print 'test_update_res_sts_after_treatment'
	
	new_model = copy.deepcopy(model)
	new_model.dependencies['Entity A'].insert(0, 'Entity B')
	update_res_sts_after_treatment(new_model, 'Entity A', 'Entity C')
	assert ordered_lists_equal(new_model.resultant_states['Entity A'], [0, 0, 0, 0, 0, 1, 1, 1])
	
	new_model = copy.deepcopy(model)
	new_model.dependencies['Entity A'].insert(0, 'Entity B')
	update_res_sts_after_treatment(new_model, 'Entity A', 'Entity D')
	assert ordered_lists_equal(new_model.resultant_states['Entity A'], [0, 0, 0, 1, 0, 0, 1, 1])
	
	new_model = copy.deepcopy(model)
	new_model.dependencies['Entity A'].insert(0, 'Entity B')
	new_model.resultant_states['Entity A'] = np.array([0, 1, 0, 0]) # => C AND (NOT D)
	update_res_sts_after_treatment(new_model, 'Entity A', 'Entity C')
	assert ordered_lists_equal(new_model.resultant_states['Entity A'], [0, 1, 1, 1, 0, 0, 0, 0]) # => (C OR B) AND (NOT D)
	
	new_model = copy.deepcopy(model)
	new_model.dependencies['Entity A'] = ['Entity B', 'Entity A', 'Entity C', 'Entity D']
	new_model.resultant_states['Entity A'] = np.array([0, 0, 0, 1, 0, 0, 1, 1]) # => (A OR D) AND C
	update_res_sts_after_treatment(new_model, 'Entity A', 'Entity A')
	assert ordered_lists_equal(new_model.resultant_states['Entity A'], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]) # => ((B OR A) OR D) AND C
test_update_res_sts_after_treatment.setup = setup
test_update_res_sts_after_treatment.teardown = teardown

def test_add_redundancy():
	print 'test_add_redundancy'
	
	try:
		add_redundancy(model, 'Entity X')
		assert False
	except ValueError:
		assert True
		
	try:
		add_redundancy(model, 'Entity A')
		assert False
	except ValueError:
		assert True
		
	try:
		add_redundancy(model, 'Entity B')
		assert False
	except ValueError:
		assert True
	
	new_model = add_redundancy(model, 'Entity D', suffix=' test')
	new_ent = 'Entity D test'
	assert new_ent in new_model.entities
	assert new_model.ent_types[new_ent] == ent_types['Entity D']
	assert new_model.parents[new_ent] == parents['Entity D']
	assert lists_equal(new_model.dependencies[new_ent], ['Entity C', new_ent])
	assert ordered_lists_equal(new_model.resultant_states[new_ent], resultant_states['Entity D'])
	assert new_model.resource_limits[new_ent] == resource_limits['Entity D']
	assert new_ent in new_model.dependencies['Entity A']
	assert ordered_lists_equal(new_model.resultant_states['Entity A'], [0, 0, 0, 1, 0, 0, 1, 1])
	assert new_ent in new_model.dependencies['Entity B']
	assert ordered_lists_equal(new_model.resultant_states['Entity B'], [0, 1, 1, 1])
	assert new_ent not in new_model.dependencies['Entity D']
	
	model_copy = copy.deepcopy(model)
	new_model = add_redundancy(model_copy, 'Entity C', select=['Entity B', 'Entity C', 'Entity D'], weight=0.3)
	del model_copy  # check that deep copy of model_copy inserted in new_model
	new_ent = 'Entity C red'
	assert new_ent not in new_model.dependencies['Entity A']  # A not in select
	assert new_ent not in new_model.dependencies['Entity B']  # B not dependent on C
	assert new_ent not in new_model.dependencies['Entity C']  # new ent dependent on itself instead of C
	assert new_ent in new_model.dependencies['Entity D']
	assert new_model.op_performance_levels['Entity C'] == 0.3
	assert new_model.op_performance_levels[new_ent] == 0.7
test_add_redundancy.setup = setup
test_add_redundancy.teardown = teardown

def test_add_flexibility():
	print 'test_add_flexibility'
	
	try:
		add_flexibility(model, 'Entity X', 'Entity C')
		assert False
	except ValueError:
		assert True
		
	try:
		add_flexibility(model, 'Entity C', 'Entity X')
		assert False
	except ValueError:
		assert True
		
	try:
		add_flexibility(model, 'Entity A', 'Entity C')
		assert False
	except ValueError:
		assert True
		
	try:
		add_flexibility(model, 'Entity B', 'Entity C')
		assert False
	except ValueError:
		assert True
	
	new_dep = 'Entity C'	
	new_model = add_flexibility(model, 'Entity D', new_dep)	
	for ent in ['Entity A', new_dep, 'Entity D']:
		assert len(new_model.dependencies[ent]) == 2  # C should only show once in dependencies
	assert new_dep in new_model.dependencies['Entity B']
	assert ordered_lists_equal(new_model.resultant_states['Entity B'], [0, 1, 1, 1])
	
	res_ent = 'Entity E'
	model.entities.append(res_ent)
	model.ent_types[res_ent] = 'resource'
	model.dependencies[res_ent] = ['Entity C']
	model.resultant_states[res_ent] = np.array([0, 1])
	new_res_dep = 'Entity D'
	model_copy = copy.deepcopy(model)
	new_model = add_flexibility(model_copy, 'Entity C', new_res_dep, select=['Entity A', 'Entity B', 'Entity E'])
	del model_copy  # check that deep copy of model_copy inserted in new_model
	assert len(new_model.dependencies['Entity A']) == 2  # D should only show once in dependencies
	assert len(new_model.dependencies['Entity B']) == 1  # C not a dependency of B
	assert new_res_dep not in new_model.dependencies[res_ent]  # resource cannot depend on another resource
test_add_flexibility.setup = setup
test_add_flexibility.teardown = teardown

def test_add_diversity():
	print 'test_add_diversity'
	
	try:
		add_diversity(model, model2, 'Entity X', 'Entity E')
		assert False
	except ValueError:
		assert True
		
	try:
		add_diversity(model, model2, 'Entity C', 'Entity X')
		assert False
	except ValueError:
		assert True
		
	try:
		add_diversity(model, model2, 'Entity A', 'Entity E')
		assert False
	except ValueError:
		assert True
		
	try:
		add_diversity(model, model2, 'Entity B', 'Entity E')
		assert False
	except ValueError:
		assert True
		
	new_dep = 'Entity E'	
	new_model = add_diversity(model, model2, 'Entity D', new_dep)	
	assert new_dep in new_model.dependencies['Entity A']
	assert ordered_lists_equal(new_model.resultant_states['Entity A'], [0, 0, 0, 1, 0, 0, 1, 1])
	assert new_dep in new_model.dependencies['Entity B']
	assert ordered_lists_equal(new_model.resultant_states['Entity B'], [0, 1, 1, 1])
	assert new_dep not in new_model.dependencies['Entity D']
	assert 'Entity F' in new_model.entities
	
	new_res_dep = 'Entity F'
	model_copy = copy.deepcopy(model)
	model2_copy = copy.deepcopy(model2)
	new_model = add_diversity(model_copy, model2_copy, 'Entity C', new_res_dep, select=['Entity B', 'Entity D'])
	del model_copy  # check that deep copy of model_copy inserted in new_model
	del model2_copy  # check that deep copy of model2_copy merged into new_model
	assert new_res_dep not in new_model.dependencies['Entity B']  # C not a dependency of B
	assert new_res_dep not in new_model.dependencies['Entity D']  # resource can't depend on another resource
test_add_diversity.setup = setup
test_add_diversity.teardown = teardown

def test_add_dispersion():
	print 'test_add_dispersion'
	
	try:
		add_dispersion(model, model2, ['Entity E', 'Entity F'])
		assert False
	except ValueError:
		assert True
		
	try:
		add_dispersion(model, model2, ['Entity A', 'Entity B'])
		assert False
	except ValueError:
		assert True
		
	dis_model = GMORModel()
	
	ents = ['Entity A', 'Entity B', 'Entity E']
	types = {'Entity A':'time', 'Entity B':'event', 'Entity E':'function'}
	pts = {'Entity A':'time', 'Entity B':'event', 'Entity E':'function'}
	deps = {'Entity A':['Entity E'], 'Entity B':['Entity E'], 'Entity E':['Entity E']}
	res_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 1]), 'Entity E':np.array([0, 1])}
	res_limits = {}
	op_perf_levels = {'Entity E':1.0}
	
	dis_model.set_and_check(ents, types, pts, deps, res_states, res_limits, op_perf_levels)
	dis_ents = ['Entity A', 'Entity B']	
	model_copy = copy.deepcopy(model)
	new_model = add_dispersion(model, dis_model, dis_ents)
	del model_copy  # check that deep copy of model_copy inserted in new_model
	del dis_model  # check that deep copy of dis_model merged into new_model
	
	assert new_model.ready()
	for ent in (model.entities + ['Entity E']): assert ent in new_model.entities
	for ent in ents: assert lists_equal(new_model.dependencies[ent], ['Entity E'])
	assert ordered_lists_equal(new_model.resultant_states['Entity A'], res_states['Entity A'])
	assert lists_equal(new_model.dependencies['Entity C'], dependencies['Entity C'])
	assert lists_equal(new_model.dependencies['Entity D'], dependencies['Entity D'])
test_add_dispersion.setup = setup
test_add_dispersion.teardown = teardown