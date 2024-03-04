clean:
	@echo Removing unnecessary files...
	@find . -name "*.pyc" -delete && \
	find . -name "*.pyo" -delete && \
	find . -name .pytest_cache | xargs rm -rf || true && \
	find . -name __pycache__ -delete && \
	find . -name ".coverage" -delete && \
	rm -f .coverage && \
	rm -rf htmlcov && \
	rm -rf test_reports

lint:
	@echo Running lint...
	@flake8 --config=.flake8 ./*

test: clean lint
	@echo Runing tests...
	@pytest tests/ -s -v

coverage: clean lint
	@echo Generating coverage report...
	@pytest --cov-report term-missing --cov=banks -s -vv --rootdir=./tests --junitxml=test_reports/junit.xml --cov-branch --cov-report=term --cov-report=html
