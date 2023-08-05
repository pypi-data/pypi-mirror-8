
JAVAC=javac
JAVA_HOME=$(shell /usr/libexec/java_home)

all: dist/rubicon.jar dist/librubicon.dylib dist/test.jar

dist/rubicon.jar: org/pybee/rubicon/Python.class org/pybee/rubicon/PythonInstance.class
	mkdir -p dist
	jar -cvf dist/rubicon.jar org/pybee/rubicon/Python.class org/pybee/rubicon/PythonInstance.class

dist/test.jar: org/pybee/rubicon/test/BaseExample.class org/pybee/rubicon/test/Example.class org/pybee/rubicon/test/ICallback.class org/pybee/rubicon/test/AbstractCallback.class org/pybee/rubicon/test/Thing.class org/pybee/rubicon/test/Test.class
	mkdir -p dist
	jar -cvf dist/test.jar org/pybee/rubicon/test/*.class

dist/librubicon.dylib: jni/rubicon.o
	mkdir -p dist
	gcc -shared -lPython -o $@ $<

clean:
	rm -f org/pybee/rubicon/test/*.class
	rm -f org/pybee/rubicon/*.class
	rm -f jni/*.o
	rm -rf dist

%.class : %.java
	$(JAVAC) $<

%.o : %.c
	gcc -c -Isrc -I$(JAVA_HOME)/include -I$(JAVA_HOME)/include/darwin -o $@ $<

