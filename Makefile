RUNP = cd $(dir $<) && python2.7 $(notdir $<)

include softsailor/module.mk

include softsailor.mk
