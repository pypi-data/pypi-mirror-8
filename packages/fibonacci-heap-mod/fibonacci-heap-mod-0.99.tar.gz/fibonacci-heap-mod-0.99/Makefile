
#%.class : %.java
#    $(JAVAC) $(JFLAGS) $<

PYTHON_FILES=fibonacci_heap_mod.py test-fibonacci-heap-mod

JAVAC=javac
JFLAGS=-Xlint:unchecked -classpath .

first: go-python go-java

go-java: TestFibonacciHeap.jar
	java -jar TestFibonacciHeap.jar TestFibonacciHeap.main

go-python:
	./this-pylint --which-2 /usr/local/cpython-2.7/bin/pylint --to-pylint $(PYTHON_FILES)
	pep8 --max-line-len=132 $(PYTHON_FILES)
	/usr/local/cpython-3.4/bin/python ./test-fibonacci-heap-mod
	/usr/local/cpython-3.0/bin/python ./test-fibonacci-heap-mod
	/usr/local/cpython-2.7/bin/python ./test-fibonacci-heap-mod
	/usr/local/pypy-2.4.0/bin/pypy ./test-fibonacci-heap-mod
	/usr/local/pypy3-2.4.0/bin/pypy ./test-fibonacci-heap-mod
	/usr/local/jython-2.7b3/jython ./test-fibonacci-heap-mod

TestFibonacciHeap.jar: TestFibonacciHeap.class
	jar cmvf mainClass.txt TestFibonacciHeap.jar *.class

TestFibonacciHeap.class: TestFibonacciHeap.java
	$(JAVAC) $(JFLAGS) TestFibonacciHeap.java

register:
	python setup.py register

publish:
	python setup.py sdist upload

clean:
	rm -f *.pyc *.class *.jar
	rm -rf __pycache__ build dist fibonacci_heap_mod.egg-info
	rm -f tags
