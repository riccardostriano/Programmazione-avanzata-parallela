/*
    Riccardo Striano SM3201366
    Programmazione Avanzata e Parallela - Progetto C
    Anno 2024-2025
*/
#ifndef _UTILS_H
#define _UTILS_H

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

typedef struct viewport{
    float x;
    float y;
    float z;
}viewport;

struct __attribute__ ((packed)) _rgb{
    uint8_t r;
    uint8_t g;
    uint8_t b;
};

typedef struct _rgb rgb;

typedef struct vector{
    float x;
    float y;
    float z;
}vector;

typedef struct ppm_p6{
    int width;
    int height;
    int offset;
    int size;
    FILE * fd;
    rgb * data;
}ppm;

typedef struct sphere{
    vector center;
    float radius;
    rgb color;
}sphere;

typedef struct scene_info{
    viewport vp;
    rgb bg;
    int obj_n;
    sphere * objects;
    FILE * fd;
}scene_info;

float difference(vector a, vector b);
float distance(sphere s, vector v);
float inner_product(vector v, vector w);
int normalize(vector * v);
void print_color(rgb c);
void print_vector(vector v);
void print_sphere(sphere s);

#endif