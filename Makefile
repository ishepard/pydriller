@PHONY: checkall lint typecheck testcoverage test

checkall: typecheck lint testcoverage

lint:
	flake8

typecheck:
	mypy --ignore-missing-imports pydriller/ tests/

testcoverage:
	pytest --cov-report term --cov=pydriller tests/

test:
	pytest