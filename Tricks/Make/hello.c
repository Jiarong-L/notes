# include <stdio.h>

int add(int a, int b);
int minus(int a, int b);

int main(int argc, char** argv[])
{
    printf("Hello World!");
    printf("10+5=%d\n",add(10,5));
    printf("10-5=%d\n",minus(10,5));
    return 0;
}

