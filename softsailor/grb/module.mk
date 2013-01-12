dirstack := $(dirstack).x
d_$(dirstack) := $(d)
d := $(dir $(lastword $(MAKEFILE_LIST)))

$(d)_TEST_FILES := $(wildcard $(d)tst/test_grb_*.py)
TSTS_$(d) := $(subst $(d)tst/,, $($(d)_TEST_FILES:.py=))
TEST_TARGETS := $(TEST_TARGETS) $(TSTS_$(d))

$(d)test: $(TSTS_$(d))

$(foreach p, $(TSTS_$(d)), $(eval $(call TEST_template,$(p))))

d := $(d_$(dirstack))
dirstack := $(basename $(dirstack))
