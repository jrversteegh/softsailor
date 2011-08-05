%:
	$(MAKE) -C .. $(notdir $(realpath .))/$@

all:
	$(MAKE) -C .. all

test_%:
	$(MAKE) -C .. $@

clean:
	$(MAKE) -C .. $@

.PHONY: test
test:
	$(MAKE) -C .. $@
