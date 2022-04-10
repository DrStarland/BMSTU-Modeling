#include "eyler.h"

inline double function(double x, double u) {
    return x * x + u * u;
}

double eylerMethod(double x, double y, double h) {
    return y + h * function(x, y);
};
