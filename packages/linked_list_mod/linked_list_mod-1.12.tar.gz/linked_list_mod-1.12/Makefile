
go: test-linked-list test-fifo test-lifo perf-comp

perf-comp:
	./this-pylint --to-pylint performance-comparison linked_list_mod.py
	pep8 --max-line-length=131 performance-comparison
	./performance-comparison

test-fifo:
	./this-pylint --to-pylint fifo_mod.py test-fifo_mod linked_list_mod.py 
	pep8 --max-line-length=131 test-fifo_mod lifo_mod.py
	/usr/local/cpython-3.4/bin/python ./test-fifo_mod
	/usr/local/cpython-2.7/bin/python ./test-fifo_mod
	/usr/local/pypy-2.3.1/bin/pypy ./test-fifo_mod
	/usr/local/pypy3-2.3.1/bin/pypy ./test-fifo_mod
	/usr/local/jython-2.7b3/bin/jython ./test-fifo_mod

test-lifo:
	./this-pylint --to-pylint lifo_mod.py test-lifo_mod linked_list_mod.py 
	pep8 --max-line-length=131 test-lifo_mod lifo_mod.py
	/usr/local/cpython-3.4/bin/python ./test-lifo_mod
	/usr/local/cpython-2.7/bin/python ./test-lifo_mod
	/usr/local/pypy-2.3.1/bin/pypy ./test-lifo_mod
	/usr/local/pypy3-2.3.1/bin/pypy ./test-lifo_mod
	/usr/local/jython-2.7b3/bin/jython ./test-lifo_mod

test-linked-list:
	./this-pylint --to-pylint test-linked_list_mod linked_list_mod.py
	pep8 --max-line-length=131 test-linked_list_mod linked_list_mod.py
	/usr/local/cpython-3.4/bin/python ./test-linked_list_mod
	/usr/local/cpython-2.7/bin/python ./test-linked_list_mod
	/usr/local/pypy-2.3.1/bin/pypy ./test-linked_list_mod
	/usr/local/pypy3-2.3.1/bin/pypy ./test-linked_list_mod
	/usr/local/jython-2.7b3/bin/jython ./test-linked_list_mod

clean:
	rm -rf __pycache__ *.pyc *.class
	rm -rf linked_list_mod.egg-info
	rm -rf dist

register:
	python setup.py register

publish:
	python setup.py sdist upload


