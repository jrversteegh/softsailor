.PHONY: test
test:
	@nosetests

clean:
	@find . -name "*.pyc" -exec rm {} \;
