init:
	pip install -r requirements.txt
dir = "default"
conf = "default"
run:
	python initializer.py -d $(dir) -c $(conf)