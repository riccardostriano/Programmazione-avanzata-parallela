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
#include "scene.h"
#include "utils.h"

int load_scene(char * path, scene_info * scene_file){
  /*
    Load a scene_info from a file

    parameters : 
        char * path -> indicates the path of the file
        scene_info * -> indicates the scene_info to populate
    returns (int) : 
        it returns the error code raised by the function
        0 : everything went well
        -1 : problem occurred while opening the requested path with fopen in reading+ mode
        -2 : problem occurred while reading a line. wrong format line
        others : refere to open image return error code 
    notes : 
        1. this function does not load the struct ppm_ptr now. this will be done by map_image
        2*. we must multiply width*height by the dimension of the struct rgb (3*sizeof(u_int8_t))
  */
    FILE * fd = fopen(path, "r+");
    scene_file->fd = fd;
    if (fd == NULL){
        return -1;
    }
    if (fscanf(fd, "VP %f %f %f\n", &(scene_file->vp.x), &(scene_file->vp.y), &(scene_file->vp.z)) != 3){
        fclose(fd);
        return -2;
    }
    if (fscanf(fd, "BG %hhu %hhu %hhu\n", &(scene_file->bg.r), &(scene_file->bg.g), &(scene_file->bg.b)) != 3){
        fclose(fd);
        return -2;
    }
    if (fscanf(fd, "OBJ_N %d\n", &(scene_file->obj_n)) != 1){
        fclose(fd);
        return -2;
    }
    scene_file->objects = (sphere *)malloc(scene_file->obj_n * sizeof(sphere));
    for(int i = 0; i < scene_file->obj_n; i++){
        float xi;
        float yi;
        float zi;
        float ri;
        rgb * col = (rgb *)malloc(sizeof(rgb));
        if (fscanf(fd, "S %f %f %f %f %hhu %hhu %hhu\n", &xi, &yi, &zi, &ri, &(col->r), &(col->g), &(col->b)) != 7){
            fclose(fd);
            return -2;
        }
        vector t;
        t.x = xi;
        t.y = yi;
        t.z = zi;
        scene_file->objects[i].center = t;
        scene_file->objects[i].radius = ri;
        scene_file->objects[i].color = *col;
    }

    fclose(fd);
    return 0;
}

int free_scene(scene_info * scene){
    free(scene->objects);
    return 0;
}
