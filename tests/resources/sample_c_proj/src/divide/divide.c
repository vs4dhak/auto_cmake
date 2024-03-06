#include "divide.h"

// Function to divide two numbers
float divide(int a, int b) {
    if (b == 0) {
        return 0; // Simple error handling for division by zero
    }
    return (float)a / b;
}
