"""
test_gmorrunner.py

__author__ = "Alison Goshulak, David Bristow"
__copyright__ = "Copyright 2016"
__credits__ = "David Bristow"
__maintainer__ = "David Bristow"
__status__ = "Development"
"""
#pylint: disable=trailing-whitespace
#pylint: disable=global-variable-undefined
import nose2
from gmor.model import *
from gmor.util import lists_equal, ordered_lists_equal
import numpy as np



def setup():
	"""
	setup for single entity model
	"""
	#print "SETUP!"
	global model
	global scen_model
	global runner
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global realized_exits
	global efforts
	global deadlines
	
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

	scen_model = GMORScenarioModel(model, "test")	
	deadlines = {'Entity A':1.0}
	scen_model.set_deadlines(deadlines)	
	current_internal_states = scen_model.current_internal_states
	realized_exits = scen_model.realized_exits
	realized_timelines = scen_model.realized_timelines
	efforts = scen_model.efforts
	
	runner = GMORRunner(model)

	
def setup2():
	"""
	setup for two entity model
	"""
	#print "SETUP!"
	global model
	global runner
	global scen_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global realized_exits
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

	scen_model = GMORScenarioModel(model, "test")
	deadlines = {'Entity A':1.0}
	scen_model.set_deadlines(deadlines)
	current_internal_states = scen_model.current_internal_states
	realized_exits = scen_model.realized_exits
	realized_timelines = scen_model.realized_timelines
	efforts = scen_model.efforts
	
	runner = GMORRunner(model)
	
def setup3():
	"""
	setup for two entity model with second one having 2 dependencies
	"""
	#print "SETUP!"
	global model
	global runner
	global scen_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global realized_exits
	global efforts
	global deadlines
	
	model = GMORModel()
		
	entities = ['Entity A', 'Entity B']
	ent_types = {'Entity A':'function', 'Entity B':'system'}
	parents = {'Entity A':'function', 'Entity B':'system'}
	dependencies = {'Entity A':['Entity B'], 'Entity B':['Entity B','Entity A']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 0, 0, 1])}
	resource_limits = {}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)	

	scen_model = GMORScenarioModel(model, "test")	
	deadlines = {'Entity A':1.0}
	scen_model.set_deadlines(deadlines)
	current_internal_states = scen_model.current_internal_states
	realized_exits = scen_model.realized_exits
	realized_timelines = scen_model.realized_timelines
	efforts = scen_model.efforts
	
	runner = GMORRunner(model)

def setup4():
	"""
	setup for three entity model with two internal dependencies
	"""
	#print "SETUP!"
	global model
	global runner
	global scen_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global realized_exits
	global efforts	
	global deadlines
	
	model = GMORModel()
		
	entities = ['Entity A', 'Entity B', 'Entity C']
	ent_types = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	parents = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	dependencies = {'Entity A':['Entity A'], 'Entity B':['Entity B', 'Entity C'], 'Entity C':['Entity A']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 0, 0, 1]), 'Entity C':np.array([0, 1])}
	resource_limits = {'Entity C':1.0}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)	

	scen_model = GMORScenarioModel(model, "test")
	scen_model.set_realized_timelines({'Entity A': 1.0, 'Entity B': 2.0, 'Entity C': 3.0})
	scen_model.set_effort_by_resource({'Entity B':1.0}, 'Entity C')
	deadlines = {'Entity A':1.0}
	scen_model.set_deadlines(deadlines)
	
	current_internal_states = scen_model.current_internal_states
	realized_exits = scen_model.realized_exits
	realized_timelines = scen_model.realized_timelines
	efforts = scen_model.efforts
	
	runner = GMORRunner(model)

def setup5():
	"""
	setup for model with two functions
	"""
	#print "SETUP!"
	global model
	global runner
	global scen_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global realized_exits
	global efforts
	global deadlines
	
	model = GMORModel()
		
	entities = ['Entity A', 'Entity B']
	ent_types = {'Entity A':'function', 'Entity B':'function'}
	parents = {'Entity A':'function', 'Entity B':'function'}
	dependencies = {'Entity A':['Entity A'], 'Entity B':['Entity B']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 1])}
	resource_limits = {}
	op_performance_levels = {'Entity A':0.25, 'Entity B':0.75}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)	

	scen_model = GMORScenarioModel(model, "test")
	scen_model.set_realized_timelines({'Entity A': 2.0, 'Entity B': 4.0})	
	deadlines = {'Entity A':10.0, 'Entity B':10.0}
	scen_model.set_deadlines(deadlines)
	
	current_internal_states = scen_model.current_internal_states
	realized_exits = scen_model.realized_exits
	realized_timelines = scen_model.realized_timelines
	efforts = scen_model.efforts
	
	runner = GMORRunner(model)

def setup6():
	"""
	setup for model with four entities, two with internal dependencies
	"""
	#print "SETUP!"
	
	global model
	global runner
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global deadlines
	
	model = GMORModel()
	
	entities = ['Entity A', 'Entity B', 'Entity C', 'Entity D']
	ent_types = {'Entity A':'function', 'Entity B':'event', 'Entity C':'function', 'Entity D':'resource'}
	parents = {'Entity A':'function', 'Entity B':'event', 'Entity C':'function', 'Entity D':'resource'}
	dependencies = {'Entity A':['Entity A'], 'Entity B':['Entity B'], 'Entity C':['Entity B'], 'Entity D':['Entity A']}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 1]), 'Entity C':np.array([0, 1]), 'Entity D':np.array([0, 1])}
	resource_limits = {'Entity D':1.0}
	op_performance_levels = {'Entity A':0.5, 'Entity C':0.5}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)
							  
	runner = GMORRunner(model)
	
	current_internal_states = {'Entity A':1, 'Entity B':1}
	realized_timelines = {'Entity A':1, 'Entity B':0, 'Entity C':0, 'Entity D':0}	
	deadlines = {'Entity A':5.0, 'Entity C':5.0}

def setup7():
	"""
	setup for three entity model with two internal dependencies
	"""
	#print "SETUP!"
	global model
	global runner
	global scen_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global realized_exits
	global efforts
	global deadlines
	
	model = GMORModel()
		
	entities = ['Entity A', 'Entity B', 'Entity C']
	ent_types = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	parents = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	dependencies = {'Entity A':['Entity A','Entity B'], 'Entity B':['Entity B','Entity C'], 'Entity C':['Entity C',]}
	resultant_states = {'Entity A':np.array([0, 0, 0, 1]), 'Entity B':np.array([0, 0, 0, 1]), 'Entity C':np.array([0, 1])}
	resource_limits = {'Entity C':1.0}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)	

	scen_model = GMORScenarioModel(model, "test")	
	deadlines = {'Entity A':1.0}
	scen_model.set_deadlines(deadlines)
	scen_model.set_realized_timelines({'Entity A': 0.0, 'Entity B': 0.0, 'Entity C': 0.0})
	scen_model.set_effort_by_resource({'Entity B':1.0}, 'Entity C')
	
	current_internal_states = scen_model.current_internal_states
	realized_exits = scen_model.realized_exits
	realized_timelines = scen_model.realized_timelines
	efforts = scen_model.efforts
	
	runner = GMORRunner(model)

def setup8():
	"""
	setup for three entity model with two internal dependencies
	"""
	#print "SETUP!"
	global model
	global runner
	global scen_model
	
	global entities
	global ent_types
	global parents
	global dependencies
	global resultant_states
	global resource_limits
	global op_performance_levels
	
	global current_internal_states
	global realized_timelines
	global realized_exits
	global efforts
	global deadlines
	
	model = GMORModel()
		
	entities = ['Entity A', 'Entity B', 'Entity C']
	ent_types = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	parents = {'Entity A':'function', 'Entity B':'system', 'Entity C':'resource'}
	dependencies = {'Entity A':['Entity B'], 'Entity B':['Entity C'], 'Entity C':['Entity C',]}
	resultant_states = {'Entity A':np.array([0, 1]), 'Entity B':np.array([0, 1]), 'Entity C':np.array([0, 1])}
	resource_limits = {}
	op_performance_levels = {'Entity A':1.0}
	
	model.set_and_check(entities, ent_types, parents, dependencies, resultant_states,
			                  resource_limits, op_performance_levels)	

	scen_model = GMORScenarioModel(model, "test")
	scen_model.set_realized_timelines({'Entity A': 0.0, 'Entity B': 0.0, 'Entity C': 0.0})
	scen_model.set_effort_by_resource({'Entity B':1.0}, 'Entity C')
	deadlines = {'Entity A':1.0}
	scen_model.set_deadlines(deadlines)
	
	current_internal_states = scen_model.current_internal_states
	realized_exits = scen_model.realized_exits
	realized_timelines = scen_model.realized_timelines
	efforts = scen_model.efforts
	
	runner = GMORRunner(model)
	
def teardown():
	"""
	teardown
	"""
	#print "TEAR DOWN!"
	model = GMORModel()

def test_gmorrunner_init():
	"""
	test_gmorrunner_init
	"""
	print 'test_gmorrunner_init'

	keys = runner.entity_lookup.keys()
	for ent in model.entities:
		assert ent in keys
		
	depKeys = runner.dependencies_lookup.keys()
	for ent in model.entities:
		assert ent in depKeys
		for dep in model.dependencies[ent]:
			assert runner.entity_lookup[dep] in runner.dependencies_lookup[ent]
			
	model2 = GMORModel()
	
	try:
		runner2 = GMORRunner(model2)
		assert False
	except ValueError:
		assert True
test_gmorrunner_init.setup = setup3
test_gmorrunner_init.teardown = teardown

def test_gmorrunner__get_ent_dep_sts_from_sys_st():
	"""
	test_gmorrunner__get_ent_dep_sts_from_sys_st
	"""
	print 'test_gmorrunner__get_ent_dep_sts_from_sys_st'
	
	func = runner._get_ent_dep_sts_from_sys_st
	
	n_ent = len(runner.entities)
	try:
		func('Entity A',get_bin_list(0,n_ent+1))
		assert False
	except ValueError:
		assert True
	
	assert lists_equal(func('Entity A',get_bin_list(0,n_ent)), [0])
	assert lists_equal(func('Entity A',get_bin_list(1,n_ent)), [1])
test_gmorrunner__get_ent_dep_sts_from_sys_st.setup = setup
test_gmorrunner__get_ent_dep_sts_from_sys_st.teardown = teardown

def test_gmorrunner__get_ent_dep_sts_from_sys_st2():
	"""
	test_gmorrunner__get_ent_dep_sts_from_sys_st2
	"""
	print 'test_gmorrunner__get_ent_dep_sts_from_sys_st2'
	
	func = runner._get_ent_dep_sts_from_sys_st
	
	n_ent = len(runner.entities)
	
	assert lists_equal(func('Entity A',get_bin_list(0,n_ent)), [0])
	assert lists_equal(func('Entity A',get_bin_list(1,n_ent)), [1])
	assert lists_equal(func('Entity A',get_bin_list(2,n_ent)), [0])
	assert lists_equal(func('Entity A',get_bin_list(3,n_ent)), [1])
	
	assert lists_equal(func('Entity B',get_bin_list(0,n_ent)), [0])
	assert lists_equal(func('Entity B',get_bin_list(1,n_ent)), [1])
	assert lists_equal(func('Entity B',get_bin_list(2,n_ent)), [0])
	assert lists_equal(func('Entity B',get_bin_list(3,n_ent)), [1])
test_gmorrunner__get_ent_dep_sts_from_sys_st2.setup = setup2
test_gmorrunner__get_ent_dep_sts_from_sys_st2.teardown = teardown

def test_gmorrunner__get_ent_dep_sts_from_sys_st3():
	"""
	test_gmorrunner__get_ent_dep_sts_from_sys_st3
	"""
	print 'test_gmorrunner__get_ent_dep_sts_from_sys_st3'
	
	func = runner._get_ent_dep_sts_from_sys_st
	
	n_ent = len(runner.entities)
	
	assert lists_equal(func('Entity A',get_bin_list(0,n_ent)), [0])
	assert lists_equal(func('Entity A',get_bin_list(1,n_ent)), [1])
	assert lists_equal(func('Entity A',get_bin_list(2,n_ent)), [0])
	assert lists_equal(func('Entity A',get_bin_list(3,n_ent)), [1])
	
	assert lists_equal(func('Entity B',get_bin_list(0,n_ent)), [0, 0])
	assert ordered_lists_equal(func('Entity B',get_bin_list(1,n_ent)), [1, 0])
	assert ordered_lists_equal(func('Entity B',get_bin_list(2,n_ent)), [0, 1])
	assert ordered_lists_equal(func('Entity B',get_bin_list(3,n_ent)), [1, 1])
test_gmorrunner__get_ent_dep_sts_from_sys_st3.setup = setup3
test_gmorrunner__get_ent_dep_sts_from_sys_st3.teardown = teardown

def test_gmorrunner__get_ent_resul_st_from_sys_st():
	"""
	test_gmorrunner__get_ent_resul_st_from_sys_st
	"""
	print 'test_gmorrunner__get_ent_resul_st_from_sys_st'
	
	func = runner._get_ent_resul_st_from_sys_st
	
	assert func('Entity A',[0]) == 0
	assert func('Entity A',[1]) == 1
test_gmorrunner__get_ent_resul_st_from_sys_st.setup = setup
test_gmorrunner__get_ent_resul_st_from_sys_st.teardown = teardown

def test_gmorrunner__get_ent_resul_st_from_sys_st2():
	"""
	test_gmorrunner__get_ent_resul_st_from_sys_st2
	"""
	print 'test_gmorrunner__get_ent_resul_st_from_sys_st2'
	
	func = runner._get_ent_resul_st_from_sys_st
	
	assert func('Entity A',[0,0]) == 0
	assert func('Entity A',[0,1]) == 1
	assert func('Entity A',[1,0]) == 0
	assert func('Entity A',[1,1]) == 1
	
	assert func('Entity B',[0,0]) == 0
	assert func('Entity B',[0,1]) == 1
	assert func('Entity B',[1,0]) == 0
	assert func('Entity B',[1,1]) == 1
test_gmorrunner__get_ent_resul_st_from_sys_st2.setup = setup2
test_gmorrunner__get_ent_resul_st_from_sys_st2.teardown = teardown

def test_gmorrunner__get_ent_resul_st_from_sys_st3():
	"""
	test_gmorrunner__get_ent_resul_st_from_sys_st3
	"""
	print 'test_gmorrunner__get_ent_resul_st_from_sys_st3'
	
	func = runner._get_ent_resul_st_from_sys_st
	
	assert func('Entity A',[0,0]) == 0
	assert func('Entity A',[0,1]) == 1
	assert func('Entity A',[1,0]) == 0
	assert func('Entity A',[1,1]) == 1
	
	assert func('Entity B',[0,0]) == 0
	assert func('Entity B',[0,1]) == 0
	assert func('Entity B',[1,0]) == 0
	assert func('Entity B',[1,1]) == 1
test_gmorrunner__get_ent_resul_st_from_sys_st3.setup = setup3
test_gmorrunner__get_ent_resul_st_from_sys_st3.teardown = teardown

def test_gmorrunner__det_sys_wide_state_pessimistic():
	"""
	test_gmorrunner__det_sys_wide_state_pessimistic
	"""
	print 'test_gmorrunner__det_sys_wide_state_pessimistic'
	
	func = runner._det_sys_wide_state_pessimistic
	
	assert lists_equal(func(current_internal_states, realized_timelines), [1])
	
	curr_int_sts = {'Entity A':0}
	assert lists_equal(func(curr_int_sts, realized_timelines), [0])
test_gmorrunner__det_sys_wide_state_pessimistic.setup = setup
test_gmorrunner__det_sys_wide_state_pessimistic.teardown = teardown

def test_gmorrunner__det_sys_wide_state_pessimistic2():
	"""
	test_gmorrunner__det_sys_wide_state_pessimistic2
	"""
	print 'test_gmorrunner__det_sys_wide_state_pessimistic2'
	
	func = runner._det_sys_wide_state_pessimistic
	assert lists_equal(func(current_internal_states, realized_timelines), [1, 1])
	
	rlzd_timelines = {'Entity A':0, 'Entity B':1}
	assert lists_equal(func(current_internal_states, rlzd_timelines), [0, 0])
test_gmorrunner__det_sys_wide_state_pessimistic2.setup = setup3
test_gmorrunner__det_sys_wide_state_pessimistic2.teardown = teardown

def test_gmorrunner__det_sys_wide_state_pessimistic3():
	"""
	test_gmorrunner__det_sys_wide_state_pessimistic3
	"""
	print 'test_gmorrunner__det_sys_wide_state_pessimistic3'
	
	func = runner._det_sys_wide_state_pessimistic
	assert lists_equal(func(current_internal_states, realized_timelines), [0, 0, 0])  # none of the time lines are zero
	
	rlzd_timelines = {'Entity A':0, 'Entity B':0, 'Entity C':0}
	assert lists_equal(func(current_internal_states, rlzd_timelines), [1, 1, 1])
	
	
	curr_int_sts = {'Entity A':1, 'Entity B':0}
	print '3.3>>>',curr_int_sts, rlzd_timelines
	assert ordered_lists_equal(func(curr_int_sts, rlzd_timelines), [1, 0, 1])
	
	curr_int_sts = {'Entity A':0, 'Entity B':1}
	print '3.4>>>',curr_int_sts, rlzd_timelines
	assert lists_equal(func(curr_int_sts, rlzd_timelines), [0, 0, 0])
	
	runner.dependencies['Entity B'] = ['Entity C']
	runner.resultant_states['Entity B'] = np.array([0, 1])
	assert lists_equal(func(current_internal_states, rlzd_timelines), [1, 1, 1])
test_gmorrunner__det_sys_wide_state_pessimistic3.setup = setup4
test_gmorrunner__det_sys_wide_state_pessimistic3.teardown = teardown

def test_gmorrunner__det_sys_wide_state_pessimistic4():
	"""
	test_gmorrunner__det_sys_wide_state_pessimistic4
	"""
	print 'test_gmorrunner__det_sys_wide_state_pessimistic4'
	
	func = runner._det_sys_wide_state_pessimistic
	assert ordered_lists_equal(func(current_internal_states, realized_timelines), [0, 1, 1, 0])
test_gmorrunner__det_sys_wide_state_pessimistic4.setup = setup6
test_gmorrunner__det_sys_wide_state_pessimistic4.teardown = teardown

def test_gmorrunner__build_progression():
	"""
	test_gmorrunner__build_progression
	"""
	print 'test_gmorrunner__build_progression'
	
	func = runner._build_progression
	system_state = [0]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert lists_equal(dep_changes, ['Entity A'])
	assert lists_equal(dep_change_timing, [0.0])
	assert lists_equal(system_state_res, [1])
	
	system_state = [1]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert lists_equal(dep_changes, [])  # A already active
	assert lists_equal(dep_change_timing, [])
	assert lists_equal(system_state_res, [1])
test_gmorrunner__build_progression.setup = setup
test_gmorrunner__build_progression.teardown = teardown

def test_gmorrunner__build_progression2():
	"""
	test_gmorrunner__build_progression2
	"""
	print 'test_gmorrunner__build_progression2'
	
	func = runner._build_progression
	system_state = [0, 1]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert lists_equal(dep_changes, ['Entity A'])
	assert lists_equal(dep_change_timing, [0.0])
	assert lists_equal(system_state_res, [1, 1])
	
	system_state = [0, 0]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert ordered_lists_equal(dep_changes, ['Entity B', 'Entity A'])  # resultant state of A only becomes 1 after B changes
	assert lists_equal(dep_change_timing, [0.0, 0.0])
	assert lists_equal(system_state_res, [1, 1])
test_gmorrunner__build_progression2.setup = setup2
test_gmorrunner__build_progression2.teardown = teardown

def test_gmorrunner__build_progression3():
	"""
	test_gmorrunner__build_progression3
	"""
	print 'test_gmorrunner__build_progression3'
	
	func = runner._build_progression
	system_state = [0, 1]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert lists_equal(dep_changes, ['Entity A'])  # resultant state of B changes, but not in system_state
	assert lists_equal(dep_change_timing, [0.0])
	assert lists_equal(system_state_res, [1, 1])
	
	system_state = [1, 0]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert lists_equal(dep_changes, ['Entity B'])
	assert lists_equal(dep_change_timing, [0.0])
	assert lists_equal(system_state_res, [1, 1])
test_gmorrunner__build_progression3.setup = setup3
test_gmorrunner__build_progression3.teardown = teardown

def test_gmorrunner__build_progression4():
	"""
	test_gmorrunner__build_progression4
	"""
	print 'test_gmorrunner__build_progression4'
	
	func = runner._build_progression
	system_state = [0, 0, 0]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert ordered_lists_equal(dep_changes, ['Entity A', 'Entity C', 'Entity B'])
	assert ordered_lists_equal(dep_change_timing, [1.0, 4.0, 6.0])
	assert lists_equal(system_state_res, [1, 1, 1])
	
	system_state = [0, 0, 1]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert ordered_lists_equal(dep_changes, ['Entity A', 'Entity B'])
	assert ordered_lists_equal(dep_change_timing, [1.0, 2.0])
	assert lists_equal(system_state_res, [1, 1, 1])
	
	system_state = [0, 1, 0]
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines)
	assert ordered_lists_equal(dep_changes, ['Entity A', 'Entity C'])
	assert ordered_lists_equal(dep_change_timing, [1.0, 4.0])
	assert lists_equal(system_state_res, [1, 1, 1])
	
	dep_changes, dep_change_timing, system_state_res = func(system_state, realized_timelines, stop_at=3.0)
	assert lists_equal(dep_changes, ['Entity A'])
	assert lists_equal(dep_change_timing, [1.0])
	assert ordered_lists_equal(system_state_res, [1, 1, 0])
test_gmorrunner__build_progression4.setup = setup4
test_gmorrunner__build_progression4.teardown = teardown

def test_gmorrunner__disimprove_from_exits():
	"""
	test_gmorrunner__disimprove_from_exits
	"""
	print 'test_gmorrunner__disimprove_from_exits'
	
	build = runner._build_progression
	disimprove = runner._disimprove_from_exits
	system_state = [0, 0, 0]
	try:
		disimprove([], [], realized_exits, system_state, [0, 0, 0])
		assert True  # no changes
	except ValueError:
		assert False
		
	dep_changes, dep_timing, system_state_res = build(system_state, realized_timelines)
	try:
		disimprove(dep_changes, dep_timing, realized_exits, system_state, system_state_res)
		assert False  # exits at -1 (impossible for changes to occur first)
	except ValueError:
		assert True
		
	system_state = [1, 1, 0]	
	rlzd_exits = {'Entity A':2.0, 'Entity B':4.0} #  A exits before C changes
	dep_changes, dep_timing, system_state_res = build(system_state, realized_timelines)
	try:
		disimprove(dep_changes, dep_timing, rlzd_exits, system_state, system_state_res)
		assert False
	except ValueError:
		assert True
		
	system_state = [0, 0, 1]	
	rlzd_exits = {'Entity A':5.0, 'Entity B':5.0} # both exit after all changes
	dep_changes, dep_timing, system_state_res = build(system_state, realized_timelines)
	try:
		disimprove(dep_changes, dep_timing, rlzd_exits, system_state, system_state_res)
		assert True
	except ValueError:
		assert False
test_gmorrunner__disimprove_from_exits.setup = setup4
test_gmorrunner__disimprove_from_exits.teardown = teardown

def test_gmorrunner__assess_resource_allotment():
	"""
	test_gmorrunner__assess_resource_allotment
	"""
	print 'test_gmorrunner__assess_resource_allotment'
	
	assess = runner._assess_resource_allotment
	build = runner._build_progression
	system_state = [0]
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	assert assess(dep_changes, dep_timing, realized_timelines, efforts) == {}  # no resources
test_gmorrunner__assess_resource_allotment.setup = setup
test_gmorrunner__assess_resource_allotment.teardown = teardown

def test_gmorrunner__assess_resource_allotment2():
	"""
	test_gmorrunner__assess_resource_allotment2
	"""
	print 'test_gmorrunner__assess_resource_allotment2'
	
	assess = runner._assess_resource_allotment
	build = runner._build_progression
	system_state = [1, 1, 1]
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	assert assess(dep_changes, dep_timing, realized_timelines, efforts) == {}
	
	system_state = [1, 0, 1]
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	try:
		res_use = assess(dep_changes, dep_timing, realized_timelines, efforts)
		assert True
	except ValueError:
		assert False
	assert res_use == {'Entity C':[1.0]}
	
	effort_over_limit = {'Entity B':{'Entity C':2.0}}  # not enough resource for effort
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	try:
		assess(dep_changes, dep_timing, realized_timelines, effort_over_limit)
		assert False
	except ValueError:
		assert True
		
	system_state = [0, 0, 0]
	float_timeline = {'Entity A':1.2, 'Entity B':0.5, 'Entity C':1}
	dep_changes, dep_timing, unused_result = build(system_state, float_timeline)
	try:
		res_use = assess(dep_changes, dep_timing, float_timeline, efforts)
		assert True
	except ValueError:
		assert False
	assert ordered_lists_equal(res_use['Entity C'], [0.0, 0.0, 1.0])
	
	runner.dependencies['Entity A'] = ['Entity C']
	runner.dependencies['Entity B'] = ['Entity A', 'Entity C']
	runner.dependencies['Entity C'] = ['Entity C']
	dep_changes = ['Entity C', 'Entity A', 'Entity B']
	dep_timing = [3.0, 4.0, 6.0]
	efforts2 = {'Entity A':{'Entity C':0.5}, 'Entity B':{'Entity C':0.5}}
	try:
		res_use = assess(dep_changes, dep_timing, realized_timelines, efforts2)
		assert True
	except ValueError:
		assert False
	assert res_use == {'Entity C':[0.0, 0.5, 0.5]}
test_gmorrunner__assess_resource_allotment2.setup = setup4
test_gmorrunner__assess_resource_allotment2.teardown = teardown

def test_gmorrunner__assess_resource_allotment3():
	"""
	test_gmorrunner__assess_resource_allotment3
	"""
	print 'test_gmorrunner__assess_resource_allotment3'
	
	assess = runner._assess_resource_allotment
	runner.dependencies['Entity B'] = ['Entity B', 'Entity D']
	runner.dependencies['Entity C'] = ['Entity D']
	realized_timelines = {'Entity A':0, 'Entity B':1, 'Entity C':2, 'Entity D':0}
	efforts = {'Entity B':{'Entity D':0.5}, 'Entity C':{'Entity D':0.5}}
	dep_changes = ['Entity B', 'Entity C']
	dep_timing = [1.0, 2.0]
	try:
		res_use = assess(dep_changes, dep_timing, realized_timelines, efforts)
		assert True
	except ValueError:
		assert False
	assert res_use == {'Entity D':[1.0, 1.0]}
test_gmorrunner__assess_resource_allotment3.setup = setup6
test_gmorrunner__assess_resource_allotment3.teardown = teardown

def test_gmorrunner__find_pa():
	"""
	test_gmorrunner__find_pa
	"""
	print 'test_gmorrunner__find_pa'
	
	func = runner._find_pa
	system_state = [1, 0]
	p_a, ents_for_pa = func(system_state)
	assert p_a == 1.0
	assert lists_equal(ents_for_pa, ['Entity A'])
	
	system_state = [0, 1]
	p_a, ents_for_pa = func(system_state)
	assert p_a == 0.0
	assert lists_equal(ents_for_pa, [])
	
	model.del_entity('Entity A')
	system_state = [1]
	assert p_a == 0.0
	assert lists_equal(ents_for_pa, [])
test_gmorrunner__find_pa.setup = setup2
test_gmorrunner__assess_resource_allotment.teardown = teardown

def test_gmorrunner_check_changes_timing():
	"""
	test_gmorrunner_check_changes_timing
	"""
	print 'test_gmorrunner_check_changes_timing'
	build = runner._build_progression
	check = runner.check_changes_timing
	assert check(1.0, ['Entity A'], [], [], deadlines)  # no changes but A is active
	
	system_state = [0, 1]
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	assert check(1.0, ['Entity A'], dep_changes, dep_timing, deadlines)  # already okay at p_a
	
	assert check(0.0, [], dep_changes, dep_timing, deadlines)  # A changed before deadline
	
	assert not check(0.0, [], dep_changes, [2.0], deadlines)  # deadline before A changed
test_gmorrunner_check_changes_timing.setup = setup2
test_gmorrunner_check_changes_timing.teardown = teardown

def test_gmorrunner_do_progression():
	"""
	test_gmorrunner_do_progression
	"""
	print 'test_gmorrunner_do_progression'
	
	func = runner.do_progression
	scen_model.set_current_internal_states({'Entity A':0, 'Entity B':1})
	# system state will be [0, 0, 0] after _det_sys_wide_state_pessimistic
	scen_model.set_realized_exits({'Entity A':2.0, 'Entity B':-1.0})
	try:
		p_a, dep_changes, dep_timing, tracked_resource_use = func(scen_model)
		assert False  # dependency expiration
	except ValueError:
		assert True
		
	scen_model.set_realized_exits({'Entity A':5.0, 'Entity B':5.0})
	scen_model.set_realized_timelines({'Entity A':5.0, 'Entity B':0, 'Entity C':0})
	try:
		p_a, dep_changes, dep_timing, tracked_resource_use = func(scen_model)
		assert False  # not enough time
	except ValueError:
		assert True
		
	scen_model.set_effort_by_resource({'Entity B':5.0}, 'Entity C')
	scen_model.set_realized_timelines({'Entity A':0, 'Entity B':0, 'Entity C':0})
	try:
		p_a, dep_changes, dep_timing, tracked_resource_use = func(scen_model)
		assert False  # not enough resource
	except ValueError:
		assert True
		
	scen_model.set_effort_by_resource({'Entity B':1.0}, 'Entity C')
	p_a, dep_changes, dep_timing, tracked_resource_use = func(scen_model)
	assert p_a == 0
	assert ordered_lists_equal(dep_changes, ['Entity A', 'Entity C', 'Entity B'])
	assert lists_equal(dep_timing, [0, 0, 0])
	assert lists_equal(tracked_resource_use['Entity C'], [1.0, 1.0, 1.0])
	
	scen_model.realized_timelines = {}
	try:
		p_a, dep_changes, dep_timing, tracked_resource_use = func(scen_model)
		assert False  # scen_model not ready
	except ValueError:
		assert True
test_gmorrunner_do_progression.setup = setup4
test_gmorrunner_do_progression.teardown = teardown

def test_gmorrunner_plot_performance_curve():
	"""
	test_gmorrunner_plot_performance_curve
	"""
	print 'test_gmorrunner_plot_performance_curve'
	
	quick_test = True  # not checking details of figure, just whether its being saved properly
	
	build = runner._build_progression
	find = runner._find_pa
	plot = runner.plot_performance_curve
	
	system_state = [0, 1]
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	p_a, unused_result = find(system_state)
	plot(p_a, dep_changes, dep_timing, save=True, file_name='plot_test.png', path=(os.getcwd() + '\\test\\'))
	file = os.getcwd() + '\\test\\plot_test.png'
	if os.path.isfile(file):
		assert True
		if quick_test:
			os.remove(file)
	else:
		assert False
	'''
	system_state = [0, 0]
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	p_a, unused_result = find(system_state)
	plot(p_a, dep_changes, dep_timing, save=True)
	file = 'c:\\workspace\\projects\\GMOR\\LOSS-'+str(date.today())+'-'+time.strftime('%X').replace(':', '_')+'.png'
	if os.path.isfile(file):  # file name may not be exactly the same due to time stamp
		os.remove(file)
		
	system_state = [1, 0]
	dep_changes, dep_timing, unused_result = build(system_state, realized_timelines)
	p_a, unused_result = find(system_state)
	plot(p_a, dep_changes, dep_timing)'''
test_gmorrunner_plot_performance_curve.setup = setup5
test_gmorrunner_plot_performance_curve.teardown = teardown

def test_gmorrunner__get_new_timeline():
	"""
	test_gmorrunner__get_new_timeline
	"""
	print 'test_gmorrunner__get_new_timeline'
	
	new_timelines = {'Entity A':2, 'Entity B':2, 'Entity C':2, 'Entity D':2}
	int_dep_func = ['Entity A']
	
	result = runner._get_new_timeline(new_timelines, int_dep_func)
	for ent in result.keys():
		if ent != 'Entity C':
			assert result[ent] == 2
	assert result['Entity C'] == 0.0 # C is a function but not internally dependent	
test_gmorrunner__get_new_timeline.setup = setup6
test_gmorrunner__get_new_timeline.teardown = teardown

def test_gmorrunner_deterministic_progression():
	"""
	test_gmorrunner_deterministic_progression
	"""
	print 'test_gmorrunner_deterministic_progression'
	
	realized_timelines = ({'Entity A':0, 'Entity B':0, 'Entity C':0})
	realized_exits = ({'Entity A':5.0, 'Entity B':5.0})
	p_a, dep_changes, dep_timing, res_use = runner.deterministic_progression(model, current_internal_states,
	                                                                         realized_timelines, realized_exits,
																			 efforts, deadlines)
	assert p_a == 1
	assert not dep_changes #[]
	assert not dep_timing #[]
	assert not res_use #[]
	
	deads = {}
	try:
		runner.deterministic_progression(model, current_internal_states, realized_timelines,
	                                          realized_exits, efforts, deads)
		assert False #scen_model not ready
	except ValueError:
		assert True
test_gmorrunner_deterministic_progression.setup = setup4
test_gmorrunner_deterministic_progression.teardown = teardown

def test_gmorrunner_next_deadline():
	"""
	test_gmorrunner_next_deadline
	"""
	print 'test_gmorrunner_next_deadline'
	
	dline,ents = runner.next_deadline(0.0, [0], deadlines)
	assert dline == 1.0
	assert lists_equal(ents,['Entity A'])
	
	dline,ents = runner.next_deadline(0.0, [1], deadlines)
	assert dline == 1.0
	assert lists_equal(ents,[])
	
	dline,ents = runner.next_deadline(1.0, [0], deadlines)
	assert dline == -1
	assert lists_equal(ents,[])
	
	dline,ents = runner.next_deadline(1.5, [0], deadlines)
	assert dline == -1
	assert lists_equal(ents,[])	
test_gmorrunner_next_deadline.setup = setup
test_gmorrunner_next_deadline.teardown = teardown

def test__gmorrunner_get_deps_to_do():
	"""
	test__gmorrunner_get_deps_to_do
	"""
	
	print 'test__gmorrunner_get_deps_to_do'
	
	deps = []
	runner.get_deps_to_do(['Entity A'],deps,{'Entity A':1,'Entity B':0,'Entity C':0},[0,0,0],[])
	assert lists_equal(deps,['Entity B','Entity C'])
	
	deps = []
	runner.get_deps_to_do(['Entity A'],deps,{'Entity A':1,'Entity B':0,'Entity C':1},[0,0,1],[])
	assert lists_equal(deps,['Entity B'])
	
	deps = []
	runner.get_deps_to_do(['Entity A'],deps,{'Entity A':1,'Entity B':1,'Entity C':0},[1,0,0],[])
	assert lists_equal(deps,['Entity C'])
	
	deps = []
	runner.get_deps_to_do(['Entity B'],deps,{'Entity A':1,'Entity B':0,'Entity C':1},[1,0,1],[])
	assert lists_equal(deps,['Entity B'])
	
	deps = []
	runner.get_deps_to_do(['Entity B'],deps,{'Entity A':0,'Entity B':0,'Entity C':1},[0,0,1],[])
	assert lists_equal(deps,['Entity B'])
	
	deps = []
	runner.get_deps_to_do(['Entity B'],deps,{'Entity A':1,'Entity B':1,'Entity C':1},[1,1,1],[])
	assert lists_equal(deps,[])
	
	deps = []
	runner.get_deps_to_do(['Entity B'],deps,{'Entity A':1,'Entity B':1,'Entity C':1},[0,0,0],[])
	assert lists_equal(deps,[])

test__gmorrunner_get_deps_to_do.setup = setup7
test__gmorrunner_get_deps_to_do.teardown = teardown

def test_gmorrunner_max_timing_progression():
	"""
	test_gmorrunner_max_timing_progression
	"""
	print 'test_gmorrunner_max_timing_progression'
	defaults = {
	 'Entity A': 1,
	 'Entity B': 1,
	 'Entity C': 1
	}
	
	#def get_rlzd_timing(timings):
	#	timing_temp = {'Entity A':0.0,'Entity B':0.0,'Entity C':0.0}
	#	for key in timings:
	#		for ent in timings[key]: timing_temp[ent] = key	
	#	return runner._get_new_timeline(timing_temp, ['Entity A'])
	
	#print ['1,' for i in range(20)]
	curr_int_sts = {'Entity A': 1,'Entity B': 1,'Entity C': 1}
	timings = runner.max_timing_progression(curr_int_sts, defaults, deadlines)
	assert lists_equal(timings.keys(),[1.0])
	assert lists_equal(timings[1.0],[])
	
	#print ['2,' for i in range(20)]
	curr_int_sts = {'Entity A': 1,'Entity B': 0,'Entity C': 1}
	timings = runner.max_timing_progression(curr_int_sts, defaults, deadlines)
	assert lists_equal(timings.keys(),[1.0])
	assert lists_equal(timings[1.0],['Entity B'])
	
	#print ['3,' for i in range(20)]
	curr_int_sts = {'Entity A': 1,'Entity B': 0,'Entity C': 0}
	timings = runner.max_timing_progression(curr_int_sts, defaults, deadlines)
	assert lists_equal(timings.keys(),[1.0])
	assert lists_equal(timings[1.0],['Entity B','Entity C'])
	#print '<<<<',get_rlzd_timing(timings)#,timings
	# the progression is showing not enough time because you are passing in
	# timings that say Entity B will take 1.0 time after C is active (which takes 1.0)
	# so on sum, B is not activated in progression probs until time 2.0}
	# basically, the function is doing what it supposed to, you were just trying to use it incorrectly.
	# print runner.deterministic_progression(model, curr_int_sts, get_rlzd_timing(timings),{}, {'Entity B':{'Entity C':0.0}})
	
	#print ['4,' for i in range(20)]
	curr_int_sts = {'Entity A': 0,'Entity B': 0,'Entity C': 0}
	timings = runner.max_timing_progression(curr_int_sts, defaults, deadlines)
	assert lists_equal(timings.keys(),[1.0])
	assert lists_equal(timings[1.0],['Entity A','Entity B','Entity C'])
test_gmorrunner_max_timing_progression.setup = setup7
test_gmorrunner_max_timing_progression.teardown = teardown

def test_gmorrunner_max_timing_progression2():
	"""
	test_gmorrunner_max_timing_progression2
	"""
	print 'test_gmorrunner_max_timing_progression2'
	defaults = {
	 'Entity A': 1,
	 'Entity B': 1,
	 'Entity C': 1
	}
	
	curr_int_sts = {'Entity C': 0}
	timings = runner.max_timing_progression(curr_int_sts, defaults, deadlines)
	assert lists_equal(timings.keys(),[1.0])
	assert lists_equal(timings[1.0],['Entity A','Entity B','Entity C'])
	
test_gmorrunner_max_timing_progression2.setup = setup8
test_gmorrunner_max_timing_progression2.teardown = teardown