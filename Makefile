# Clean venv
.PHONY: clean
clean:
	rm -rf env


# Create virtualenv 
.PHONY: env
env: env/bin/activate
env/bin/activate: requirements.txt
	@test -d env || python3 -m venv env
	env/bin/pip install -r requirements.txt
	@touch env/bin/activate