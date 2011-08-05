dirstack := $(dirstack).x
d_$(dirstack) := $(d)
d := $(dir $(lastword $(MAKEFILE_LIST)))

TSTS_$(d) := sol_test_boatperformance sol_test_boatwind sol_test_course \
	sol_test_functions sol_test_interpol sol_test_map sol_test_performance \
	sol_test_router sol_test_settings sol_test_weather sol_test_wind_online \
	sol_test_wind
TEST_TARGETS := $(TEST_TARGETS) $(TSTS_$(d))

sol_test_%: $(d)tst/test_%.py
	$(RUNP)

$(d)sol_test_%: $(d)tst/test_%.py
	$(RUNP)

$(d)test: $(TSTS_$(d))

#.PHONY: $(TSTS_$(d))

d := $(d_$(dirstack))
dirstack := $(basename $(dirstack))
