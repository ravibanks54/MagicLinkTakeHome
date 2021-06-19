.PHONY: run
run:
	python src/index.py

.PHONY: test
test:
	python -m unittest discover

