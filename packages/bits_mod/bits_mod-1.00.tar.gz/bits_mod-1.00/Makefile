
FILES=test-bits_mod bits_mod.py
go:
	./this-pylint --to-pylint $(FILES)
	pep8 --max-line-len 132 $(FILES)
	/usr/local/cpython-2.4/bin/python ./test-bits_mod
	/usr/local/cpython-2.5/bin/python ./test-bits_mod
	/usr/local/cpython-2.6/bin/python ./test-bits_mod
	/usr/local/cpython-2.7/bin/python ./test-bits_mod
	/usr/local/cpython-3.0/bin/python ./test-bits_mod
	/usr/local/cpython-3.1/bin/python ./test-bits_mod
	/usr/local/cpython-3.2/bin/python ./test-bits_mod
	/usr/local/cpython-3.3/bin/python ./test-bits_mod
	/usr/local/cpython-3.4/bin/python ./test-bits_mod
	/usr/local/pypy-2.3.1/bin/pypy ./test-bits_mod
	/usr/local/pypy3-2.3.1/bin/pypy ./test-bits_mod
	/usr/local/jython-2.7b3/bin/jython ./test-bits_mod

register:
	python setup.py register

publish:
	python setup.py sdist upload

clean:
	rm -f *.pyc *.class
	rm -rf __pycache__
