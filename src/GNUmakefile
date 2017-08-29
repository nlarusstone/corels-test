CFLAGS := -g -W -fPIC -Wall -Wno-unused-parameter -I. -DGMP -O$(O)

ifneq (,$(filter $(shell uname -n),elaines-MacBook-Pro.local Nicholass-Air-5.wireless.yale.internal))
    LIBS := -L/usr/local/lib
    CFLAGS += -I/usr/local/include
else
    LIBS :=
endif

LIBS += -L/usr/local/lib -lgmpxx -lgmp

ifneq ($(shell uname -n),beepboop)
    LDFLAGS :=
    CFLAGS += -fno-omit-frame-pointer
    ifneq ($(shell uname -r),15.6.0)
        LIBS += -lprofiler -ltcmalloc
    endif
else
    LDFLAGS :=
endif

ifneq ($(shell uname),Darwin)
    LIBS += -lbsd
endif

CC = gcc
CXX = g++ -std=c++11

DEPSDIR := .deps

CLEAN = corels evaluate-test *~ *.o *.so

all: corels libcorels.so evaluate-test

corels: cli.o params.o run.o corels.o pmap.o cache.o rulelib.o utils.o
	$(CXX) $(CFLAGS) $^ -o $@ $(LDFLAGS) $(LIBS)

libcorels.so: run.o params.o corels.o pmap.o cache.o rulelib.o utils.o
	$(CXX) -shared  -Wl,-soname,$@ -o $@ $^

evaluate-test: evaluate-test.o evaluate.o params.o run.o corels.o pmap.o cache.o rulelib.o utils.o
	$(CXX) $(CFLAGS) $^ -o $@ $(LDFLAGS) $(LIBS)

cli.o: cli.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

run.o: run.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

corels.o: corels.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

pmap.o: pmap.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

utils.o: utils.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

cache.o: cache.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

rulelib.o: rulelib.c $(DEPSDIR)/stamp
	$(CC) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

params.o: params.c $(DEPSDIR)/stamp
	$(CC) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

evaluate-test.o: evaluate-test.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

evaluate.o: evaluate.cc $(DEPSDIR)/stamp
	$(CXX) $(CFLAGS) $(DEPCFLAGS) -c $< -o $@

$(DEPSDIR)/stamp:
	mkdir -p $(dir $@)
	touch $@

clean:
	$(RM) $(wildcard $(CLEAN))
	$(RM) -r $(DEPSDIR)

DEPFILES := $(wildcard $(DEPSDIR)/*.d)
ifneq ($(DEPFILES),)
include $(DEPFILES)
endif

.PHONY: all clean
.SUFFIXES:
