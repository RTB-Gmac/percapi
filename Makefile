.PHONY: tests
tests: # Apply migrations created by django to postgres
	@$(MAKE) pytest poc/test.py

.PHONY: setup_env
setup_env: # Set up local environment
	@$(MAKE) pip install -r requirements.txt