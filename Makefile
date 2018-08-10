.PHONY: usage install uninstall
usage:
	@echo "Usage: make <target>, where target is one of:\n"
	@echo "install:       install the library locally from source"
	@echo "uninstall:     uninstall the local library"
	@echo "python-readme: generate library/README.rst from README.md"
	@echo "python-wheels: build python .whl files for distribution"
	@echo "python-sdist:  build python source distribution"
	@echo "python-clean:  clean python build and dist directories"
	@echo "python-dist:   build all python distribution files" 

install:
	./install.sh

uninstall:
	./uninstall.sh

python-readme: library/README.rst

library/README.rst: README.md
	pandoc --from=markdown --to=rst -o library/README.rst README.md

python-wheels:
	cd library; python3 setup.py bdist_wheel
	cd library; python setup.py bdist_wheel

python-sdist:
	cd library; python setup.py sdist

python-clean:
	-rm -r library/dist
	-rm -r library/build
	-rm -r library/*.egg-info

python-dist: python-clean python-readme python-wheels python-sdist
	ls library/dist

python-deploy: python-dist
	twine upload library/dist/*
