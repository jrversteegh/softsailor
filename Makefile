test:
	@nosetests

clean:
	@find . -name "*.pyc" -exec rm {} \;
