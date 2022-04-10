#include "picar.h"
#include <cmath>
#include <iostream>

double picar1(double x) {
    return x * x * x / 3.0;
}

double picar2(double x) {
    double temp = picar1(x);
    return  temp * (1. + temp * x / 7.0);
}

double picar3(double x) {
    double t = powl(x, 11);
    return picar2(x) + t / 1039.5 + t * powl(x, 4) / 59535.0;
}

double picar4(double x) {
    double factor = powl(x, 4); // x^4
    double t = powl(factor, 3) / x; // (x^4)^3 / x = x^11
    double result = picar3(x);
    result += ((t *= factor) / 46777.5); // x^15
    result += ((t *= factor) / 1696747.5); // x^19
    result += ((t) / 1244281.5); // x^19
    result += ((t *= factor) / 43133107.5); // x^23
    result += (t / 99411543.); // x^23
    result += ((t *= factor) / 1670939077.5);  // x^27
    result += ((t *= factor) / 109876902975.0);  // x^31
    return result;
}

double picarMethod(double x, int approxType) {
    double result = 0;
    switch (approxType) {
    case 1:
        result = picar1(x);
        break;
    case 2:
        result = picar2(x);
        break;
    case 3:
        result = picar3(x);
        break;
    case 4:
        result = picar4(x);
        break;
    default:
        std::cerr << "Unknown approximation level.";
    }
    return result;
}
