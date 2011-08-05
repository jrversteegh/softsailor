dirstack := $(dirstack).x
d_$(dirstack) := $(d)
d := $(dir $(lastword $(MAKEFILE_LIST)))

include $(d)sol/module.mk

$(d)_TEST_FILES := $(wildcard $(d)tst/test_*.py)
TSTS_$(d) := $(subst $(d)tst/,, $($(d)_TEST_FILES:.py=))
TEST_TARGETS := $(TEST_TARGETS) $(TSTS_$(d))

$(d)test: $(TSTS_$(d))

test_%: $(d)tst/test_%.py
	$(RUNP)

d := $(d_$(dirstack))
dirstack := $(basename $(dirstack))
