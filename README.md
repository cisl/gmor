# The Graph Model for Operational Resilience (GMOR)
Build graphs of complex operations of any type and assess how failures and recovery cascade.

# Installing the Requirements
pip install -r requirements.txt from project root

# Run tests
Run `nose2` from the project root

# Documentation
Documentation is found in the `docs` folder. It can be generated by running `pydoc -w module_name` (without the .py extension)

# Using GMOR
GMOR consists of two modules: `model.py` and `util.py`. `model.py` contains all of the classes you'll need to direclty interact with.

To build a model, create an instance of `GMORModel`

To run it, use `GMORRunner`

More to come...

# How to cite
Aspects of this software are described in:
Bristow and Hay, 2016. Graph Model for Probabilistic Resilience and Recovery Planning of Multi-Infrastructure Systems. ASCE Journal of Infrastructure Systems, http://dx.doi.org/10.1061/(ASCE)IS.1943-555X.0000338#sthash.6JtAP3OV.dpuf
