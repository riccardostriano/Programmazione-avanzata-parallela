/*
    Riccardo Striano SM3201366
    Programmazione Avanzata e Parallela - Progetto C
    Anno 2024-2025
*/

#ifndef _PPM_H
#define _PPM_H

#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

typedef struct ppm_p6 * ppm_ptr;

int open_image(char * path, ppm_ptr img);

int empty_image(char * path, ppm_ptr img, int width, int height);

rgb * pixel_at(ppm_ptr file, int x, int y);

int close_image(ppm_ptr img);

#endif
