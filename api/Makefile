build: create_venv install-requirements
test: run-api-tests
clean-build: clean clean-deps create_venv install-requirements
clean-build-package: clean clean-deps create_venv install-requirements package

run:
	. venv/bin/activate && \
	uvicorn main:app --host 0.0.0.0

run-reload:
	. venv/bin/activate && \
	uvicorn main:app --host 0.0.0.0 --reload

clean:
	rm -rf dist/

clean-deps:
	rm -rf venv/

create_venv:
	test -e venv/bin/activate || \
	python3 -m venv venv

install-requirements: create_venv
	. venv/bin/activate && \
	pip3 install -q -r requirements.txt

install-test-requirements: create_venv
	. venv/bin/activate && \
	pip3 install -q -r requirements-test.txt

package: install-requirements
	mkdir -p ./dist
	cd ./venv/lib/python3.8/site-packages/ && \
	zip -qr9 ../../../../dist/api.zip . -x \*.pyc
	zip -qgr9 ./dist/api.zip . -x ./dist/**\* ./venv/**\* \*.pyc ./.env* ./.git*

run-api-tests:
	. venv/bin/activate && \
	pytest controllers/tests services/tests

test-code-formatting:
	. venv/bin/activate && \
	black . --check --exclude "/venv/"

run-checks: build install-test-requirements run-api-tests test-code-formatting
