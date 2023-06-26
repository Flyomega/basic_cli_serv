gcc -c fibo/fibo.c -fpic -o fibo/fibo.o

gcc -shared -o fibo/libfibo.so fibo/fibo.o