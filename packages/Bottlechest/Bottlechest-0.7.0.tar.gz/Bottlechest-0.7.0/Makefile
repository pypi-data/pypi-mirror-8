# Bottleneck Makefile 

PYTHON=python

srcdir := bottlechest/src

help:
	@echo "Available tasks:"
	@echo "help   -->  This help page"
	@echo "pyx    -->  Create Cython pyx files from templates"
	@echo "cfiles -->  Convert pyx files to C files"
	@echo "build  -->  Build the Cython extension modules"
	@echo "clean  -->  Remove all the build files for a fresh start"
	@echo "test   -->  Run unit tests"
	@echo "all    -->  clean, pyx, build, test"
	@echo "bench  -->  Run performance benchmark"
	@echo "sdist  -->  Make source distribution"

all: clean pyx cfiles build test

pyx:
	${PYTHON} -c "from bottlechest.src.makepyx import makepyx; makepyx()"

cfiles:
	cython ${srcdir}/func/32bit/*.pyx
	cython ${srcdir}/func/64bit/*.pyx
	

build: funcs
	
funcs:
	rm -rf ${srcdir}/../*.so
	${PYTHON} ${srcdir}/func/setup.py build_ext --inplace
	
test:
	${PYTHON} -c "import bottlechest;bottlechest.test()"

bench:
	${PYTHON} -c "import bottlechest; bottlechest.bench()"

sdist: pyx cfiles
	rm -f MANIFEST
	git status
	find -name *.c
	${PYTHON} setup.py sdist

# Phony targets for cleanup and similar uses

.PHONY: clean
clean:
	rm -rf ${srcdir}/*~ ${srcdir}/*.so ${srcdir}/*.c ${srcdir}/*.o ${srcdir}/*.html ${srcdir}/build ${srcdir}/../*.so
	rm -rf ${srcdir}/func/32bit/*.c ${srcdir}/func/64bit/*.c
	rm -rf ${srcdir}/func/32bit/*.pyx  ${srcdir}/func/64bit/*.pyx
