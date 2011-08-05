dirstack := $(dirstack).x
d_$(dirstack) := $(d)
d := $(dir $(lastword $(MAKEFILE_LIST)))

include $(d)sol/module.mk

TSTS_$(d) := test_boat test_conditions test_motion test_navigator \
	test_classes test_performance test_route test_router test_sailor \
	test_situation test_updater test_utils test_world
TEST_TARGETS := $(TEST_TARGETS) $(TSTS_$(d))

$(d)test: $(TSTS_$(d))

test_%: $(d)tst/test_%.py
	$(RUNP)


d := $(d_$(dirstack))
dirstack := $(basename $(dirstack))
