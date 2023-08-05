all:	CHANGES.rst

CHANGES.rst:
	git log --oneline --pretty=format:"* %ad: %s\n" --date=short > CHANGES.rst

install:
	python setup.py install

clean:
	-rm -f CHANGES.rst

test:
	nosetests

.PHONY:	all install clean test
