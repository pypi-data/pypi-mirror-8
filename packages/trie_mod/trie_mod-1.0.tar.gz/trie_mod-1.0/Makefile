
FILES1=sample trie_mod.py
FILES2= test-trie-mod trie_mod.py

go:
	./this-pylint --to-pylint $(FILES1)
	pep8 --max-line-len 132 $(FILES1)
	./this-pylint --to-pylint $(FILES2)
	pep8 --max-line-len 132 $(FILES2)
	# we use all(), which is 2.5+
	#/usr/local/cpython-2.4/bin/python test-trie-mod
	/usr/local/cpython-2.5/bin/python test-trie-mod
	/usr/local/cpython-2.6/bin/python test-trie-mod
	/usr/local/cpython-2.7/bin/python test-trie-mod
	/usr/local/cpython-3.0/bin/python test-trie-mod
	/usr/local/cpython-3.1/bin/python test-trie-mod
	/usr/local/cpython-3.2/bin/python test-trie-mod
	/usr/local/cpython-3.3/bin/python test-trie-mod
	/usr/local/cpython-3.4/bin/python test-trie-mod
	/usr/local/pypy-2.4.0/bin/pypy test-trie-mod
	/usr/local/pypy3-2.4.0/bin/pypy test-trie-mod
	/usr/local/jython-2.7b3/bin/jython test-trie-mod
	./sample

register:
	python setup.py register

publish:
	python setup.py sdist upload

clean:
	rm -f *.pyc *.class
	rm -rf __pycache__

