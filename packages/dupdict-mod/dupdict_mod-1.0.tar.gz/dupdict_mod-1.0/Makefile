
FILES=dupdict_mod.py test-dupdict_mod

go: treap.py py_treap.py red_black_dict_mod.py
	./this-pylint --to-pylint $(FILES)
	pep8 --max-line-len 132 $(FILES)
	/usr/local/cpython-3.0/bin/python test-dupdict_mod
	/usr/local/cpython-3.1/bin/python test-dupdict_mod
	/usr/local/cpython-3.2/bin/python test-dupdict_mod
	/usr/local/cpython-3.3/bin/python test-dupdict_mod
	/usr/local/cpython-3.4/bin/python test-dupdict_mod
	#/usr/local/cpython-2.4/bin/python test-dupdict_mod
	#/usr/local/cpython-2.5/bin/python test-dupdict_mod
	/usr/local/cpython-2.6/bin/python test-dupdict_mod
	/usr/local/cpython-2.7/bin/python test-dupdict_mod
	/usr/local/pypy-2.4.0/bin/pypy test-dupdict_mod
	/usr/local/pypy3-2.3.1/bin/pypy test-dupdict_mod
	/usr/local/jython-2.7b3/bin/jython test-dupdict_mod

treap.py py_treap.py: treap-dir/m4_treap.m4
	cd treap-dir && python setup.py build
	cp treap-dir/treap.py treap-dir/py_treap.py .
	
red_black_dict_mod.py: red_black_tree-dir/red_black_tree_mod.m4
	cd red_black_tree-dir && make
	cp red_black_tree-dir/red_black_dict_mod.py .

register:
	python setup.py register

publish:
	python setup.py sdist upload

clean:
	rm -f treap.py py_treap.py red_black_dict_mod.py
	rm -rf __pycache__
	rm -f *.pyc
	cd treap-dir && python setup.py clean
	cd red_black_tree-dir && make clean
	rm -f *.class

