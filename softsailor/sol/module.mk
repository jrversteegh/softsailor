dirstack := $(dirstack).x
d_$(dirstack) := $(d)
d := $(dir $(lastword $(MAKEFILE_LIST)))

$(d)_TEST_FILES := $(wildcard $(d)tst/test_*.py)
TSTS_$(d) := $(subst $(d)tst/,sol_, $($(d)_TEST_FILES:.py=))
TEST_TARGETS := $(TEST_TARGETS) $(TSTS_$(d))

sol_test_%: $(d)tst/test_%.py
	$(RUNP)

$(d)sol_test_%: $(d)tst/test_%.py
	$(RUNP)

$(d)test: $(TSTS_$(d))


d := $(d_$(dirstack))
dirstack := $(basename $(dirstack))
