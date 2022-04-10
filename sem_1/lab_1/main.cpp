#include <stdio.h>
#include <iostream>
#include <cmath>
#include "picar.h"
#include "eyler.h"


inline double function(double x, double u) {
    return x * x + u * u;
}

double methodRK(double x, double y, double h) {
    const double alpha = 1.;
    double k1 = function(x, y);
    double k2 = function(x + h / (2. * alpha), y + h / (2. * alpha) * k1);
    return y + h * ((1 - alpha) * k1 + alpha * k2);
};

int main() {
    int i = 0;
    const double h = 1e-5;
    for (double x = 0., yEy = 0., yRk = 0.; x < 2.; x += h, i++) {
        yEy = eylerMethod(x, yEy, h);
        yRk = methodRK(x, yRk, h);
        if (i % 4000 == 0 || fabs(x - 2.) < 1e-6) {
//            printf("%7.4lf | %9.4lf | %9.4lf | %9.4lf| %9.4lf | %9.4lf | %9.4lf\n",
//               x, picarMethod(x, 1), picarMethod(x, 2),
//               picarMethod(x, 3), picarMethod(x, 4),
//               yEy,
//               yRk
//            );

            printf("%5.2lf | %6.2lf | %6.2lf | %6.2lf| %6.2lf | %6.2lf | %6.2lf\n",
               x, picarMethod(x, 1), picarMethod(x, 2),
               picarMethod(x, 3), picarMethod(x, 4),
               yEy,
               yRk
            );
        }
    }

    return 0;
}
