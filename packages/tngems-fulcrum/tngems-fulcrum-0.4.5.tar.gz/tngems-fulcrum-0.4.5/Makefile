# vim: noexpandtab:syntax=make
CONF_DIR=/etc/tngems/fulcrum
LOG_DIR=/var/log/tngems/fulcrum
STATE_DIR=/var/lib/tngems/fulcrum
LIB_DIR=/usr/lib/tngems/fulcrum
PID_DIR=/var/run/tngems
SHARE_DIR=/usr/share/tngems/fulcrum
CLI_TOOL_NAME=fulcrum
CLI_TOOL_EXEC=bin/fulcrum.sh


install:
	@echo "Installing Fulcrum"
	@echo "\tCreating application directories"
	@mkdir -p $(CONF_DIR)
	@mkdir -p $(LOG_DIR)
	@mkdir -p $(STATE_DIR)
	@mkdir -p $(PID_DIR)
	@mkdir -p $(SHARE_DIR)
	@chmod 755 $(SHARE_DIR)

	@echo "\tCopying configuration files"

	@echo "\tCreating the Fulcrum virtual environment"
	@test -d $(LIB_DIR) || virtualenv $(LIB_DIR) --system-site-packages \
		-p python3 > /dev/null
	
	@echo "\tDownloading dependencies"
	@. $(LIB_DIR)/bin/activate; 
	@pip3 install -r requirements.txt > /dev/null
	@python3 setup.py install > /dev/null

	@echo "\tCopying executables"
	@cp $(CLI_TOOL_EXEC) /usr/bin/$(CLI_TOOL_NAME)
	@chmod +x /usr/bin/$(CLI_TOOL_NAME)

	@echo "\tCleanup"
	@rm -rf build dist sdist


purge:
	@echo "Completely removing Fulcrum from this system"
	@rm -rf $(CONF_DIR)
	@rm -rf $(STATE_DIR)
	@rm -rf $(LOG_DIR)
	@rm -rf $(LIB_DIR)
	@rm -rf $(SHARE_DIR)
	@echo "Done"
