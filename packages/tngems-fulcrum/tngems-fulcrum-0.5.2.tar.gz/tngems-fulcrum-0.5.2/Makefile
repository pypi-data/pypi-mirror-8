#!/usr/bin/make -f
# -*- makefile -*-
# vim: noexpandtab
include macros/make/tngems.mk
include macros/make/fulcrum.mk
PYTHON=python3
FULCRUM_CONF_DIR=$(TNGEMS_CONF_DIR)/components/fulcrum


install:
	@echo "Installing Fulcrum to $(TNGEMS_LIB_DIR)/fulcrum"
	@echo "Creating virtual environment in $(TNGEMS_LIB_DIR)/fulcrum"
	@ test -d $(TNGEMS_LIB_DIR)/fulcrum || \
		virtualenv $(TNGEMS_LIB_DIR)/fulcrum --system-site-packages
	@. $(TNGEMS_LIB_DIR)/fulcrum/bin/activate; \
		$(PYTHON) setup.py install
	@cp bin/fulcrum /usr/bin/fulcrum
	@rsync -rv share/templates $(TNGEMS_SHARED_DIR)/fulcrum
	@sudo -u $(TNGEMS_UNIX_USER) mkdir -p $(FULCRUM_CONF_DIR)
	@sudo -u $(TNGEMS_UNIX_USER) cp -n etc/fulcrum.conf $(FULCRUM_CONF_DIR)/fulcrum.conf
	@sudo chown -R $(TNGEMS_UNIX_USER):$(TNGEMS_UNIX_GROUP) $(TNGEMS_LIB_DIR)
	@sudo chown -R $(TNGEMS_UNIX_USER):$(TNGEMS_UNIX_GROUP) $(FULCRUM_CONF_DIR)

clean:
	@find . | grep -E "(__pycache__|\.pyc$\)" | xargs rm -rf
	@rm -rf dist build
	@rm -rf *.egg-info
	@rm -rf ../*.orig.tar.gz
	@rm -rf *.egg-info

dist: clean
	@echo "rsync the contents to $(TNGEMS_SRC_DIR)"
	@mkdir -p $(TNGEMS_SRC_DIR)/fulcrum
	rsync -rv . $(TNGEMS_SRC_DIR)/fulcrum \
		--exclude=.hg \
		--exclude=debian \
		--exclude=legacy \
		--exclude=.hg* \
		--exclude=.* \
		--exclude=.vagrant \
		--exclude=build \
		--exclude=tmp \
		--exclude=dist \
		--exclude=VagrantFile > /dev/null
