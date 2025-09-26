export LD_LIBRARY_PATH=`pwd`
CC = clang
CFLAGS = -Wall -pedantic -std=c99
SWIG = swig

all: a4

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

phylib_wrap.c phylib.py: phylib.i
	$(SWIG) -python phylib.i

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o 
	$(CC) $(CFLAGS) phylib_wrap.o -shared -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

a4: libphylib.so _phylib.so

clean:
	rm -f *.o *.so a4 phylib_wrap.c phylib.py 
