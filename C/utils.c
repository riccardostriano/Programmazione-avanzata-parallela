/*
    Riccardo Striano SM3201366
    Programmazione Avanzata e Parallela - Progetto C
    Anno 2024-2025
*/
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include "utils.h"
#include <math.h>

void print_color(rgb c){
    printf("R %hhu G %hhu B %hhu\n", c.r, c.g, c.b);
}

void print_vector(vector v){
    printf("X %f Y %f Z %f \n", v.x, v.y, v.z);
}

void print_sphere(sphere s){
    print_vector(s.center);
}

int normalize(vector * v){
    float norm = sqrt((pow(v->x, 2) + pow(v->y, 2) + pow(v->z, 2)));
    if (norm == 0){
        return -1;
    }
    v->x /= norm;
    v->y /= norm;
    v->z /= norm;
    return 0;
}

float inner_product(vector v, vector w){
    return (v.x*w.x + v.y*w.y + v.z * w.z);
}

float distance(sphere s, vector v){
    float a = inner_product(v, v);
    float b = -2*inner_product(s.center, v);
    float c = inner_product(s.center, s.center) - s.radius*s.radius;
    float delta = (b*b - 4*a*c);
    if (delta < 0){
        return -1; // Default for saying no-intersection found
    }else if (delta == 0){
        return fabs(-b/(2*a));
    }else{
        return fmin(fabs((-b+sqrt(delta))/(2*a)), fabs((-b-sqrt(delta))/(2*a)));
    }
}