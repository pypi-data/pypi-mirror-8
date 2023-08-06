CC = gcc
OPT = -march=native -O3 -funroll-loops
CFLAGS = -Wall -pedantic  $(OPT) -fpic  # -g -pg

all: lib exec

lib: libeafbb.so

exec: eafbb

libeafbb.so: algorithm.o dataload.o heuristic.o eafbb.o
	$(CC) -shared -o libeafbb.so dataload.o algorithm.o heuristic.o eafbb.o

eafbb: algorithm.o dataload.o heuristic.o eafbb.o main.o
	$(CC) $(CFLAGS) -o eafbb dataload.o algorithm.o heuristic.o eafbb.o main.o

#eafbb.o:
#	$(CC) $(CFLAGS) -c -o eafbb.o -fpic eafbb.c	

clean:
	$(RM) *.o

distclean: clean
	$(RM) eafbb libeafbb.so

