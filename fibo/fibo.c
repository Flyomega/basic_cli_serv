#include "fibo.h"


int fibo(int n)
{
    int a = 0;
    int b = 0;
    int c = 1;

    while(n > 0)
    {
        a = b;
        b = c;
        c = a + b;
        n--;
    }
    return b;
}