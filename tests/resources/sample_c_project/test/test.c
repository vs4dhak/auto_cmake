#include <stdio.h>
#include "add.h"
#include "subtract.h"
#include "multiply.h"
#include "divide.h"

int main() {
    int x = 10;
    int y = 5;

    // Using the add function
    printf("%d + %d = %d\n", x, y, add(x, y));

    // Using the subtract function
    printf("%d - %d = %d\n", x, y, subtract(x, y));

    // Using the multiply function
    printf("%d * %d = %d\n", x, y, multiply(x, y));

    // Using the divide function
    // Note: The divide function returns a float, so use %f to print the result
    printf("%d / %d = %f\n", x, y, divide(x, y));

    return 0;
}
