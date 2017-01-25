"""
test_gmorscenariomodel.py

__author__ = "Alison Goshulak"
__copyright__ = "Copyright 2016"
__credits__ = "David Bristow"
__maintainer__ = "David Bristow"
__status__ = "Development"
"""
#pylint: disable=trailing-whitespace
#pylint: disable=global-variable-undefined
#from nose2.tools import *
import nose2
from gmor.model import *
#from gmor.util import lists_equal, ordered_lists_equal
#from gmor.model import GMORModel #import gmor
#from gmor.model import GMORRunner
import numpy as np

def setup_gmormodel():
	"""
	setup for single entity GMORModel without initialization of GMORScenarioModel
	(for testing init method)
	"""
	#print "SETUP!"
	global model
	global scenario_model

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
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)
	
def setup():
	"""
	setup for two entity GMORModel and corresponding GMORScenarioModel
	"""
	#print "SETUP!"
	global model
	global scenario_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_exits
	global realized_timelines
	global efforts
	global deadlines
	
	model = GMORModel()
	
	entities = ['Entity A', 'Entity B']
	ent_types = {'Entity A':'function', 'Entity B':'system'}
	parents = {'Entity A':'function', 'Entity B':'system'}
	dependencies = {'Entity A':['Entity B'], 'Entity B':['Entity B']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 1])}
	resource_limits = {}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)

	scenario_model = GMORScenarioModel(model, 'test')
	deadlines = {'Entity A':1.0}
	scenario_model.deadlines = deadlines
	
	current_internal_states = scenario_model.current_internal_states
	realized_exits = scenario_model.realized_exits
	realized_timelines = scenario_model.realized_timelines
	efforts = scenario_model.efforts
		
def setup2():
	"""
	setup for three entity GMORModel and corresponding GMORScenarioModel
	with second entity having 3 dependencies
	"""
	#print "SETUP!"
	global model
	global scenario_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_exits
	global realized_timelines
	global efforts
	global deadlines
	
	model = GMORModel()
	
	entities = ['Entity A', 'Entity B', 'Entity C']
	ent_types = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	parents = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	dependencies = {'Entity A':['Entity B'], 'Entity B':['Entity B','Entity A', 'Entity C'], 'Entity C':['Entity C']}
	resultant_states = {'Entity A':np.array([0, 0]), 'Entity B':np.array([0, 0, 0, 1, 1, 0, 1, 0]), 'Entity C':np.array([1, 1])}
	resource_limits = {'Entity C':1.0}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)

	scenario_model = GMORScenarioModel(model, 'test')
	deadlines = {'Entity A':1.0}
	scenario_model.deadlines = deadlines
	
	current_internal_states = scenario_model.current_internal_states
	realized_exits = scenario_model.realized_exits
	realized_timelines = scenario_model.realized_timelines
	efforts = scenario_model.efforts

def setup3():
	"""
	setup for four entity GMORModel and corresponding GMORScenarioModel
	with second entity having 4 dependencies and third entity having 2 dependencies
	"""
	#print "SETUP!"
	global model
	global scenario_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_exits
	global realized_timelines
	global efforts
	global deadlines
	
	model = GMORModel()
	
	entities = ['Entity A', 'Entity B', 'Entity C', 'Entity D']
	ent_types = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource', 'Entity D':'resource'}
	parents = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource', 'Entity D':'resource'}
	dependencies = {'Entity A':['Entity B'], 'Entity B':['Entity B','Entity A', 'Entity C', 'Entity D'],
	                'Entity C':['Entity C', 'Entity B'], 'Entity D':['Entity A']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0]),
                    	'Entity C':np.array([0, 1, 0, 1]), 'Entity D':np.array([1, 0])}
	resource_limits = {'Entity C':1.0, 'Entity D':1.0}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)

	scenario_model = GMORScenarioModel(model, 'test')
	deadlines = {'Entity A':1.0}
	scenario_model.deadlines = deadlines
	
	current_internal_states = scenario_model.current_internal_states
	realized_exits = scenario_model.realized_exits
	realized_timelines = scenario_model.realized_timelines
	efforts = scenario_model.efforts
	
def teardown():
	"""
	teardown
	"""
	#print "TEAR DOWN!"
	model = GMORModel()
		
def test_gmorscenariomodel_init():
	"""
	test_gmorscenariomodel_init
	"""
	print 'test_gmorscenariomodel_init'
	
	try:
		scenario_model = GMORScenarioModel(model, 'test')
		assert scenario_model.ready()
	except ValueError:
		assert False
	
	assert scenario_model.name == 'test'
	
	model_not_ready = GMORModel()
	
	try:
		scenario_model = GMORScenarioModel(model_not_ready, 'error')
		assert False
	except ValueError:
		assert True
test_gmorscenariomodel_init.setup = setup_gmormodel
test_gmorscenariomodel_init.teardown = teardown

def test_gmorscenariomodel_reset():
	"""
	test_gmorscenariomodel_reset
	"""
	print 'test_gmorscenariomodel_reset'
	
	# adjust model
	model.add_entity('Entity D', 'function', parent='function')
	model.add_dep('Entity D', 'Entity C')
	model.del_entity('Entity A')
	
	scenario_model.reset(model)
	
	current_internal_states = scenario_model.current_internal_states
	realized_exits = scenario_model.realized_exits
	realized_timelines = scenario_model.realized_timelines
	efforts = scenario_model.efforts
	deadlines = scenario_model.deadlines
	
	assert current_internal_states == {'Entity B':1, 'Entity C':1}
	assert realized_exits == {'Entity B':-1, 'Entity C':-1}
	assert realized_timelines == {'Entity B':0, 'Entity C':0, 'Entity D':0}
	assert efforts == {'Entity B':{'Entity C':0}, 'Entity D':{'Entity C':0}}
	assert deadlines == {'Entity D':0}
		
	assert scenario_model.ready()		
test_gmorscenariomodel_reset.setup = setup2
test_gmorscenariomodel_reset.teardown = teardown

def test_gmorscenariomodel_set_and_check():
	"""
	test_gmorscenariomodel_set_and_check
	"""
	print 'test_gmorscenariomodel_set_and_check'
	
	result = scenario_model.set_and_check(model, current_internal_states,
					              realized_timelines, realized_exits, efforts, deadlines)
	assert result
	
	not_ready = {'Error': -2}  # invalid for all class variables
	
	result = scenario_model.set_and_check(model, not_ready, not_ready, not_ready, not_ready, not_ready)
	assert not result	
test_gmorscenariomodel_set_and_check.setup = setup
test_gmorscenariomodel_set_and_check.teardown = teardown

def test_gmorscenariomodel_set():
	"""
	test_gmorscenariomodel_set
	"""
	print 'test_gmorscenariomodel_set'

	set_test = {'Entity T': 'test'}
	
	scenario_model.set(model, set_test, set_test, set_test, set_test, set_test)
	
	assert scenario_model.current_internal_states['Entity T'] == 'test'
	assert scenario_model.realized_timelines['Entity T'] == 'test'
	assert scenario_model.realized_exits['Entity T'] == 'test'
	assert scenario_model.efforts['Entity T'] == 'test'
	assert scenario_model.deadlines['Entity T'] == 'test'

	model_not_ready = GMORModel()
	
	try:
		scenario_model.set(model_not_ready, current_internal_states,
					              realized_timelines, realized_exits, efforts, deadlines)
		assert False
	except ValueError:
		assert True		
test_gmorscenariomodel_set.setup = setup
test_gmorscenariomodel_set.teardown = teardown

def test_gmorscenariomodel_valid_states():
	"""
	test_gmorscenariomodel_valid_states
	"""
	print 'test_gmorscenariomodel_valid_states'
	
	# valid
	assert scenario_model.valid_states([0, 0, 0])
	assert scenario_model.valid_states([1, 1, 1])
	assert scenario_model.valid_states([1, 0, 1, 0])

	# invalid	
	assert not scenario_model.valid_states([])
	assert not scenario_model.valid_states([1, 0, 2])
	assert not scenario_model.valid_states(['zero', 'one'])
test_gmorscenariomodel_valid_states.setup = setup
test_gmorscenariomodel_valid_states.teardown = teardown
	
def test_gmorscenariomodel_valid_internal_states():
	"""
	test_gmorscenariomodel_valid_internal_states
	"""
	print 'test_gmorscenariomodel_valid_internal_states'
	
	assert scenario_model.valid_internal_states(current_internal_states)
	
	not_ents = {'Entity X':0, 'Entity Y':0}  # not entities in model
	assert not scenario_model.valid_internal_states(not_ents)
	try:
		scenario_model.valid_internal_states(not_ents, verbose=True)
		assert False
	except ValueError:
		assert True
		
	invalid_state = {'Entity B':1, 'Entity C':-1}  # -1 invalid state
	assert not scenario_model.valid_internal_states(invalid_state)
	try:
		scenario_model.valid_internal_states(invalid_state, verbose=True)
		assert False
	except ValueError:
		assert True
		
	not_int_dep = {'Entity B':1, 'Entity A': 1, 'Entity C':1}  # Entity A has no internal dependence
	assert not scenario_model.valid_internal_states(not_int_dep)
	try:
		scenario_model.valid_internal_states(not_int_dep, verbose=True)
		assert False
	except ValueError:
		assert True
		
	assert not scenario_model.valid_internal_states({})  # model has two internally-dependent entities
test_gmorscenariomodel_valid_internal_states.setup = setup2
test_gmorscenariomodel_valid_internal_states.teardown = teardown
	
def test_gmorscenariomodel_valid_realized_timelines():
	"""
	test_gmorscenariomodel_valid_realized_timelines
	"""
	print 'test_gmorscenariomodel_valid_realized_timelines'
	
	assert scenario_model.valid_realized_timelines(realized_timelines)
	
	not_ents = {'Entity X':0, 'Entity Y':0, 'Entity Z':0}  # not entities in model
	assert not scenario_model.valid_realized_timelines(not_ents)
	try:
		scenario_model.valid_realized_timelines(not_ents, verbose=True)
		assert False
	except ValueError:
		assert True
	
	invalid_timeline = {'Entity A':1, 'Entity B':1, 'Entity C':-1}  # negative time line invalid
	assert not scenario_model.valid_realized_timelines(invalid_timeline)
	try:
		scenario_model.valid_realized_timelines(invalid_timeline, verbose=True)
		assert False
	except ValueError:
		assert True
		
	missing_ent = {'Entity A':1, 'Entity C':1}  # missing Entity B
	assert not scenario_model.valid_realized_timelines(missing_ent)
	try:
		scenario_model.valid_realized_timelines(missing_ent, verbose=True)
		assert False
	except ValueError:
		assert True
test_gmorscenariomodel_valid_realized_timelines.setup = setup2
test_gmorscenariomodel_valid_realized_timelines.teardown = teardown
	
def test_gmorscenariomodel_valid_efforts():
	"""
	test_gmorscenariomodel_valid_efforts
	"""
	print 'test_gmorscenariomodel_valid_efforts'
	
	assert scenario_model.valid_efforts(efforts)
	
	assert scenario_model.valid_efforts({})
	
	not_ents = {'Entity X':{}, 'Entity Y':{}}  # not entities in model
	assert not scenario_model.valid_efforts(not_ents)
	try:
		scenario_model.valid_efforts(not_ents, verbose=True)
		assert False
	except ValueError:
		assert True
	
	not_dep = {'Entity A':{'Entity C':0}}  # Entity C not a dependency of Entity A
	assert not scenario_model.valid_efforts(not_dep)
	try:
		scenario_model.valid_efforts(not_dep, verbose=True)
		assert False
	except ValueError:
		assert True
		
	ent_a_res = {'Entity C':{'Entity D':0}}  # Entity C is a resource
	assert not scenario_model.valid_efforts(ent_a_res)
	try:
		scenario_model.valid_efforts(ent_a_res, verbose=True)
		assert False
	except ValueError:
		assert True
		
	dep_not_ent = {'Entity B':{'Entity X':0}}  # Entity X does not exist in model
	assert not scenario_model.valid_efforts(dep_not_ent)
	
	dep_not_res = {'Entity B':{'Entity A':0}}  # Entity A not a resource
	assert not scenario_model.valid_efforts(dep_not_res)
	try:
		scenario_model.valid_efforts(dep_not_res, verbose=True)
		assert False
	except ValueError:
		assert True
		
	invalid_effort = {'Entity B':{'Entity C':-1, 'Entity D':0}}  # negative effort invalid
	assert not scenario_model.valid_efforts(invalid_effort)
	try:
		scenario_model.valid_efforts(invalid_effort, verbose=True)
		assert False
	except ValueError:
		assert True
test_gmorscenariomodel_valid_efforts.setup = setup3
test_gmorscenariomodel_valid_efforts.teardown = teardown

def test_gmorscenariomodel__valid_realized_exits():
	"""
	test_gmorscenariomodel__valid_realized_exits
	"""
	print 'test_gmorscenariomodel__valid_realized_exits'
	
	valid_exits = {'Entity B':-1, 'Entity C':0}
	assert scenario_model._valid_realized_exits(valid_exits)
	
	assert scenario_model._valid_realized_exits({})
	
	not_ents = {'Entity X':0, 'Entity Y':0}  # not entities in model
	assert not scenario_model._valid_realized_exits(not_ents)
	try:
		scenario_model._valid_realized_exits(not_ents, verbose=True)
		assert False
	except ValueError:
		assert True
		
	invalid_exit = {'Entity B':-0.5, 'Entity C':0}  # invalid value between -1 and 0
	assert not scenario_model._valid_realized_exits(invalid_exit)
	try:
		scenario_model._valid_realized_exits(invalid_exit, verbose=True)
		assert False
	except ValueError:
		assert True
		
	invalid_exit = {'Entity B':0, 'Entity C':-100}  # invalid value < -1
	assert not scenario_model._valid_realized_exits(invalid_exit)
	try:
		scenario_model._valid_realized_exits(invalid_exit, verbose=True)
		assert False
	except ValueError:
		assert True
		
	not_int_dep = {'Entity B':1, 'Entity A': 1, 'Entity C': 1}  # Entity A has no internal dependence
	assert not scenario_model._valid_realized_exits(not_int_dep)
	try:
		scenario_model._valid_realized_exits(not_int_dep, verbose=True)
		assert False
	except ValueError:
		assert True
test_gmorscenariomodel__valid_realized_exits.setup = setup3
test_gmorscenariomodel__valid_realized_exits.teardown = teardown	

def test_gmorscenariomodel_valid_deadlines():
	"""
	test_gmorscenariomodel_valid_deadlines
	"""
	print 'test_gmorscenariomodel_valid_deadlines'
	assert scenario_model.valid_deadlines(deadlines)
	
	invalid_dead = {'Entity A':-1}
	assert not scenario_model.valid_deadlines(invalid_dead)  # negative deadline
	try:
		scenario_model.valid_deadlines(invalid_dead, verbose=True)
		assert False
	except ValueError:
		assert True
	
	assert not scenario_model.valid_deadlines({'Entity X':1.0})  # not an entity
	try:
		scenario_model.valid_deadlines({'Entity X':1.0}, verbose=True)
		assert False
	except ValueError:
		assert True
		
	assert not scenario_model.valid_deadlines({})  # no deadlines
	try:
		scenario_model.valid_deadlines({}, verbose=True)
		assert False
	except ValueError:
		assert True
test_gmorscenariomodel_valid_deadlines.setup = setup
test_gmorscenariomodel_valid_deadlines.teardown = teardown

def test_gmorscenariomodel_cur_int_st_ready():
	"""
	test_gmorscenariomodel_cur_int_st_ready
	"""
	print 'test_gmorscenariomodel_cur_int_st_ready'
	
	assert scenario_model.cur_int_st_ready()
	
	scenario_model.current_internal_states = {}
	
	assert not scenario_model.cur_int_st_ready()  # should never be empty
test_gmorscenariomodel_cur_int_st_ready.setup = setup
test_gmorscenariomodel_cur_int_st_ready.teardown = teardown

def test_gmorscenariomodel_rlzd_time_ready():
	"""
	test_gmorscenariomodel_rlzd_time_ready
	"""
	print 'test_gmorscenariomodel_rlzd_time_ready'
	
	assert scenario_model.rlzd_time_ready()
	
	scenario_model.realized_timelines = {}
	
	assert not scenario_model.rlzd_time_ready()  # should never be empty
test_gmorscenariomodel_rlzd_time_ready.setup = setup
test_gmorscenariomodel_rlzd_time_ready.teardown = teardown

def test_gmorscenariomodel_rlzd_ex_ready():
	"""
	test_gmorscenariomodel_rlzd_ex_ready
	"""
	print 'test_gmorscenariomodel_rlzd_ex_ready'
	
	assert scenario_model.rlzd_ex_ready()
	
	scenario_model.realized_exits = {'Entity X':1}
	
	assert not scenario_model.rlzd_ex_ready()
test_gmorscenariomodel_rlzd_ex_ready.setup = setup
test_gmorscenariomodel_rlzd_ex_ready.teardown = teardown

def test_gmorscenariomodel_eff_ready():
	"""
	test_gmorscenariomodel_eff_ready
	"""
	print 'test_gmorscenariomodel_eff_ready'
	
	assert scenario_model.eff_ready()
	
	scenario_model.efforts = {'Entity A':{'Entity X':1}}
	assert not scenario_model.eff_ready()
test_gmorscenariomodel_eff_ready.setup = setup2
test_gmorscenariomodel_eff_ready.teardown = teardown

def test_gmorscenariomodel_deads_ready():
	"""
	test_gmorscenariomodel_deads_ready
	"""
	print 'test_gmorscenariomodel_deads_ready'
	
	assert scenario_model.deads_ready()
	
	scenario_model.deadlines = {}
	assert not scenario_model.deads_ready()
test_gmorscenariomodel_deads_ready.setup = setup
test_gmorscenariomodel_deads_ready.teardown = teardown

def test_gmorscenariomodel_ready():
	"""
	test_gmorscenariomodel_ready
	"""
	print 'test_gmorscenariomodel_ready'
	
	assert scenario_model.ready()
	
	scenario_model.current_internal_states = {}
	scenario_model.realized_timelines = {}
	scenario_model.realized_exits = {'Entity X':1}
	scenario_model.efforts = {'Entity A':{'Entity B':2}}  # Entity B is not a resource
	
	assert not scenario_model.ready()
test_gmorscenariomodel_ready.setup = setup
test_gmorscenariomodel_ready.teardown = teardown

def test_gmorscenariomodel_set_current_internal_states():
	"""
	test_gmorscenariomodel_set_current_internal_states
	"""
	print 'test_gmorscenariomodel_set_current_internal_states'
	
	assert scenario_model.current_internal_states == {'Entity B':1, 'Entity C':1}	
	new_internal_states = {'Entity B':0, 'Entity C':0}
	assert scenario_model.set_current_internal_states(new_internal_states)
	assert scenario_model.current_internal_states == new_internal_states

	invalid_internal_state = {'Entity B':-1, 'Entity C':1}
	assert not scenario_model.set_current_internal_states(invalid_internal_state)
	assert not scenario_model.current_internal_states['Entity B'] == -1
	assert not scenario_model.current_internal_states['Entity C'] == 1
test_gmorscenariomodel_set_current_internal_states.setup = setup2
test_gmorscenariomodel_set_current_internal_states.teardown = teardown
	
def test_gmorscenariomodel_set_realized_timelines():
	"""
	test_gmorscenariomodel_set_realized_timelines
	"""
	print 'test_gmorscenariomodel_set_realized_timelines'

	assert scenario_model.realized_timelines == {'Entity A':0, 'Entity B':0}	
	new_realized_timelines = {'Entity A':50, 'Entity B':100}
	assert scenario_model.set_realized_timelines(new_realized_timelines)
	assert scenario_model.realized_timelines == new_realized_timelines

	invalid_realized_timeline = {'Entity A':0, 'Entity B':-1}
	assert not scenario_model.set_realized_timelines(invalid_realized_timeline)
	assert not scenario_model.realized_timelines['Entity B'] == -1
test_gmorscenariomodel_set_realized_timelines.setup = setup
test_gmorscenariomodel_set_realized_timelines.teardown = teardown
	
def test_gmorscenariomodel_set_realized_exit_by_ent():
	"""
	test_gmorscenariomodel_set_realized_exit_by_ent
	"""
	print 'test_gmorscenariomodel_set_realized_exit_by_ent'
	
	assert scenario_model.realized_exits['Entity B'] == -1
	assert scenario_model.set_realized_exit_by_ent('Entity B', 50)
	assert scenario_model.realized_exits['Entity B'] == 50
	
	not_ent = 'Entity Z'
	assert not scenario_model.set_realized_exit_by_ent(not_ent, -1)  # not an entity of model
	assert not_ent not in scenario_model.realized_exits
	try:
		scenario_model.set_realized_exit_by_ent(not_ent, -1, verbose=True)
		assert False
	except ValueError:
		assert True
	
	not_int_dep = 'Entity A'
	assert not scenario_model.set_realized_exit_by_ent(not_int_dep, -1)  # Entity A has no internal dependence
	assert not_int_dep not in scenario_model.realized_exits
	try:
		scenario_model.set_realized_exit_by_ent(not_int_dep, -1, verbose=True)
		assert False
	except ValueError:
		assert True
	
	assert not scenario_model.set_realized_exit_by_ent('Entity B', -50)  # exit can't be < -1
	assert not scenario_model.realized_exits['Entity B'] == -50
	try:
		scenario_model.set_realized_exit_by_ent('Entity B', -50, verbose=True)
		assert False
	except ValueError:
		assert True
	
	assert not scenario_model.set_realized_exit_by_ent('Entity B', -0.5)  # exit can't be between -1 and 0
	assert not scenario_model.realized_exits['Entity B'] == -0.5
	try:
		scenario_model.set_realized_exit_by_ent('Entity B', -0.5, verbose=True)
		assert False
	except ValueError:
		assert True
test_gmorscenariomodel_set_realized_exit_by_ent.setup = setup
test_gmorscenariomodel_set_realized_exit_by_ent.teardown = teardown	
	
def test_gmorscenariomodel_set_realized_exits():
	"""
	test_gmorscenariomodel_set_realized_exits
	"""
	print 'test_gmorscenariomodel_set_realized_exits'
	
	assert scenario_model.realized_exits == {'Entity B':-1, 'Entity C':-1}
	new_realized_exits = {'Entity B':50, 'Entity C':100}
	assert scenario_model.set_realized_exits(new_realized_exits)
	assert scenario_model.realized_exits == new_realized_exits

	invalid_realized_exit = {'Entity B':-50, 'Entity C':-1}
	assert not scenario_model.set_realized_exits(invalid_realized_exit)
	assert not scenario_model.realized_exits['Entity B'] == -50
test_gmorscenariomodel_set_realized_exits.setup = setup2
test_gmorscenariomodel_set_realized_exits.teardown = teardown

def test_gmorscenariomodel_set_effort_by_resource():
	"""
	test_gmorscenariomodel_set_effort_by_resource
	"""
	print 'test_gmorscenariomodel_set_effort_by_resource'
	
	assert scenario_model.efforts['Entity B']['Entity D'] == 0
	new_efforts = {'Entity B':1}
	assert scenario_model.set_effort_by_resource(new_efforts, 'Entity D')
	assert scenario_model.valid_efforts(scenario_model.efforts)
	assert scenario_model.efforts['Entity B']['Entity D'] == 1
	
	not_ents = {'Entity X':0, 'Entity Y':0}  # not entities of the model
	assert not scenario_model.set_effort_by_resource(not_ents, 'Entity D')
	try:
		scenario_model.set_effort_by_resource(not_ents, 'Entity D', verbose=True)
		assert False
	except ValueError:
		assert True
		
	assert not scenario_model.set_effort_by_resource(new_efforts, 'Entity A')  # Entity A not a resource
	try:
		scenario_model.set_effort_by_resource(new_efforts, 'Entity A', verbose=True)
		assert False
	except ValueError:
		assert True
		
	assert not scenario_model.set_effort_by_resource(new_efforts, 'Entity Z')  # Entity Z not an entity
	try:
		scenario_model.set_effort_by_resource(new_efforts, 'Entity Z', verbose=True)
		assert False
	except ValueError:
		assert True
		
	ent_a_res = {'Entity B':1, 'Entity C':2}  # resource can't use itself
	assert not scenario_model.set_effort_by_resource(ent_a_res, 'Entity C')
	try:
		scenario_model.set_effort_by_resource(ent_a_res, 'Entity C', verbose=True)
		assert False
	except ValueError:
		assert True
		
	not_dep = {'Entity A':1, 'Entity B':2}
	assert not scenario_model.set_effort_by_resource(not_dep, 'Entity D')  # Entity D not a dependency of Entity A
	try:
		scenario_model.set_effort_by_resource(not_dep, 'Entity D', verbose=True)
		assert False
	except ValueError:
		assert True
		
	invalid_effort = {'Entity B':-1}
	assert not scenario_model.set_effort_by_resource(invalid_effort, 'Entity D')  # efforts must be >= 0
	try:
		scenario_model.set_effort_by_resource(invalid_effort, 'Entity D', verbose=True)
		assert False
	except ValueError:
		assert True
test_gmorscenariomodel_set_effort_by_resource.setup = setup3
test_gmorscenariomodel_set_effort_by_resource.teardown = teardown

def test_gmorscenariomodel_set_deadlines():
	"""
	"""
	print 'test_gmorscenariomodel_set_deadlines'
			
	assert not scenario_model.set_deadlines({'Entity A':-1.0})
	assert not scenario_model.deadlines == {'Entity A':-1.0}
			
	assert scenario_model.set_deadlines({'Entity A':5.0})
	assert scenario_model.deadlines == {'Entity A':5.0}
test_gmorscenariomodel_set_deadlines.setup = setup
test_gmorscenariomodel_set_deadlines.teardown = teardown

def test_gmorscenariomodel_set_new_scen_model():
	"""
	same model
	"""
	print 'test_gmorscenariomodel_set_new_scen_model'
	
	current_internal_states = {'Entity B':0, 'Entity C':0}
	realized_exits = {'Entity B':1, 'Entity C':2}
	realized_timelines = {'Entity A':1, 'Entity B':2, 'Entity C':3, 'Entity D':4}
	efforts = {'Entity B':{'Entity C':1, 'Entity D':2}}
	deadlines = {'Entity A':1}
	
	scenario_model.set_current_internal_states(current_internal_states)
	scenario_model.set_realized_exits(realized_exits)
	scenario_model.set_realized_timelines(realized_timelines)
	scenario_model.set_effort_by_resource({'Entity B':1}, 'Entity C')
	scenario_model.set_effort_by_resource({'Entity B':2}, 'Entity D')
	scenario_model.set_deadlines(deadlines)
	
	assert scenario_model.set_new_scen_model(model)  # should not change above
	assert scenario_model.ready()
	
	assert scenario_model.current_internal_states == current_internal_states
	assert scenario_model.realized_exits == realized_exits
	assert scenario_model.realized_timelines == realized_timelines
	assert scenario_model.efforts == efforts
	assert scenario_model.deadlines == deadlines
	
	model2 = GMORModel()
	assert not scenario_model.set_new_scen_model(model2)
test_gmorscenariomodel_set_new_scen_model.setup = setup3
test_gmorscenariomodel_set_new_scen_model.teardown = teardown

def test_gmorscenariomodel_set_new_scen_model2():
	"""
	different model
	"""
	print 'test_gmorscenariomodel_set_new_scen_model2'
	
	new_model = GMORModel()
	
	entities = ['Entity N', 'Entity M']
	ent_types = {'Entity N':'function', 'Entity M':'resource'}
	parents = {'Entity N':'function', 'Entity M':'resource'}
	dependencies = {'Entity N':['Entity N', 'Entity M'], 'Entity M':['Entity M']}
	resultant_states = {'Entity N':np.array([0, 0, 0, 1]), 'Entity M':np.array([0, 1])}
	resource_limits = {'Entity M':1.0}
	op_performance_levels = {'Entity N':1.0}
	
	new_model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)

	assert scenario_model.set_new_scen_model(new_model)
	assert scenario_model.model == new_model
	assert scenario_model.ready()
	
	assert scenario_model.current_internal_states == {'Entity N':1, 'Entity M':1}
	assert scenario_model.realized_exits == {'Entity N':-1, 'Entity M':-1}
	assert scenario_model.realized_timelines == {'Entity N':0, 'Entity M':0}
	assert scenario_model.efforts == {'Entity N':{'Entity M':0}}
	assert scenario_model.deadlines == {'Entity N':0}
test_gmorscenariomodel_set_new_scen_model2.setup = setup
test_gmorscenariomodel_set_new_scen_model2.teardown = teardown