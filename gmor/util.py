"""
util.py

__author__ = "David Bristow"
__copyright__ = "Copyright 2016"
__credits__ = []
__maintainer__ = "David Bristow"
__status__ = "Development"
"""

import numpy as np
import itertools
import copy
from model import GMORModel, ENTTYPE, get_bin_lists, get_dec_from_bin_arr

def lists_equal(L1,L2):
	"""
	Check if two lists are the same.
	
	Arguments:
	L1 -- one list
	L2 -- the other list
	
	Return values:
	True -- if lists equal length, and equal when sorted
	False -- otherwise
	"""
	return len(L1) == len(L2) and sorted(L1) == sorted(L2)

def ordered_lists_equal(L1, L2):
	"""
	Check if two lists have equal length and order.
	
	Arguments:
	L1 -- one list
	L2 -- the other list
	
	Return values:
	True -- if lists equal length, and contain same item at each position
	False -- otherwise
	"""
	if len(L1) != len(L2):
		return False
	
	for i in range(len(L1)):
		if L1[i] != L2[i]:
			return False
	
	return True
	
def get_curr_int_states(ents_to_do, defaults):
	"""
	Create a list of current_internal_states dictionaries.
	
	Arguments:
	ents_to_do -- dictionary of internally-dependent entities with values
				  indicating whether to use default states (0) or not (1)
	defaults -- dictionary of internally-dependent entities and their 
				default internal states
				
	Return values:
	curr_int_states -- a list of current_internal_states dictionaries
	"""
	curr_int_states = []
	for temp_arr in itertools.product(range(2), repeat=sum(ents_to_do.values())):
		temp = {}
		count = 0
		for ent in ents_to_do.keys():
			if ents_to_do[ent] == 0:
				temp[ent] = defaults[ent]
			else:
				temp[ent] = temp_arr[count]
				count += 1
		curr_int_states.append(temp)
	return curr_int_states
	
def update_res_sts_after_treatment(model, ent, old_dep):
	"""
	Update resultant states of an entity after adding a new dependency.
	
	Arguments:
	model -- the GMORModel containing the affected entity and its dependencies
	ent -- the affected entity
	old_dep -- the old dependency of ent involved in the treatment of model
	           (i.e. addition of redundancy, flexibility, or diversity)
	
	Note: 
	An OR relationship between old_dep and the new dependency will be reflected in the states.
	"""
	'''
	deps = model.dependencies[ent]
	n_dep = len(deps)
	ind_old_dep = deps.index(old_dep)-1
	old_states = get_bin_lists(n_dep-1)
	new_res_states = np.zeros(2**n_dep)
	for i in range(2**(n_dep-1)): 
		if model.resultant_states[ent][i] == 1: # get the easy ones where there is just duplication
			new_res_states[i] = 1
			new_res_states[i+2**(n_dep-1)] = 1
		else: # toggle existing old_dep value to see if state changes
			cur_st = copy.copy(old_states[i])
			cur_st[ind_old_dep] = 1-cur_st[ind_old_dep]
			i_new = get_dec_from_bin_arr(cur_st)
			if model.resultant_states[ent][i_new] == 1:
				new_res_states[i+2**(n_dep-1)] = 1
	#print model.dependencies[ent],'\n'
	#print model.resultant_states[ent],'\n'
	model.resultant_states[ent] = copy.copy(new_res_states)
	#print model.resultant_states[ent],'\n'
	'''
	#old code not working, new code passing current tests
	deps = model.dependencies[ent]
	n_dep = len(deps)
	ind_old_dep = deps.index(old_dep)
	new_res_states = np.zeros(2**n_dep, dtype=int)
	old_states = get_bin_lists(n_dep-1)
	new_states = get_bin_lists(n_dep)
	for i in range(2**(n_dep-1)): 
		if model.resultant_states[ent][i] == 1: # get the easy ones where there is just duplication
			new_res_states[i*2] = 1 #corresponding position in new res states
			if (old_states[i][::-1])[ind_old_dep-1] == 1: # if state of old_dep is 1
				state = copy.deepcopy(old_states[i][::-1])
				for j in range(len(new_states)):
					cur_st = copy.deepcopy(new_states[j][::-1])
					del cur_st[ind_old_dep]
					if ordered_lists_equal(state, cur_st): # (old_dep OR new_dep)
						new_res_states[j] = 1
	model.resultant_states[ent] = copy.copy(new_res_states)
	
def add_redundancy(model_old, ent_to_copy, suffix=' red', select=[], weight=0.5):
	"""
	Create a copy of the model with a redundant entity.
	
	Arguments:
	model_old -- the GMORModel before the redundancy is added
	ent_to_copy -- the entity being made redundant
	
	Keyword argument:
	suffix -- distinguishes the new entity from the original entity (default ' red')
	select -- the entities dependent on ent_to_copy that will receive the redundancy (default [];
			  all dependencies will receive the redundancy)
	weight -- used to adjust performance levels to sum to 1 if necessary (default 0.5)
			  
	Return values:
	model -- the new model after the redundancy is added (GMORModel instance)
	
	Exceptions:
	ValueError -- raised when ent_to_copy is not an entity of model_old, or ent_to_copy is an event or time entity
	              (entities of these types cannot be made redundant)
	"""
	if not model_old.is_ent(ent_to_copy):
		raise ValueError('Cannot add redundancy with non-entity')
	if model_old.ent_types[ent_to_copy] == ENTTYPE.EVENT:
		raise ValueError('events cannot be made redundant')
	elif model_old.ent_types[ent_to_copy] == ENTTYPE.TIME:
		raise ValueError('time entities cannot be made redundant')
	
	model = copy.deepcopy(model_old)
	ent_new = ent_to_copy+suffix
	
	if len(select) == 0:
		select = [ent for ent in model.entities if ent_to_copy in model.dependencies[ent]]
	
	# add redundant dependency to entities
	for ent in select:
		if ent_to_copy in model.dependencies[ent] and ent_to_copy != ent:
			model.dependencies[ent].insert(0, ent_new)#append(ent_new)
	
			update_res_sts_after_treatment(model, ent, ent_to_copy)
	
	# add dependencies on to new entity
	model.dependencies[ent_new] = []
	for dep in model.dependencies[ent_to_copy]:
		if dep == ent_to_copy:
			model.dependencies[ent_new].append(ent_new)
		else:
			model.dependencies[ent_new].append(dep)
	
	# add entity
	model.entities.append(ent_new)
	
	# add entType
	model.ent_types[ent_new] = model.ent_types[ent_to_copy]
	
	# add parent
	model.parents[ent_new] = model.parents[ent_to_copy]
	
	# add new ent resultant states
	model.resultant_states[ent_new] = copy.deepcopy(model.resultant_states[ent_to_copy])
	
	# add resource limits to new ent
	if ent_to_copy in model.resource_limits:
		model.resource_limits[ent_new] = model.resource_limits[ent_to_copy]
		
	# add performance levels to new ent, adjust levels of red ent
	if ent_to_copy in model.op_performance_levels:
		model.op_performance_levels[ent_new] = model.op_performance_levels[ent_to_copy]*(1.0-weight)
		model.op_performance_levels[ent_to_copy] = model.op_performance_levels[ent_to_copy]*weight
			
	return model

def add_flexibility(model_old, dep_ent, flex_ent, select=[]):
	"""
	Create a copy of the model with added flexibility.
	
	Arguments:
	model_old -- the GMORModel before the flexibility is added
	dep_ent -- entities that depend on dep_ent will receive flexibility
	flex_ent -- the entity that will be made a more flexible dependency
	
	Keyword argument:
	select -- the entities dependent on dep_ent that will receive the flexibility (default [];
			  all dependencies will receive the flexibility)
			  
	Return values:
	model -- the new model after the flexibility is added (GMORModel instance)
	
	Exceptions:
	ValueError -- raise when flex_ent or dep_ent is not an entity in model_old, or dep_ent is an event
	              or time entity (entities of these types cannot be used for adding flexibility)
	"""
	if not model_old.is_ent(flex_ent) or not model_old.is_ent(dep_ent):
		raise ValueError('Cannot add flexibility with non-entity')
	if model_old.ent_types[dep_ent] == ENTTYPE.EVENT:
		raise ValueError('events cannot be used for adding flexibility')
	elif model_old.ent_types[dep_ent] == ENTTYPE.TIME:
		raise ValueError('time entities cannot be used for adding flexibility')
	model = copy.deepcopy(model_old)
	
	if len(select) == 0:
		select = [ent for ent in model.entities if dep_ent in model.dependencies[ent]]
		
	#add flexibility to ents that depend on dep_ent
	for ent in select:
		if (dep_ent in model.dependencies[ent] and ent != dep_ent and
		    ent != flex_ent and flex_ent not in model.dependencies[ent]):
			# check that ent and flex_ent are not both resources (resource can't depend on a different resource)
			if not (model.ent_types[ent] == ENTTYPE.RESOURCE and model.ent_types[flex_ent] == ENTTYPE.RESOURCE):
				model.dependencies[ent].insert(0, flex_ent)
		
				update_res_sts_after_treatment(model, ent, dep_ent)
	
	return model

def add_diversity(model_old, model_new, dep_ent, div_ent, select=[]):
	"""
	Create a copy of the model with added diversity.
	
	Arguments:
	model_old -- the GMORModel before diversity is added
	model_new -- the GMORModel containing div_ent and its dependencies
	dep_ent -- entities dependent on dep_ent will be diversified
	div_ent -- the entity to be made a more diverse dependency
	
	Keyword argument:
	select -- the entities dependent on dep_ent that will receive the diversification (default [];
			  all dependencies will receive the diversification)
			  
	Return values:
	model -- the new model after diversity is added (GMORModel instance)
	
	Exceptions:
	ValueError -- raised when dep_ent is not an entity of model_old or div_ent is not an entity of model_new,
	              or dep_ent is an event or time entity (entities of these types cannot be used for diversification)
	"""
	if not model_old.is_ent(dep_ent) or not model_new.is_ent(div_ent):
		raise ValueError('Cannot add diversity with non-entity')
	if model_old.ent_types[dep_ent] == ENTTYPE.EVENT:
		raise ValueError('events cannot be used for diversification')
	elif model_old.ent_types[dep_ent] == ENTTYPE.TIME:
		raise ValueError('time entities cannot be used for diversification')
	
	model = copy.deepcopy(model_old)
	model.merge_models(model_new)  # add entities of model_new
	
	if len(select) == 0:
		select = [ent for ent in model.entities if dep_ent in model.dependencies[ent]]
	
	#add diversity to ents that depend on dep_ent
	for ent in select:
		if dep_ent in model.dependencies[ent] and ent != dep_ent:
			# check that ent and div_ent are not both resources (resource can't depend on a different resource)
			if not (model.ent_types[ent] == ENTTYPE.RESOURCE and model.ent_types[div_ent] == ENTTYPE.RESOURCE):
				model.dependencies[ent].insert(0, div_ent)
			
				update_res_sts_after_treatment(model, ent, dep_ent)
			
	return model
	
def add_dispersion(model_old, model_new, dis_ents):#, deps_keep=[]):
	"""
	Disperse some of the entities in the model.
	
	Arguments:
	model_old -- the GMORModel before the dispersion
	model_new -- a GMORModel containing the dispersed entities
	             and possibly other entities not in model_old
	dis_ents -- the dispersed entities
	
	Return values:
	model -- the model after the dispersion, including all of the original entities (GMORModel instance)
	
	Exceptions:
	ValueError -- raised when entities in dis_ents are not entities of model_old or model_new
	"""
	if not model_old.are_ents(dis_ents):
		raise ValueError('Cannot disperse non-entities')
	if not model_new.are_ents(dis_ents):
		raise ValueError('Missing dispersed entities in new model')
	model = copy.deepcopy(model_old)
	
	#old_deps = {}  # deps of dis_ents in old model
	for ent in dis_ents:
		model.entities.remove(ent)
		#old_deps[ent] = model.dependencies.pop(ent)
		model.dependencies.pop(ent)
		model.resultant_states.pop(ent)
		
	model.merge_models(model_new)  # add entities of model_new
	
	'''
	for dependencies in deps_keep:
		ent, dep = dependencies
		if model_new.is_ent(ent) and dep in old_deps[ent]:
			model.dependencies[ent].append(dep)
			#would need to update resultant states of ent
	'''
	return model