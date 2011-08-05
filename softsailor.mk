all: $(TARGETS)
	  @echo $(TARGETS)

.PHONY: test   
test: $(TEST_TARGETS)
	  @echo "Ran tests!"

.PHONY: clean
clean: 
		@rm -f $(CLEAN_TARGETS)
		@find . -iname "*.pyc" -exec rm -f {} \; 
			

