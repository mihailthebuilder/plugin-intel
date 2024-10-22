run:
	python main.py

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

test:
	python -m unittest discover -p "*_test.py"