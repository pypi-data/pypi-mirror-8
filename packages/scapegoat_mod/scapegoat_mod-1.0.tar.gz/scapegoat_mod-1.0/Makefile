
go: scapegoat_mod.py
	./this-pylint --to-pylint test-scapegoat_mod scapegoat_mod.py
	/usr/local/cpython-3.3/bin/python ./test-scapegoat_mod 0.75
	/usr/local/cpython-3.0/bin/python ./test-scapegoat_mod 0.60
	/usr/local/cpython-2.7/bin/python ./test-scapegoat_mod 0.90
	/usr/local/cpython-2.5/bin/python ./test-scapegoat_mod 0.75
	/usr/local/pypy-2.2/bin/pypy ./test-scapegoat_mod 0.60
	/usr/local/jython-2.7b2/bin/jython ./test-scapegoat_mod 0.90

scapegoat_mod.py: scapegoat_mod.m4
	m4 < scapegoat_mod.m4 > scapegoat_mod.py

register:
	python setup.py register

publish:
	python setup.py sdist upload

clean:
	rm -f *.pyc scapegoat_mod.py *.class
	rm -rf __pycache__

