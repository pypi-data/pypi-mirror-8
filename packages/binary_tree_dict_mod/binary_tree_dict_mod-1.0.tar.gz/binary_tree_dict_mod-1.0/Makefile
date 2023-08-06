
go: binary_tree_dict_mod.py
	./this-pylint --to-pylint binary_tree_dict_mod.py
	/usr/local/cpython-2.5/bin/python ./test-binary_tree_dict_mod
	/usr/local/cpython-2.7/bin/python ./test-binary_tree_dict_mod
	/usr/local/cpython-3.0/bin/python ./test-binary_tree_dict_mod
	/usr/local/cpython-3.4/bin/python ./test-binary_tree_dict_mod
	/usr/local/pypy-2.4.0/bin/pypy ./test-binary_tree_dict_mod
	/usr/local/pypy3-2.4.0/bin/pypy ./test-binary_tree_dict_mod
	/usr/local/jython-2.7b3/bin/jython ./test-binary_tree_dict_mod

binary_tree_dict_mod.py: binary_tree_dict_mod.m4
	m4 binary_tree_dict_mod.m4 > binary_tree_dict_mod.py

register:
	python setup.py register

publish:
	python setup.py sdist upload

clean:
	rm -f *.pyc *.class
	rm -rf __pycache__
	rm -f binary_tree_dict_mod.py

