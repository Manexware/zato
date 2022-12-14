
.PHONY: test

Zato_Python_Dir=$(CURDIR)/../bin
Zato_Package_Name=zato-common

run-tests:
	echo "Running tests in zato-common"
	$(Zato_Python_Dir)/nosetests $(CURDIR)/test/zato/common/test_kv_data_api.py -s
	$(Zato_Python_Dir)/nosetests $(CURDIR)/test/zato/common/test_util.py -s
	$(Zato_Python_Dir)/nosetests $(CURDIR)/test/zato/common/marshall_/test_attach.py -s
	$(Zato_Python_Dir)/nosetests $(CURDIR)/test/zato/common/marshall_/test_validation.py -s
	$(Zato_Python_Dir)/nosetests $(CURDIR)/test/zato/common/marshall_/test_json_to_dataclass.py -s

pylint:
	echo Running pylint in $(Zato_Package_Name)
	$(Zato_Python_Dir)/pylint --verbose \
		--rcfile $(CURDIR)/../pylint.ini \
				 $(CURDIR)/../zato-common/src/zato/common/

pyright:
	$(Zato_Python_Dir)/pyright -p $(CURDIR)/../pyproject.toml $(CURDIR)/src/zato/common/pubsub.py
	$(Zato_Python_Dir)/pyright -p $(CURDIR)/../pyproject.toml $(CURDIR)/src/zato/common/util/pubsub.py

mypy:
	$(Zato_Python_Dir)/mypy --show-error-codes --ignore-missing-imports $(CURDIR)/src/zato/common/pubsub.py

flake8:
	echo "Running flake8 checks in $(Zato_Package_Name)"
	$(Zato_Python_Dir)/flake8 --config=$(CURDIR)/../tox.ini $(CURDIR)/

type-check:
	echo "Running type checks ($(Zato_Package_Name))"
	$(MAKE) mypy
	$(MAKE) pyright

static-check:
	echo "Running static checks in $(Zato_Package_Name)"
	$(MAKE) flake8
	$(MAKE) type-check
