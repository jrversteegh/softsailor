define TEST_template

.PHONY: $(1)
$(1): $$(d)tst/$(1).py
	cd $$(dir $$<) && python2.7 $$(notdir $$<)

endef

include softsailor/module.mk

#test_map: softsailor/tst/test_map.py
#	cd $(dir $<) && python2.7 $(notdir $<)

all: $(TARGETS)
	  @echo $(TARGETS)

.PHONY: test   
test: $(TEST_TARGETS)
	  @echo "Ran tests!"

.PHONY: test   
test_list:
	@echo "$(TEST_TARGETS)"

.PHONY: install
install: 
		@python setup.py build
		@sudo python setup.py install

.PHONY: clean
clean: 
		@rm -f $(CLEAN_TARGETS)
		@find . -iname "*.pyc" -exec rm -f {} \; 
			
vr:
	python3 vr.py
