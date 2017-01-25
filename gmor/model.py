"""
model.py

__author__ = "David Bristow, Alison Goshulak"
__copyright__ = "Copyright 2016"
__credits__ = []
__maintainer__ = "David Bristow"
__status__ = "Development"
"""
#pylint: disable=too-many-arguments
#pylint: disable=too-many-instance-attributes
#pylint: disable=trailing-whitespace
#import csv
#import random
#import itertools
import copy
import re
from datetime import date
import time
import os
import json
import pickle
import matplotlib.pylab as plt
import numpy as np
#import statemachine6

#from scipy.stats import lognorm
#from gmor.stats import findAlphaXmin

def get_bin_list(num, n_var):
	"""
	Generate a binary value as a list of 1s and 0s from a decimal number.
	
	Arguments:
	num -- the decimal number
	n_var -- the number of bits in the binary value
	
	Return values:
	state -- the binary value (list)
	"""
	binary = np.binary_repr(num, width=n_var)
	b_state = str(binary)
	state = list(b_state)
	state = map(int, state)
	return state

def get_bin_lists(n_var):
	"""
	Generate binary values as lists of 1s and 0s for a given number of bits.
	
	Arguments:
	n_var -- the number of bits in each binary value
	
	Return values:
	states -- the list of binary values (list)
	"""
	states = []
	i = 0
	for i in range(2**n_var):
		binary = np.binary_repr(i, width=n_var)
		b_state = str(binary)
		state = list(b_state)
		state = map(int, state)
		states.append(state)
	return states

def get_dec_from_bin_arr(arr):
	"""
	Calculate the decimal value equivalent to a given array of 1s and 0s.
	
	Arguments:
	arr -- a binary value represented by a list of 1s and 0s
	
	Return values:
	res -- the decimal number equal to the binary value (int)
	"""
	i = 0
	res = 0
	for val in arr[::-1]:
		res += val*(2**i)
		i += 1
	return res

def valid_state(state, st_len, verbose=False):
	"""
	Determine if the state is properly formed.
	
	Arguments:
	state -- a list of zeros and or ones representing entity states
	st_len -- the length that state should be
	
	Keyword arguments:
	verbose -- activate throwing errors with descriptive messages (default False)
	
	Return values:
	True -- if state is right length with values equal to 0 or 1
	False -- otherwise
	
	Exceptions:
	ValueError -- raised when verbose mode on and states are invalid
	"""
	if len(state) != st_len:
		if verbose:
			raise ValueError('Length of states should be ', st_len)
		return False
	if not (set(state) == set([0, 1]) or set(state) == set([0]) or set(state) == set([1])):
		if verbose:
			raise ValueError('Each state must be 0 or 1')
		return False
	return True

def is_all_non_neg(a_list):
	"""
	Determine if all the values in a list are non-negative.
	
	Arguments:
	a_list -- a list of decimal values
	
	Return values:
	True -- if all values in a_list are all 0 or greater
	False -- otherwise
	"""
	if sum([1 for i in a_list if i < 0]) == 0:
		return True
	return False
	
class ENTTYPE:
	"""
	ENTYPE: Permitted entity types
	"""
	
	FUNCTION = 'function'
	ANTECEDENT = 'antecedent'
	RESOURCE = 'resource'
	SYSTEM = 'system'
	EVENT = 'event'
	TIME = 'time'
	TYPES = (FUNCTION, ANTECEDENT, RESOURCE, SYSTEM, EVENT, TIME)

class GMORModel(object):
	"""
	Builds and modifies a GMOR entity model.
	
	Public methods:
	set_and_check, set_and_check_json, is_ent, are_ents, is_dep, valid_res_sts,
	n_dep_of_ent, num_res_sts, num_ents, get_ents_with_internal_dep, valid_parent,
	ents_ready, deps_ready, res_sts_ready, res_lm_ready, op_p_ready, ready,
	add_entity, add_dep, merge_models, set_res_sts, set_op_perf_levs, set_res_lim,
	del_entity,	del_dep, edit_entity
	
	Instance variables:
	entities, ent_types, parents, dependencies, resultant_states,
	resource_limits, op_performance_levels
	"""
	
	def __init__(self):
		"""
		Constructs a new (and initially empty) model.
		"""
		self.entities = []
		self.ent_types = {}
		self.parents = {}
		self.dependencies = {}
		self.resultant_states = {}
		self.resource_limits = {}
		self.op_performance_levels = {}

	def set_and_check(self, entities, ent_types, parents, dependencies, resultant_states, 
	                  resource_limits, op_performance_levels):
		"""
		Set model with given values and check that it's ready for analysis.
		
		Arguments:
		entities -- the entities that will populate the model
		ent_types -- the type of each entity in the model
		parents -- the parent of each entity (can be another entity, a type, or blank)
		dependencies -- for each entity, the list of entities it depends on
		resultant_states -- for each entity, a list of states resulting from the state of it's dependencies
		resource_limits -- the total amount available of each resource entity
		op_performance_levels -- the performance level of each function entity when active
		
		Return values:
		True -- if the model is ready for analysis
		False -- otherwise
		"""
		self._set(entities, ent_types, parents, dependencies, resultant_states, 
		          resource_limits, op_performance_levels)

		if self.ready():
			return True
		return False

	def set_and_check_json(self, json_text):
		"""
		Set model with given values from JSON text and check that it's ready for analysis.
		
		Arguments:
		json_text -- the JSON text containing values for the model variables
		
		Return values:
		True -- if the model is ready for analysis
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when JSON text is not in the proper form
		"""
		try:
			obj = json.loads(json_text)
			entities = obj['entities']
			ent_types = obj['ent_types']
			parents = obj['parents']
			dependencies = obj['dependencies']
			resultant_states = obj['resultant_states']
			resource_limits = obj['resource_limits']
			op_performance_levels = obj['op_performance_levels']
			
			for ent in entities:
				if type(resultant_states[ent]).__module__ != np.__name__:
					resultant_states[ent] = np.array(resultant_states[ent])
			
			return self.set_and_check(entities, ent_types, parents, dependencies, resultant_states, 
			                          resource_limits, op_performance_levels)
		except:
			raise ValueError('json text must be of form' + \
				'"entities": [], ' + \
				'"ent_types": {}, ' + \
				'"parents": {}, ' + \
				'"dependencies": {}, ' + \
				'"resultant_states": {}, ' + \
				'"resource_limits": {}, ' + \
				'"op_performance_levels": {}')


	def _set(self, entities, ent_types, parents, dependencies, resultant_states, 
	             resource_limits, op_performance_levels):
		"""
		Set the model variables with the given values.
		
		Arguments:
		entities -- the entities that will populate the model
		ent_types -- the type of each entity in the model
		parents -- the parent of each entity (can be another entity, a type, or blank)
		dependencies -- for each entity, the list of entities it depends on
		resultant_states -- for each entity, a list of states resulting from the state of it's dependencies
		resource_limits -- the total amount available of each resource entity
		op_performance_levels -- the performance level of each function entity when active
		"""
		self.entities = entities
		self.ent_types = ent_types
		self.parents = parents
		self.dependencies = dependencies
		self.resultant_states = resultant_states
		self.resource_limits = resource_limits
		self.op_performance_levels = op_performance_levels

	def formatted_json_text(self):
		"""
		Useful for saving GMORModel models as json strings that are human readable.
		Creates a string that prints nicely in json format (but is not a json loaded object). 
		"""
		out = ''
		out += '{\n'
		for key in self.__dict__:
			if key != "entities":
				out += "\t\""+key+"\":{\n"
				do_fix = False
				for ent in self.__dict__[key]:
					do_fix = True
					out += "\t\t\""+ent+"\":"
					if key == "resultant_states":
						out += str(list(self.resultant_states[ent]))+",\n"
					elif key == "dependencies" or key == "parents" or key == "ent_types":
						out += json.dumps(self.__dict__[key][ent]) + ',\n'
					else:
						out += str(self.__dict__[key][ent])+",\n"
				if do_fix:
					out = out[:-2]
					out += '\n'
				out += "\t},\n"
			else:
				out += "\t\""+key+"\":[\n"
				for ent in self.entities:
					out += "\t\t\""+ent+"\","
					out += '\n'
				out = out[:-2]
				out += '\n'
				out += '\t],\n'
		out = out[:-2]
		out += '\n'
		out += '}'
		return out
	#CHECKS

	def is_ent(self, ent):
		"""
		Check if it is an entity of the model.
		
		Arguments:
		ent -- the string name of the potential entity
		
		Return values:
		True -- if ent is an entity
		False -- otherwise
		"""
		if ent in self.entities:
			return True
		return False

	def are_ents(self, ents):
		"""
		Checks if all are entities of the model.
		
		Arguments:
		ents -- a list of names for potential entities
		
		Return values:
		True -- if all values in ents exist in model
		Fales -- otherwise
		"""
		for ent in ents:
			if self.is_ent(ent) is False:
				return False
		return True

	def is_dep(self, ent, dep):
		"""
		Check if one entity is a dependency of another.
		
		Arguments:
		ent -- an entity with a possible dependency on dep
		dep -- a possible dependency of ent
		
		Return values:
		True -- if dep is a dependency of ent
		False -- otherwise
		"""
		if dep in self.dependencies[ent]:
			return True
		return False

	def valid_res_sts(self, ent, state, verbose=False):
		"""
		Check if they are valid resultant states for the entity.
		
		Arguments:
		ent -- the entity
		state -- the list of resultant states being checked
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if state is a valid list of resultant states for ent
		        (a numpy array of the right length with values equal to 0 or 1)
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and the resultant states are invalid
		"""
		if not type(state).__module__ == np.__name__:
			if verbose:
				raise ValueError('States must be in a numpy array')
			return False
		if not self.is_ent(ent):
			if verbose:
				raise ValueError('Not an entity of the model')
			return False
		return valid_state(state, self.num_res_sts(ent), verbose)
		


	#INFO

	def n_dep_of_ent(self, ent):
		"""
		Calculate number of dependencies of an entity.
		
		Arguments:
		ent -- the entity
		
		Return values:
		the number of dependencies of ent (int)
		
		Exceptions:
		ValueError -- raised if ent not in model
		"""
		if self.is_ent(ent):
			return len(self.dependencies[ent])
		raise ValueError('ent invalid for num of dep check')

	def num_res_sts(self, ent):
		"""
		Calculate number of resultant states of an entity.
		
		Arguments:
		ent -- the entity
		
		Return values:
		the number of entity resultant states for ent (int)
		
		Exceptions:
		ValueError -- raised if ent not in model
		"""
		if self.is_ent(ent):
			return 2**self.n_dep_of_ent(ent)
		raise ValueError('ent invalid for num states check')

	def num_ents(self):
		"""
		Calculate the number of entities in the model.
		
		Return values:
		the number of entities (int)
		"""
		return len(self.entities)
		
	def get_ents_with_internal_dep(self):
		"""
		Find entities with an internal dependency (that depend on an internal state).
		
		Return values:
		the entities with an internal dependency (list)
		"""
		return [ent for ent in self.entities if ent in self.dependencies[ent]]

	def _valid_parent(self, parent):
		"""
		Check if it is a valid parent name.
		
		Arguments:
		parent -- the string name being checked
		
		Return values:
		True -- if parent is an eligible parent name
		False -- otherwise
		"""
		return parent == '' or self.is_ent(parent) or parent in ENTTYPE.TYPES

	def valid_parent(self, ent, parent):
		"""
		Check if it is a valid parent for the entity.
		
		Arguments:
		ent -- the entity
		parent -- the parent name being checked
		
		Return values:
		True -- if parent is an eligible parent name (either another entity, a type, or blank)
		False -- otherwise
		
		Exceptions:
		ValueError -- raised if ent not in model or ent and parent are the same
		"""
		if self.is_ent(ent) and ent != parent:
			return self._valid_parent(parent)
		raise ValueError('ent invalid')

	def _are_functions(self, ents):
		"""
		Check whether all are of type function.
		
		Arguments:
		ents -- the list of entities being checked
		
		Return values:
		True -- if all entities in ents are functions
		False -- otherwise
		"""
		for ent in ents:
			if self.ent_types[ent] != ENTTYPE.FUNCTION:
				return False
		return True




	#FINAL CHECKS

	def ents_ready(self, verbose=False):
		"""
		Check if entities are ready.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if entities are valid (at least one exists in model, at least one is a function,
		        and all names do not contain any of the following chars: \, /, *, ?, <, >, |, %, ")
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and entities are not valid
		"""
		if len(self.entities) == 0:
			if verbose:
				raise ValueError('Model has no entities')
			return False
		illegal = re.compile('[/*?<>|%"\\\\]')
		for ent in self.entities:
			if re.search(illegal, "%r"%ent):
				if verbose:
					msg = 'Entity names cannot contain the following: \\, /, *, ?, <, >, |, %, "'
					raise ValueError(msg)
				return False
		if not ENTTYPE.FUNCTION in self.ent_types.values():
			if verbose:
				raise ValueError('Model has no functions')
			return False
		return True

	def deps_ready(self, verbose=False):
		"""
		Check if dependencies are ready.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if dependencies of each entity are valid (every entity has at least one dependency, at least
        		one entity has an internal dependency, and resources do not depend on other resources)
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and dependencies are not valid
		"""
		internal_deps = 0
		for ent in self.entities:
			if len(self.dependencies[ent]) == 0:
				if verbose:
					raise ValueError('Entity with no dependency')
				return False #every entity must have at least one dependency
			if self.ent_types[ent] == ENTTYPE.RESOURCE:
				for dep in self.dependencies[ent]:
					if self.ent_types[dep] == ENTTYPE.RESOURCE and ent != dep:
						if verbose:
							raise ValueError('Resource depending on another distinct resource')
						return False  # resource cannot depend on a different resource
			if ent in self.dependencies[ent]:
				internal_deps += 1
		if internal_deps == 0:
			if verbose:
				raise ValueError('No entities with internal dependency')
			return False  # must have at least one internally-dependent entity
		return True

	def res_sts_ready(self, verbose=False):
		"""
		Check if resultant states are ready.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if resultant states of each entity are valid
		        (a numpy array of the right length with values equal to 0 or 1)
		False -- otherwise
		"""
		for ent in self.entities:
			if not self.valid_res_sts(ent, self.resultant_states[ent], verbose):
				return False
		return True

	def res_lm_ready(self, verbose=False):
		"""
		Check if resource limits are ready.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if resource limits are valid (non-negative and only for resource entities)
		False -- otherwise
		"""
		return self._res_lm_ready(self.resource_limits, verbose)

	def _res_lm_ready(self, res_lims, verbose=False):
		"""
		Check if resource limits are ready.
				
		Arguments:
		res_lims -- the resource limits for the resources in the model
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if resource limits are valid (non-negative and only for resource entities)
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and limits are not valid
		"""
		if not self.are_ents(res_lims.keys()):
			if verbose:
				raise ValueError('Not all entities of the model')
			return False
		if not is_all_non_neg(res_lims.values()):
			if verbose:
				raise ValueError('Not all non-negative values')
			return False
		for res_ent in res_lims.keys():
			if self.ent_types[res_ent] != ENTTYPE.RESOURCE:#ENTTYPE_RESOURCE:
				if verbose:
					raise ValueError('Not all resources')
				return False
		return True

	def op_p_ready(self, verbose=False):
		"""
		Check if performance levels are ready.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if performance levels are valid (only for function entities
		        and sum of values is between 0.9999999999 and 0.0000000001)
		False -- otherwise
		"""
		return self._op_p_ready(self.op_performance_levels, verbose)

	def _op_p_ready(self, op_perf_levs, verbose=False):
		"""
		Check if performance levels are ready.
		
		Arguments:
		op_perf_levs -- the performance levels of the functions in the model
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if performance levels are valid (only for function entities
		        and sum of values is between 0.9999999999 and 0.0000000001)
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and levels are not valid
		"""
		if not self._are_functions(op_perf_levs.keys()):
			if verbose:
				raise ValueError('Not all functions')
			return False
		if abs(sum(op_perf_levs.values())-1.0) > 1.0e-10:
			if verbose:
				raise ValueError('Sum of levels not between 0.9999999999 and 0.0000000001')
			return False
		return True

	def ready(self, verbose=False):
		"""
		Check if model is ready for analysis.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if minimum entry requirements complete (entities, dependencies,
			    resultant states, performance levels, and resource limits all ready)
		False -- otherwise
		"""
		if self.ents_ready(verbose) and self.deps_ready(verbose) and self.res_sts_ready(verbose):
			if self.op_p_ready(verbose) and self.res_lm_ready(verbose):
				return True
		return False




	#ADDITIONS
	def add_entity(self, name, ent_type, parent=''):
		"""
		Add a new entity to the model.
		
		Arguments:
		name -- string name of the new entity
		ent_type -- the type of the new entity
		
		Keyword arguments:
		parent -- the parent name of the new entity (default '';
		          parent will be set to same value as ent_type)
		
		Return values:
		True -- if entity added
		False -- if entity already exists, type is invalid, or parent is invalid
		"""
		if (not self.is_ent(name) and ent_type in ENTTYPE.TYPES and
			   self._valid_parent(parent) and parent != name):

			self.entities.append(name)
			self.ent_types[name] = ent_type
			if parent == '':
				parent = ent_type
			self.parents[name] = parent
			self.dependencies[name] = []
			self.resultant_states[name] = []
			return True
		else:
			return False
			
	def add_dep(self, ent, dep_name):
		"""
		Add a new dependency relationship between two entities.
		
		Arguments:
		ent -- the entity with the new dependency on dep_name
		dep_name -- the entity that will be added to ent's list of dependencies
		
		Return values:
		True -- if dependency on dep_name added to ent 
		False -- if the dependency already exists, if ent or dep_name are not entities,
				 or if they're both resources that are distinct from one another
		"""
		if self.is_ent(ent) and self.is_ent(dep_name) and self.is_dep(ent, dep_name) == False:
			if self.ent_types[ent] == ENTTYPE.RESOURCE and self.ent_types[dep_name] == ENTTYPE.RESOURCE:
				if ent != dep_name:
					return False
			self.dependencies[ent].append(dep_name)
			self._set_default_res_sts(ent)
			return True
		return False
		
	def merge_models(self, new_model, weight=0.5):
		"""
		Add entities of another model to this model.
		
		Arguments:
		new_model -- the other GMORModel being merged into this model
		
		Keyword arguments:
		weight -- used to adjust performance levels to sum to 1 after merge (default 0.5)
		
		Exceptions:
		ValueError -- raised when new_model is not ready
		"""
		if not new_model.ready():
			raise ValueError('Must pass in a model ready for analysis')
		for ent in new_model.entities:
			if self.is_ent(ent):
				raise ValueError('Models cannot share any entities')
			
		#adjust performance levels of functions in this model	
		for ent in self.op_performance_levels.keys():
			self.op_performance_levels[ent] = self.op_performance_levels[ent]*weight
		for ent in new_model.entities:
			self.entities.append(ent)
			self.ent_types[ent] = new_model.ent_types[ent]
			self.parents[ent] = new_model.parents[ent]
			self.dependencies[ent] = new_model.dependencies[ent]
			self.resultant_states[ent] = new_model.resultant_states[ent]
			if ent in new_model.resource_limits:
				self.resource_limits[ent] = new_model.resource_limits[ent]
			if ent in new_model.op_performance_levels:
				self.op_performance_levels[ent] = new_model.op_performance_levels[ent]*(1.0-weight)
	
	
	#SETTINGS
	def _set_default_res_sts(self, ent):
		"""
		Set default resultant states for an entity (states will all be zero).
		
		Arguments:
		ent -- the entity
		
		Exceptions:
		ValueError -- raised if ent is not in model
		"""
		if self.is_ent(ent):
			self.resultant_states[ent] = np.zeros(self.num_res_sts(ent), dtype=int)
		else:
			raise ValueError('resultant states default cannot be set for invalid ent')
			
	def set_res_sts(self, ent, states, verbose=False):
		"""
		Set new resultant states for an entity.
		
		Arguments:
		ent -- the entity
		states -- the new resultant states for ent
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if states copied in
		False -- if ent does not exist, states length is not 2**len(dep of ent)
			     or values of states are not all 0 or 1
		"""
		if self.valid_res_sts(ent, states, verbose):
			self.resultant_states[ent] = copy.copy(states)
			return True
		return False
		
	def set_op_perf_levs(self, op_perf_levs, verbose=False):
		"""
		Set new performance levels.
		
		Arguments:
		op_perf_levs -- the new levels
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if op_perf_levs copied in
		False -- if some keys of op_perf_levs are not functions,
		         or the sum of values is not between 0.9999999999 and 0.0000000001
		"""
		if self._op_p_ready(op_perf_levs, verbose):
			self.op_performance_levels = copy.copy(op_perf_levs)
			return True
		return False
		
	def set_res_lim(self, res_lim, verbose=False):
		"""
		Set new resource limits.
		
		Arguments:
		res_lim -- the new resource limits
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if res_lim copied in
		False -- if some keys of res_lim are not resources,
		         or values are not all non-negative
		"""
		if self._res_lm_ready(res_lim, verbose):
			self.resource_limits = copy.copy(res_lim)
			return True
		return False
	
	
	
	
	#DELETIONS
	def del_entity(self, name):
		"""
		Delete entity and track affected entities.
		
		Arguments:
		name -- the name of the entity
		
		Return values:
		all the entities that used to depend on the deleted entity (list)
		
		Exceptions:
		ValueError -- raised if ent does not exist in model
		"""
		if self.is_ent(name):
			affected_ents = []
			self.entities.remove(name)
			self.dependencies.pop(name)
			self.parents.pop(name)
			self.resultant_states.pop(name)
			if self.ent_types[name] == ENTTYPE.FUNCTION:
				self.op_performance_levels.pop(name)
			elif self.ent_types[name] == ENTTYPE.RESOURCE:
				self.resource_limits.pop(name)
			self.ent_types.pop(name)
			for ent in self.entities:
				if name in self.dependencies[ent]:
					n_dep = len(self.dependencies[ent])-1
					affected_ents.append(ent)
					self.dependencies[ent].remove(name)
					self.resultant_states[ent] = np.array([0 for i in range(2**n_dep)]) # pylint: disable=unused-variable
			return affected_ents
		raise ValueError('not an entity')
	
	def del_dep(self, ent, dep):
		"""
		Delete dependency relationship between two entities.
		
		Arguments:
		ent -- the entity that used to depend on dep
		dep_name -- the entity that will be removed from ent's list of dependencies
		
		Return values:
		True -- if dependency removed
		False -- if ent or dep is not an entity, or the dependency relationship doesn't exist
		"""
		if self.is_ent(ent) and self.is_ent(dep) and self.is_dep(ent, dep):
			self.dependencies[ent].remove(dep)
			#self.resultantStates[ent] = []
			self._set_default_res_sts(ent)
			return True
		return False
	


	
	#EDITS
	def _edit_ent_type(self, ent, new_ent_type):
		"""
		Change the type of an entity.
		
		Arguments:
		ent -- the entity
		new_ent_type -- the new type of ent
		
		Return values:
		True -- if ent's type has been changed to new_ent_type
		False -- if ent is not an entity, new_ent_type is not a valid type,
		         new_ent_type is the same as ent's current type, or the new type
				 is resource and ent depends on another resource
		"""
		if self.is_ent(ent) and new_ent_type in ENTTYPE.TYPES and new_ent_type != self.ent_types[ent]:
			if new_ent_type == ENTTYPE.FUNCTION:
				self.op_performance_levels[ent] = 0.0
			elif new_ent_type == ENTTYPE.RESOURCE:
				for dep in self.dependencies[ent]:
					if dep != ent and self.ent_types[dep] == ENTTYPE.RESOURCE:
						return False
				self.resource_limits[ent] = 0
				
			if self.ent_types[ent] == ENTTYPE.FUNCTION:
				del self.op_performance_levels[ent]
			elif self.ent_types[ent] == ENTTYPE.RESOURCE:
				del self.resource_limits[ent]			

			self.ent_types[ent] = new_ent_type
				
			return True
		return False
		
	def _edit_parent(self, ent, new_parent):
		"""
		Change the parent of an entity.
		
		Arguments:
		ent -- the entity
		new_parent -- the new parent of ent
		
		Return values:
		True -- if ent's parent has been changed to new_parent
		False -- if new_parent is not a valid parent name or is the same
		         as ent's current parent
		"""
		if self.valid_parent(ent, new_parent) and new_parent != self.parents[ent]:
			self.parents[ent] = new_parent
			return True
		return False
		
	def edit_entity(self, ent, new_ent_type, new_ent_parent):
		"""
		Change the parent or the type (or both) of an entity.
		
		Arguments:
		ent -- the entity
		new_ent_type -- the new type of ent
		new_ent_parent -- the new parent of ent
		
		Return values:
		True -- if the parent or the type of ent changed
		False -- otherwise
		"""		
		edited = False
		
		if self._edit_parent(ent, new_ent_parent):
			edited = True
		if self._edit_ent_type(ent, new_ent_type):
			edited = True			
		return edited
		
class GMORScenarioModel(object):
	"""
	Builds and modifies a scenario model based on the properties of a GMORModel.
	
	Public methods:
	reset, set_and_check, set, valid_states, valid_internal_states,
	valid_realized_timelines, valid_efforts, valid_deadlines, cur_int_st_ready, rlzd_time_ready,
	rlzd_ex_ready, eff_ready, deads_ready, ready, set_current_internal_states, set_realized_timelines,
	set_realized_exit_by_ent, set_realized_exits, set_effort_by_resource, set_deadlines, set_new_scen_model
						
	Instance variables:
	model, name, current_internal_states, realized_timelines, realized_exits, efforts, deadlines
	"""
	
	def __init__(self, model, name):
		"""
		Constructs a scenario model.
		
		Arguments:
		model -- GMORModel the scenario will be based on
		name -- identifier of scenario model
		
		Exceptions:
		ValueError -- raised when GMORModel is not ready for analysis
		"""
		if model.ready():
			self.model = model
		else:
			raise ValueError('must send in a model ready for analysis')
		self.reset(model)
		self.name = name
		
	def reset(self, model):
		"""
		Reset scenario conditions.
		
		Arguments:
		model -- GMORModel the scenario is based on		
		"""
		self.current_internal_states = {}
		self.realized_timelines = {}
		self.realized_exits = {}
		self.efforts = {}
		self.deadlines = {}
		for ent in model.entities:
			if ent in model.dependencies[ent]:  # if entity is dependent of itself
				self.current_internal_states[ent] = 1
				self.realized_exits[ent] = -1
			self.realized_timelines[ent] = 0.0
			if model.ent_types[ent] != ENTTYPE.RESOURCE:  # if entity is not a resource
				for dep in model.dependencies[ent]:
					if model.ent_types[dep] == ENTTYPE.RESOURCE:  # if dependency of entity is a resource
						if self.efforts.has_key(ent) == False:  # if first found resource dependency of ent
							self.efforts[ent] = {}
						self.efforts[ent][dep] = 0  #{ent:{dep:0},...}
			if model.ent_types[ent] == ENTTYPE.FUNCTION:
				self.deadlines[ent] = 0.0
				
	def set_and_check(self, model, current_internal_states,
					              realized_timelines, realized_exits, efforts, deadlines):
		"""
		Set up scenario model and check if it's ready for analysis.
		
		Arguments:
		model -- GMORModel the scenario is based on
		current_internal_states -- state of internally dependent entities
								   (0 for unavailable, 1 for available)
		realized_timelines -- time it takes for an entity's state to change once it's dependencies are met
		realized_exits -- amount of time an internal dependency of an entity is available
		efforts -- number of units of a resource dependency an entity requires
		deadlines -- for function entities, the time that the entity must be active by
		
		Return values:
		True -- if scenario model is ready for analysis
		False -- otherwise
		"""
		self.set(model, current_internal_states, realized_timelines, realized_exits, efforts, deadlines)
		if self.ready():
			return True
		return False
		
	def set(self, model, current_internal_states, realized_timelines, realized_exits, efforts, deadlines):
		"""
		Set up scenario model with given conditions.
		
		Arguments:
		model -- GMORModel the scenario is based on
		current_internal_states -- state of internally dependent entities
								   (0 for unavailable, 1 for available)
		realized_timelines -- time it takes for an entity's state to change once it's dependencies are met
		realized_exits -- amount of time an internal dependency of an entity is available
		efforts -- number of units of a resource dependency an entity requires
		deadlines -- for function entities, the time that the entity must be active by
		
		Exceptions:
		ValueError -- raised when GMORModel is not ready for analysis
		"""
		if model.ready():
			self.model = model
		else:
			raise ValueError('must send in a model ready for analysis')
		self.current_internal_states = current_internal_states
		self.realized_timelines = realized_timelines
		self.realized_exits = realized_exits
		self.efforts = efforts
		self.deadlines = deadlines
		
	#CHECKS
	def valid_states(self, arr):
		"""
		Check states of entities are valid.
		
		Arguments:
		arr -- the states
		
		Return values:
		True -- if states are valid (i.e. either 0 or 1 and not empty)
		False -- otherwise
		"""
		if set(arr) == set([0, 1]) or set(arr) == set([0]) or set(arr) == set([1]): 
			return True
		return False
		
	def _valid_internal_states(self, int_states, model, verbose=False):
		"""
		Check internal states of entities are valid and match with dependencies.
		
		Arguments:
		int_states -- current internal states of the entities
		model -- GMORModel scenario is based on
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if states are valid (i.e. either 0 or 1) and match dependencies
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and internal states are invalid
		"""
		if not model.are_ents(int_states.keys()):
			if verbose:
				raise ValueError('Not all entities of the model')
			return False
		if not self.valid_states(int_states.values()):
			if verbose:
				raise ValueError('Invalid states (must be 0 or 1)')
			return False
		for ent in int_states.keys():
			if ent not in model.dependencies[ent]:
				if verbose:
					raise ValueError('Not an internally-dependent entity')
				return False
		return True
		
	def valid_internal_states(self, int_states, verbose=False):
		"""
		Check internal states of entities are valid and match with dependencies.
		
		Arguments:
		int_states -- current internal states of the entities
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if states are valid (i.e. either 0 or 1) and match dependencies
		False -- otherwise
		"""
		return self._valid_internal_states(int_states, self.model, verbose)
		
	def valid_realized_timelines(self, timelines, verbose=False):
		"""
		Check time lines of entities are valid.
		
		Arguments:
		timelines -- realized time lines of the entities
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if each entity of GMORModel has a valid (i.e. non-negative) time line
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and time lines are invalid
		"""
		if not self.model.are_ents(timelines.keys()):
			if verbose:
				raise ValueError('Not all entities of the model')
			return False
		if not is_all_non_neg(timelines.values()):
			if verbose:
				raise ValueError('Negative time lines invalid')
			return False
		for ent in self.model.entities:
			if ent not in timelines.keys():
				if verbose:
					raise ValueError('Missing time line for an entity')
				return False
		return True
		
	def valid_efforts(self, efforts, verbose=False):
		"""
		Check efforts of entities are valid and match with dependencies.
		
		Arguments:
		efforts -- efforts of the entities
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if efforts of each entity are valid (i.e. non-negative) and match dependencies
				(efforts for resource entities cannot be included)
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and efforts are invalid
		"""
		#print '1',self.model.are_ents(efforts.keys())
		if self.model.are_ents(efforts.keys()):
			for ent in efforts.keys():
				#print '5',is_all_non_neg(efforts[ent].values()) == False
				if is_all_non_neg(efforts[ent].values()) == False:
					if verbose:
						raise ValueError('Negative efforts invalid')
					return False
				if self.model.ent_types[ent] == ENTTYPE.RESOURCE:  # efforts for resources not allowed
					if verbose:
						raise ValueError('Cannot have efforts for resource entities')
					return False
				for dep_ent in efforts[ent].keys():
					eff_val = efforts[ent][dep_ent]
					#print '2',eff_val < 0
					#if eff_val < 0:
						#return False
					#print '3',self.model.is_dep(ent,dep_ent) == False
					#print '4',self.model.ent_types[dep_ent]# != ENTTYPE.RESOURCE
					if self.model.is_dep(ent, dep_ent) == False:
						if verbose:
							raise ValueError('Entity does not depend on resource')
						return False
					if self.model.ent_types[dep_ent] != ENTTYPE.RESOURCE:
						if verbose:
							raise ValueError('Dependency not a resource entity')
						return False
			return True
		if verbose:
			raise ValueError('Not all entities of the model')
		return False
		
	def _valid_realized_exits(self, rlzd_exits, verbose=False):
		"""
		Check realized exits of entities are valid and match with dependencies.
		
		Arguments:
		rlzd_exit -- realized exits of the entities
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if realized exits are valid (i.e. either -1 or non-negative) and match dependencies
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and exits are invalid
		"""
		if self.model.are_ents(rlzd_exits.keys()):	
			for ent in rlzd_exits.keys():
				if ent not in self.model.dependencies[ent]:
					if verbose:
						raise ValueError('Not an internally-dependent entity')
					return False
				if rlzd_exits[ent] < 0.0 and rlzd_exits[ent] > -1:
					if verbose:
						raise ValueError('Exit between -1 and 0 invalid')
					return False
				if rlzd_exits[ent] < -1:
					if verbose:
						raise ValueError('Exit less than -1 invalid')
					return False
			return True
		if verbose:
			raise ValueError('Not all entities of the model')
		return False
	
	def valid_deadlines(self, deadlines, verbose=False):
		"""
		Check if deadlines are valid.
		
		Keyword arguments:
		deadlines -- deadlines of the function entities
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if deadlines of each entity are valid (not empty, keys are ents, and no negative values)
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and deadlines are not valid
		"""
		if len(deadlines.keys()) == 0:
			if verbose:
				raise ValueError('No deadlines')
			return False
		if not self.model.are_ents(deadlines.keys()):
			if verbose:
				raise ValueError('Not all entities of the model')
			return False
		if not is_all_non_neg(deadlines.values()):
			if verbose:
				raise ValueError('Not all non-negative values')
			return False
		return True
		
	#FINAL CHECKS
	def cur_int_st_ready(self, verbose=False):
		"""
		Check that the current internal states are ready for analysis.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the states are ready
		False -- otherwise
		"""
		return self.valid_internal_states(self.current_internal_states, verbose)
		
	def rlzd_time_ready(self, verbose=False):
		"""
		Check that the realized time lines are ready for analysis.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the time lines are ready
		False -- otherwise
		"""
		return self.valid_realized_timelines(self.realized_timelines, verbose)
		
	def rlzd_ex_ready(self, verbose=False):
		"""
		Check that the realized exits are ready for analysis.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the exits are ready
		False -- otherwise
		"""
		return  self._valid_realized_exits(self.realized_exits, verbose)
		
	def eff_ready(self, verbose=False):
		"""
		Check that the efforts are ready for analysis.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the efforts are ready
		False -- otherwise
		"""
		return self.valid_efforts(self.efforts, verbose)
		
	def deads_ready(self, verbose=False):
		"""
		Check if deadlines are ready.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if deadlines are ready
		False -- otherwise
		"""
		return self.valid_deadlines(self.deadlines, verbose)
		
	def ready(self, verbose=False):
		"""
		Check that the scenario model is ready for analysis.
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the scenario model is ready
		False -- otherwise
		"""
		if (self.cur_int_st_ready(verbose) and self.rlzd_time_ready(verbose)
    		and self.rlzd_ex_ready(verbose) and self.eff_ready(verbose) and self.deads_ready(verbose)):
			return True
		return False
		
	#SETTINGS
	def set_current_internal_states(self, curr_int_sts, verbose=False):
	#must be comprised of existing entities with internal dependencies and states equal to 0 or 1
		"""
		Set new internal states.
		
		Arguments:
		curr_int_sts -- the new states of entities with internal dependence
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the new states are valid and have been copied in
		False -- otherwise
		"""
		#if self.model.are_ents(curr_int_sts.keys()) and self.valid_states(curr_int_sts.values()):
		#	for ent in curr_int_sts:
		#		if ent not in self.model.dependencies[ent]:
		#			return False
		if self.valid_internal_states(curr_int_sts, verbose):
			self.current_internal_states = copy.copy(curr_int_sts)
			return True
		return False
		
	def set_realized_timelines(self, rlzd_times, verbose=False):# must include all ents of model with non-zero time
		"""
		Set new realized time lines.
		
		Arguments:
		rlzd_times -- the new time lines of the entities
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the new time lines are valid and have been copied in
		False -- otherwise
		"""
		#if self.model.are_ents(rlzd_times.keys()) and is_all_non_neg(rlzd_times.values()):
		#	for ent in self.model.entities:
		#		if ent not in rlzd_times.keys():
		#			return False
		if self.valid_realized_timelines(rlzd_times, verbose):
			self.realized_timelines = copy.copy(rlzd_times)
			return True
		return False
		
	def set_realized_exit_by_ent(self, ent, rlzd_exit, verbose=False):
		"""
		Set a new realized exit for an entity.
		
		Arguments:
		ent -- the entity
		rlzd_exit -- the new exit for ent
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if rlzd_exit is valid (entity has an internal dependence
		        and time is >=0.0 or ==-1) and has been copied in
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and new exit cannot be set
		"""
		if not self.model.is_ent(ent):
			if verbose:
				raise ValueError('Not an entity of the model')
			return False
		if ent not in self.model.dependencies[ent]:
			if verbose:
				raise ValueError('Not an internally-dependent entity')
			return False
		if not (rlzd_exit >= 0.0 or rlzd_exit == -1):
			if verbose:
				raise ValueError('Exit must be either -1 or non-negative')
			return False
		self.realized_exits[ent] = rlzd_exit
		return True
		
		
	def set_realized_exits(self, rlzd_exits, verbose=False):
		"""
		Set new realized exits.
		
		Arguments:
		rlzd_exits -- the new exits of the entities
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the new exits are valid and have been copied in
		False -- otherwise
		"""
		if self._valid_realized_exits(rlzd_exits, verbose):
			self.realized_exits = copy.copy(rlzd_exits)
			return True
		return False
		
	def set_effort_by_resource(self, efforts, resource, verbose=False):
		"""
		Set new efforts corresponding to a resource for entities dependent on the resource.
		
		Arguments:
		efforts -- the new efforts corresponding to resource
		resource -- the shared resource dependency of the affected entities
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if the new efforts are valid (resource is a dependency of each entity in efforts,
		        each new effort is non-negative, and none of the entities in efforts
				are the same entity as resource) and have been copied in
		False -- otherwise
		
		Exceptions:
		ValueError -- raised when verbose mode on and new efforts cannot be set
		"""
		if not self.model.are_ents(efforts.keys()):
			if verbose:
				raise ValueError('Not all entities of the model')
			return False
		if not self.model.is_ent(resource):
			if verbose:
				raise ValueError('Resource not an entity of the model')
			return False
		if not self.model.ent_types[resource] == ENTTYPE.RESOURCE:
			if verbose:
				raise ValueError('Efforts for a non-resource entity')
			return False
		for ent in efforts.keys():
			if not self.model.is_dep(ent, resource):
				if verbose:
					raise ValueError('Entity does not depend on resource')
				return False
			if efforts[ent] < 0.0:
				if verbose:
					raise ValueError('Negative effort invalid')
				return False
			if ent == resource:
				if verbose:
					raise ValueError('Entity in efforts and resource cannot be the same')
				return False
			self.efforts[ent][resource] = efforts[ent]
		return True
	
	def set_deadlines(self, deadlines, verbose=False):
		"""
		Set new deadlines.
		
		Arguments:
		deadlines -- the new deadlines
		
		Keyword arguments:
		verbose -- activate throwing errors with descriptive messages (default False)
		
		Return values:
		True -- if deadlines copied in
		False -- if deadlines are empty, keys of deadlines are not entities,
		         or values are not all non-negative
		
		Exceptions:
		ValueError -- raised when verbose mode on and new deadlines are invalid
		"""
			
		if self.valid_deadlines(deadlines, verbose):
			self.deadlines = copy.copy(deadlines)
			return True
		return False
		
	def set_new_scen_model(self, model):
		"""
		Set new scenario model with a different GMORModel.
		
		Arguments:
		model -- new GMORModel, possibly with some same entities and dependencies
		
		Return values:
		True -- if model is ready for analysis
		False -- otherwise
		"""
		if model.ready():
			#current_internal_states
			new_curr_int_states = {}
			for ent in model.entities:
				if ent in model.dependencies[ent]:
					if ent in self.current_internal_states.keys():
						new_curr_int_states[ent] = self.current_internal_states[ent]  # save internal state for ent
					else:
						new_curr_int_states[ent] = 1
				
			#realized_timelines
			new_realized_timelines = {}
			for ent in model.entities:
				if ent in self.realized_timelines.keys():
					new_realized_timelines[ent] = self.realized_timelines[ent]  # save time line for ent
				else:
					new_realized_timelines[ent] = 0.0
			
			#realized_exits
			new_realized_exits = {}
			for ent in model.entities:
				if ent in model.dependencies[ent]:
					if ent in self.realized_exits.keys():
						new_realized_exits[ent] = self.realized_exits[ent]  # save exit for ent
					else:
						new_realized_exits[ent] = -1
			
			#efforts
			new_efforts = {}
			for ent in model.entities:
				if model.ent_types[ent] != ENTTYPE.RESOURCE:
					for dep in model.dependencies[ent]:
						if model.ent_types[dep] == ENTTYPE.RESOURCE:
							if new_efforts.has_key(ent) == False:
								new_efforts[ent] = {}
							if self.efforts.has_key(ent) and self.efforts[ent].has_key(dep):
								new_efforts[ent][dep] = self.efforts[ent][dep]  # save effort for ent
							else:
								new_efforts[ent][dep] = 0
								
			new_deadlines = {}
			for ent in model.entities:
				if model.ent_types[ent] == ENTTYPE.FUNCTION:
					if ent in self.deadlines.keys():
						new_deadlines[ent] = self.deadlines[ent]  # save deadline for ent
					else:
						new_deadlines[ent] = 0.0
			
			self.model = model
			self.set_current_internal_states(new_curr_int_states)
			self.set_realized_exits(new_realized_exits)
			self.set_realized_timelines(new_realized_timelines)
			self.efforts = copy.copy(new_efforts)
			self.set_deadlines(new_deadlines)
			#self.reset(model)
			
			return True
		return False


class GMORRunner(object):#(GMORModel):
	"""
	Calculate and demonstrate implications of initial conditions set by scenario model.

    Public methods:
    do_progression, plot_performance_curve, check_changes_timing, deterministic_progression,
    next_deadline, get_deps_to_do, max_timing_progression, 

    Instance variables:
    entities, ent_types, dependencies, resultant_states, resource_limits,
    op_performance_levels, entity_lookup, dependencies_lookup
	"""
	def __init__(self, model):
		"""
		Constructs a runner for a given GMORModel.
		
		Arguments:
		model -- the GMORModel the runner is based on
		
		Exceptions:
		ValueError -- raised when model is not ready for analysis
		"""
		if model.ready() is False:
			raise ValueError('must send in a ready model')

		self.entities = model.entities
		self.ent_types = model.ent_types
		self.dependencies = model.dependencies
		self.resultant_states = model.resultant_states
		self.resource_limits = model.resource_limits
		self.op_performance_levels = model.op_performance_levels

		self.entity_lookup = {}
		self.dependencies_lookup = {}

		def _build_entity_lookup():
			"""
			Creates a dictionary with entity names as keys and entity indices from self.entities as values.
			"""
			self.entity_lookup = {}
			i = 0
			for ent in self.entities:
				self.entity_lookup[ent] = i
				i += 1


		def _build_entity_dep_lookup():
			"""
			Creates a dictionary with entity names as keys and lists of dependency indices as values.
			"""
			self.dependencies_lookup = {}
			for ent in self.entities:
				self.dependencies_lookup[ent] = []
				for dep in self.dependencies[ent]:
					self.dependencies_lookup[ent].append(self.entity_lookup[dep])

		_build_entity_lookup()
		_build_entity_dep_lookup()
		#self._buildSystemResultantStates()
		
	##
	## LOGIC
	##
	def _get_ent_resul_st_from_sys_st(self, ent, system_state):
		"""
		Evaluate entity resultant state from system state.
		
		Arguments:
		ent -- entity to be evaluated
		system_state -- states of all entities
		
		Return values:
		resultant state of ent (either 0 or 1)
		"""
		entity_state = self._get_ent_dep_sts_from_sys_st(ent, system_state)
		entity_state_id = get_dec_from_bin_arr(entity_state)  # ID of entity resultant state
		return self.resultant_states[ent][entity_state_id]
		
	def _get_ent_dep_sts_from_sys_st(self, ent, system_state):
		"""
		Evaluate entity state from system state.
		
		Arguments:
		ent -- entity to be evaluated
		system_state -- states of all entities
		
		Exceptions:
		ValueError -- raised when system_state is wrong size
		
		Return values:
		ent_state -- states of ent's dependencies (list)
		"""
		if len(system_state) != len(self.entities):
			raise ValueError('system_state incorrect size')
		ent_state = []
		for dep in self.dependencies[ent]:
			dep_id = self.entity_lookup[dep]
			ent_state.append(system_state[dep_id])  # entity state determined by state of dependencies
		return ent_state
		
	def _det_sys_wide_state_pessimistic(self, current_internal_states, realized_timelines):
		"""
		Constructs worst possible system state given the current internal states.
		
		Arguments:
		current_internal_states -- states of internally-dependent entities
		realized_timelines -- time it takes for an entity's state to change once it's dependencies are met
		
		Return values:
		system_state -- worst possible system state (list)
		"""
		#put all timelines in one place
		durations = copy.copy(realized_timelines)
		
		states = get_bin_list(0, len(self.entities)) # will include internal states
		system_state = get_bin_list(0, len(self.entities)) # will not initially include internal states
		
		changed_ents = []
		for ent in current_internal_states:
			if current_internal_states[ent] == 1 and durations[ent] == 0:
				ent_id = self.entity_lookup[ent]
				changed_ents.append(ent)
				states[ent_id] = 1
		old_states = copy.copy(states)
		while len(changed_ents) > 0:
			for dep_ent in changed_ents:
				for ent in self.entities:
					if dep_ent in self.dependencies[ent] and dep_ent != ent and durations[ent] == 0.0:
						new_resultant = self._get_ent_resul_st_from_sys_st(ent, states)
						old_resultant = self._get_ent_resul_st_from_sys_st(ent, old_states)
						temp_resultant = self._get_ent_resul_st_from_sys_st(ent, system_state)
						#print ':::::',states,system_state,ent,new_resultant,old_resultant
						if new_resultant == 1 and (old_resultant == 0 or temp_resultant == 0):
							old_states = copy.copy(states)
							changed_ents.append(ent)
							ent_id = self.entity_lookup[ent]
							#print '....',dep_ent,ent
							states[ent_id] = 1
							system_state[ent_id] = 1
				changed_ents.remove(dep_ent)
		for ent in current_internal_states: # add internal states of entities that only depend on themselves
			if len(self.dependencies[ent]) == 1 and durations[ent] == 0:
				ent_id = self.entity_lookup[ent]
				system_state[ent_id] = current_internal_states[ent]
		return system_state
		
	def _build_progression(self, _system_state, realized_timelines, stop_at=-1):
		"""
		Builds lists of entity changes, times the changes occur, and the system state after the changes.
		
		Arguments:
		_system_state -- state of all entities
		realized_timelines -- time it takes for an entity's state to change once it's dependencies are met
		
		Keyword arguments:
		stop_at -- Halt and return the progression at this time (default -1)
		
		Return values:
		dep_changes -- entity state changes (list)
		dep_change_timing -- times when changes occur (list)
		system_state -- system state after changes (list)
		"""
		system_state = copy.copy(_system_state)
		#system_state_old = copy.copy(system_state)
		durations = copy.copy(realized_timelines)
		#for key in self.timeEfforts.keys(): durations[key] = self.timeEfforts[key]
		#max_time_step = max(durations.values())
		
		current_time = 0.0
		ents_underway = {}
		
		dep_changes = []
		dep_change_timing = []
		times_with_no_underway = 0
		min_time_step = min(realized_timelines.values())
		while times_with_no_underway <= 1:
			#print '>>', system_state, current_time, ents_underway
			
			# find entities that will change after internal dependence changes
			# (after the duration has passed).
			for ent in self.entities:
				if self._get_ent_resul_st_from_sys_st(ent, system_state) == 0 and ent in self.dependencies[ent]:
					entity_state = self._get_ent_dep_sts_from_sys_st(ent, system_state)
					entity_state_id = get_dec_from_bin_arr(entity_state)
					dep_id = self.dependencies[ent].index(ent)
					entity_state[dep_id] = 1-entity_state[dep_id]  # change ent's state
					entity_state_id = get_dec_from_bin_arr(entity_state)
					if self.resultant_states[ent][entity_state_id] == 1 and ents_underway.has_key(ent) == False:
						ents_underway[ent] = current_time+durations[ent]
						times_with_no_underway = 0
						del durations[ent]
			
			#print 1, times_with_no_underway, ents_underway
			
			# find entities whose dependencies have updated such that the state can change
			# (once the appropriate time passes)
			for ent in self.entities:
				ent_id = self.entity_lookup[ent]
				if self._get_ent_resul_st_from_sys_st(ent, system_state) == 1 and system_state[ent_id] == 0:
					if ent in durations.keys() and ents_underway.has_key(ent) == False:
						ents_underway[ent] = current_time+durations[ent]
						times_with_no_underway = 0
						del durations[ent]
			
			
			#get smallest increment >0 and increment time (some durations can be zero
			#and still not have flipped because of needed dependency changes)
			time_step = min_time_step
			if len(ents_underway.keys()) > 0:
				time_step = min(ents_underway.values())-current_time
			
			# find entities whose time is up
			#system_state_old = copy.copy(system_state)
			for ent in ents_underway.keys():
				#if ents_underway[ent] < current_time:
				#	raise ValueError('entity underway should have already changed state, '+ent)
				#elif ents_underway[ent] == current_time:
				if ents_underway[ent] <= current_time:
					ent_id = self.entity_lookup[ent]
					system_state[ent_id] = 1-system_state[ent_id] #toggle state element
					del ents_underway[ent]
					dep_changes.append(ent)
					dep_change_timing.append(current_time)
					time_step = 0.0
					# don't update time if all that is done is an expiry of an entity's state
			
			#print 3, times_with_no_underway, ents_underway		
			current_time += time_step
			
			if len(ents_underway) == 0: times_with_no_underway += 1
			else: times_with_no_underway = 0
			
			if stop_at >= 0 and current_time >= stop_at:
				underway_vals = [val for val in ents_underway.values() if val <= stop_at]
				#if current_time >= stop_at and n_underway_vals == 0:
				#print '%%%',ents_underway
				if len(underway_vals) == 0:
					return dep_changes, dep_change_timing, system_state
		
		return dep_changes, dep_change_timing, system_state
		
	def _disimprove_from_exits(self, dep_changes, dep_timing, realized_exits, _system_state_at_pa,
			                         _system_state_goal):
		"""
		Recover system after a possible entity state change.
		
		Arguments:
		dep_changes -- entity state changes
		dep_timing -- times when changes occur
		realized_exits -- amount of time an internal dependency of an entity is available
		_system_state_at_pa -- system state before any changes occur
		_system_state_goal -- expected system state after recovery from changes
		
		Exceptions:
		ValueError -- raised when system state not recovered from state changes.
		"""
		system_state = copy.copy(_system_state_at_pa)
		system_state_old = copy.copy(system_state)
		change_occured = False
		for i in range(len(dep_changes)):
			current_time = dep_timing[i]
			#ent_change_id = self.entity_lookup[dep_changes[i]]
			#system_state[ent_change_id] = 1 - system_state[ent_change_id]
			for exit_time_ent in realized_exits.keys():
				if current_time >= realized_exits[exit_time_ent]:  # if exit time reached
					exit_time_ent_id = self.entity_lookup[exit_time_ent]
					system_state[exit_time_ent_id] = 0
					change_occured = True
		if change_occured:
			while change_occured:
				new_change = False
				for ent in self.entities:
					ent_id = self.entity_lookup[ent]
					if (self._get_ent_resul_st_from_sys_st(ent, system_state) == 0 and
					    self._get_ent_resul_st_from_sys_st(ent, system_state_old) == 1):  # if dependency expired
						
						system_state_old = copy.copy(system_state)
						system_state[ent_id] = 0
						new_change = True
				if new_change == False:
					change_occured = False
		else:
			system_state = copy.copy(_system_state_goal)
		#print system_state, _system_state_goal
		if set(system_state) == set(_system_state_goal):
			pass#print 'Expirations okay'
		else:
			raise ValueError('Recovery incomplete due to dependency exit: '+str(system_state))
			
	def _assess_resource_allotment(self, dep_changes, dep_timing, realized_timelines, effort_outputs):
		"""
		Calculate the maximum amount of usage of each resource entity in a timeslice
		by entities with changing states.
		
		Arguments:
		dep_changes -- entity state changes
		dep_timing -- times when changes occur
		realized_timelines -- time it takes for an entity's state to change once it's dependencies are met
		effort_outputs -- number of units of a resource dependency an entity requires
		
		Exceptions:
		ValueError -- raised when there is not enough of a resource
		
		Return values:
		tracked_resource_use -- a dictionary with resources as keys, each with a list of the
								max amount of the resource that was used in each time slice
								between when an entity's deps were met and when its state changed
		"""
		if len(dep_changes) == 0:
			return {}
		durations = copy.copy(realized_timelines)
		#for key in self.timeEfforts.keys(): durations[key] = self.timeEfforts[key]
		
		#find out when entityChanges were initialized
		change_init_times = []
		for i in range(len(dep_changes)):
			ent = dep_changes[i]
			change_init_times.append(dep_timing[i] - durations[ent])
		#instantiate blank list of resource use
		current_resource_use = {}
		tracked_resource_use = {}
		for ent in self.resource_limits.keys():
			current_resource_use[ent] = 0
			tracked_resource_use[ent] = []
			for temp in dep_timing: #temp unused in loop
				tracked_resource_use[ent].append(0.0)
		
		for j in range(len(dep_timing)):
			for ent in self.resource_limits.keys():
				current_resource_use[ent] = 0
			for i in range(len(dep_changes)):
				if (dep_timing[i] == dep_timing[j] or change_init_times[i] == change_init_times[j] 
				    or (dep_timing[j] < dep_timing[i] and dep_timing[j] > change_init_times[i])):
					ent_active = dep_changes[i]
					for resource_ent in current_resource_use.keys():
						if resource_ent != ent_active and resource_ent in self.dependencies[ent_active]:
							current_resource_use[resource_ent] += \
								effort_outputs[ent_active][resource_ent]
							if current_resource_use[resource_ent] > self.resource_limits[resource_ent]:
								raise ValueError('not enough resources of, ' + resource_ent)
			for resource_ent in current_resource_use.keys():
				tracked_resource_use[resource_ent][j] += current_resource_use[resource_ent]
		#print 'Resource Usage Okay', tracked_resource_use
		return tracked_resource_use
		
	def _find_pa(self, system_state):
		"""
		Calculate system level performance with current system state.
		
		Arguments:
		system_state -- state of all entities
		
		Return values:
		p_a -- performance a, the system level performance (float)
		ents_for_pa -- entities contributing to p_a (list)
		"""
		n_ent = len(self.entities)
		ents_for_pa = []
		p_a = 0.0
		for i in range(n_ent):
			ent = self.entities[i]
			if ent in self.op_performance_levels.keys():
				if system_state[i] == 1:
					p_a += self.op_performance_levels[ent]
					ents_for_pa.append(ent)
		return p_a, ents_for_pa
		
	##
	## ASSESS
	##
	def do_progression(self, scenario):
		"""
		Progress the system based on scenario conditions.
		
		Arguments:
		scenario -- GMORScenarioModel progression will be based on
		
		Exceptions:
		ValueError -- raised when GMORScenarioModel is not ready for analysis
					  or when there isn't enough time to meet a deadline
		
		Return values:
		p_a -- performance a, the system level performance (float)
		dep_changes -- entity state changes (list)
		dep_timing -- times when changes occur (list)
		tracked_resource_use -- amounts of resource usage by changed entities (dict)
		"""
		debug_print = False
		if scenario.ready() == False:
			raise ValueError('must send in a ready scenario')
			
		current_internal_states = scenario.current_internal_states
		realized_timelines = scenario.realized_timelines
		realized_exits = copy.copy(scenario.realized_exits)
		effort_outputs = scenario.efforts
		deadlines = scenario.deadlines
		
		for ent in realized_exits.keys():
			if realized_exits[ent] < 0:
				del realized_exits[ent]
		
		#n_ent = len(self.entities)
		#p_r = 1.0
		#pm = self.pm
		#ps = self.ps
		
		##
		## Establish p_a
		##
		# ASSUMPTION: Start in the worst possible state given the internal state infor provided
		#(cannnot assume enough time has passed for any benefits of these states to have propagated)
		system_state = self._det_sys_wide_state_pessimistic(current_internal_states, 
                                                      realized_timelines)
		p_a, ents_for_pa = self._find_pa(system_state)
		if debug_print:
			print '\n>>> p_a...'
			print 'system state:', system_state
			print 'p_a: ', p_a, ents_for_pa

		dep_changes, dep_timing, system_state_res = self._build_progression(system_state,
                                                                      realized_timelines)
		if debug_print:
			print '\n>>> m, s, r...'
			print '', dep_changes
			print '', dep_timing
		
		
		enough_time = self.check_changes_timing(p_a, ents_for_pa, dep_changes, dep_timing, deadlines)
		if debug_print:
			print '\n>>> enough time...', enough_time
		if enough_time == False:
			raise ValueError('Not enough time')
		
		# check that all completed before a dependency expired - like fuel refills.'
		if debug_print:
			print '\n>>> expires...'
		self._disimprove_from_exits(dep_changes, dep_timing, realized_exits, system_state,
									                     system_state_res)
		
		#see if there are enough resources
		if debug_print:
			print '\n>>> resources...'
		tracked_resource_use = self._assess_resource_allotment(dep_changes, dep_timing,
                                                         realized_timelines, effort_outputs)
		
		return p_a, dep_changes, dep_timing, tracked_resource_use
		
	def plot_performance_curve(self, p_a, dep_changes, dep_timing, save=False, file_name='', path=''):
		"""
		Plot the performance curve from the start of the scenario.
		
		Arguments:
		p_a -- performance a, the system level performance
		dep_changes -- entity state changes
		dep_timing -- times when changes occur
		
		Keyword arguments:
		save -- should the figure be saved to a file? (default False)
		file_name -- name of the file the figure will be saved to (default '';
					 name will start with 'LOSS' followed by current date and time)
		path -- absolute path to directory where file will be located (default '';
				path will be to current working directory)
		"""
		perf = 0.0
		p_s = [1.0, 1.0, p_a]
		t_s = [-0.01*max(dep_timing), 0.0, 0.0]
		for i in range(len(dep_changes)):
			ent = dep_changes[i]
			time_ = dep_timing[i]
			if ent in self.op_performance_levels.keys():
				perf += self.op_performance_levels[ent]
				p_s.append(perf)
				t_s.append(time_)
		
		plt.plot(t_s, p_s)
		if save:
			if file_name == '':
				file_name = '\\LOSS-'+str(date.today())+'-'+time.strftime('%X').replace(':', '_')+'.png'
			if path == '':
				path = os.getcwd()
			plt.savefig(path + file_name)
		else:
			print 'Perf', p_s
			print 'Time', t_s
			plt.show()
		plt.close()
		
	def check_changes_timing(self, p_a, ents_for_pa, dep_changes, dep_timing, deadlines):
	#p_a unused argument (unless perf variable below is used)
		"""
		Check that deadlines of entities have been met.
		
		Arguments:
		p_a -- performance a, the system level performance
		ents_for_pa -- entities contributing to p_a
		dep_changes -- entity state changes
		dep_timing -- times when changes occur
		deadlines -- for functions in the scenario, the time that the entity must be active by
		
		Return values:
		True -- if all deadlines have been met
		False -- otherwise
		"""
		#perf = p_a
		deadlines_met = {}
		
		# any ents already okay at p_a automatically meet deadlines since deadlines are >=0
		for ent in deadlines.keys():
			if ent in ents_for_pa:
				deadlines_met[ent] = 1
			else:
				deadlines_met[ent] = 0
		
		#sum(deadlines_met.values()) == len(deadlines_met.keys())
		# proceed through changes
		for i in range(len(dep_changes)):
			ent = dep_changes[i]
			current_time = dep_timing[i]
			if ent in deadlines.keys():
				if current_time <= deadlines[ent]:
					deadlines_met[ent] = 1
					#perf += self.op_performance_levels[ent]
		#if sum(deadlines_met.values()) == 0:
		#	print '\n\n<<<<<<<\n', dep_changes, dep_timing, deadlines_met
		if sum(deadlines_met.values()) == len(deadlines.keys()):#len(deadlines_met.keys()):
			return True
		else:
			return False
			
	def _get_new_timeline(self, new_times, int_dep_funcs):
		"""
		Set new time lines for entities.
		
		Arguments:
		new_times -- new time lines for all entities except functions without internal dependencies
		int_dep_funcs -- functions with internal dependencies
		
		Return values:
		realized_timelines -- the new time lines for the entities (dict)
		"""
		realized_timelines = {}
		for ent in self.entities:
			ent_type = self.ent_types[ent]
			if ent_type == ENTTYPE.FUNCTION and ent not in int_dep_funcs:
				realized_timelines[ent] = 0.0
			else:
				realized_timelines[ent] = new_times[ent]
		return realized_timelines
	
	def deterministic_progression(self, model, current_internal_states, realized_timelines,
              	                  realized_exits, efforts, deadlines):
		"""
		Do progression with given initial scenario conditions.
		
		Arguments:
		model -- GMORModel the scenario is based on
		current_internal_states -- state of internally dependent entities
								   (0 for unavailable, 1 for available)
		realized_timelines -- time it takes for an entity's state to change once it's dependencies are met
		realized_exits -- amount of time an internal dependency of an entity is available
		efforts -- number of units of a resource dependency an entity requires
		deadlines -- for function entities, the time at which the entity must be active by
		
		Return values:
		p_a -- performance a, the system level performance (float)
		dep_change -- entity state changes (list)
		dep_timing -- times when changes occur (list)
		tracked_resource_use -- amounts of resource usage by changed entities (dict)
		"""
		c_b = GMORScenarioModel(model, 'Scenario 1')
		c_b.set_and_check(model, current_internal_states, realized_timelines, realized_exits, efforts, deadlines)
		return self.do_progression(c_b)
		
	def next_deadline(self, current_time, system_state, deadlines):
		"""
		For a given time get the next deadline and the functions that
		have that deadline and aren't currently in a desirable state
		
		Arguments:
		current_time -- the time within a progression
		system_state -- an array of current entity realized states (in the order of self.entities)
		deadlines -- for functions in the scenario, the time that the entity must be active by
		
		Return an array:
		[0] -- the next upcoming deadline
		[1] -- an array of entity functions with that deadline
		"""
		# use np.array to get all occurrences, and not just first
		dlines = np.array(deadlines.values()) 
		if len(dlines[dlines > current_time]) > 0:
			next_dline = min(dlines[dlines > current_time])
			next_funcs = []
			
			for ent in deadlines.keys():
				if (deadlines[ent] == next_dline and 
				    self._get_ent_resul_st_from_sys_st(ent, system_state) != 1):
					next_funcs.append(ent)
			
			return next_dline, next_funcs
		return -1, []

	def get_deps_to_do(self, ents, deps, entity_states, system_state, have_checked):
		"""
		Adds entity names to the deps argument if they meet several condtions:
		They have an internal state, they do not already have a realized state of 1
		and are not events.
		
		Arguments:
		ents -- list of entities whose dependencies are being assessed
		deps -- list of dependencies that are known to satisfy the conditions
		entity_states -- dictionary of current internal states of entities with intenral dependency
		system_state -- the current realized states of all entities (ordered by self.entities)
		have_checked -- Optional list of entites that have already been checked
		"""
		#have_checked = [ent for ent in ents]
		for ent in ents:
			for dep in self.dependencies[ent]:
				# not already checked
				# not already added
				# not a hazard event
				# not already in the desired state
				# assume all non event entities have a desired state of 1
				if (dep not in have_checked and dep not in deps and
				    self.ent_types[dep] != ENTTYPE.EVENT and
				    self._get_ent_resul_st_from_sys_st(dep, system_state) != 1):
					
					# has an internal dependency in undesirable state
					# assumes realized state requires internal state of 1
					if dep in self.dependencies[dep] and entity_states[dep] == 0:
						deps.append(dep)
					
					#have_checked.append(dep)
					if dep != ent:
						self.get_deps_to_do([dep], deps, entity_states, system_state, have_checked)
				
				if dep not in have_checked:
					have_checked.append(dep)
		#have_checked += [ent for ent in ents]
	
	def max_timing_progression(self, current_internal_states, defaults, deadlines):
		"""
		Computes the longest possible recovery from an initial state subject to function entity
		deadlines.
		
		Arguments
		current_internal_states -- Dictionary. Keys are entities with internal dependencies
											  Values are state of internal dependencies
		defaults -- default realized entity state (0 for most entities, 1 for events, generally)
		deadlines -- for functions in the scenario, the time that the entity must be active by
		
		Returns:
		timings
		"""
		# keep track of current realized state of entities
		# initialize to current_internal_states
		entity_states = copy.copy(current_internal_states)
		
		# dictionary of entities with internal dependencies
		timings = {}
		
		realized_timelines = {}
		for ent in self.entities:
			if ent in self.dependencies[ent] and entity_states[ent] == 0:
				# don't want internal dependencies to change unless they have to
				realized_timelines[ent] = max(deadlines.values())+1.0 
			else:
				realized_timelines[ent] = 1.0 # do not chnage this

		system_state = self._det_sys_wide_state_pessimistic(current_internal_states, realized_timelines)
		
		p_a, ents_for_pa = self._find_pa(system_state)
		
		time = 0.0
		done = False
		while not done:

			dline, func_ents = self.next_deadline(time, system_state, deadlines)
			
			if dline >= 0:
				# Dependencies that may need to change (OR dependencies not account for, all assumed AND)
				deps = []
				self.get_deps_to_do(func_ents,deps,entity_states,system_state,[])
				
				#update timings
				for ent in self.entities:
					if ent in self.dependencies[ent]:
						if ent not in deps:
							realized_timelines[ent] = max(deadlines.values())+1.0 # don't want internal dependencies to change unless they have to
						else:
							realized_timelines[ent] = 0.0#dline
					else:
						realized_timelines[ent] = 0.0
				
				# progress based on updated internal dependencies and timings
				dep_changes, dep_change_timing, system_state = self._build_progression(system_state, realized_timelines, dline)
								
				# update total set of dep changes
				deps += [dep for dep in dep_changes if dep not in deps]
				timings[dline] = copy.copy(deps)
				
				for ent in deps:
					if ent in self.dependencies[ent]:
						entity_states[ent] = 1
						
				time = dline
			else:
				done = True
				
		return timings
	
if __name__ == '__main__':
	pass
