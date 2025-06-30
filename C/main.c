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
#include <float.h>
#include <math.h>
#include "utils.h"
#include "ppm.h"
#include "scene.h"

int raytraicing(scene_info scene, ppm * img, int width, int height){
    /*
    Function that performs raytraycing of the given scene.

    parameters : 
        scene_info -> indicates the scene_info
        ppm * -> indicates the struct retaining the data for the image
    returns (int) : 
        it returns the error code raised by the function
        0 : everything went well
    notes : 
        1*. we parallelize the outer cycle
        2*. we must use for the t_i vector y cordinate the y as height - 1 - y to flip the image correctly
        3*. we find the minimum iteratively and update the minimum and the color at the same time
  */
    sphere * objs = scene.objects;
    rgb def = scene.bg;
    viewport v = scene.vp;
    int obj_n = scene.obj_n;
    // 1*
    #pragma omp parallel for collapse (2)
    for (int x = 0; x < width; x ++){
        for (int y = 0; y < height; y ++){
            vector t;
            t.x = ((v.x/(width-1))*x - v.x/2);
            // 2*
            t.y =  ((v.y/(height-1))*(height - 1 - y) - v.y/2);
            t.z = 1;
            int errn = normalize(&t);
            if (errn != 0){
                printf("ERROR WHILE NORMALIZING THE VECTOR \n");
            }
            rgb pixel_color = def;
            // 3*
            float min_distance = FLT_MAX;
            for (int i = 0; i < obj_n; i++){
                float dist = distance(objs[i], t);
                if (dist != -1 && dist < min_distance){
                    min_distance = dist;
                    pixel_color = objs[i].color;
                }
            }
            rgb * dest;
            dest = pixel_at(img, x, y);
            * dest = pixel_color;
        }
    }
    return 0;
}

int main(int argc, char *argv[]){
    // DEFAULT PARAMETERS
    char * scene_path = "scene_test.txt";
    char * img_path = "img_test.ppm";
    int width = 1920;
    int height = 1080;

    // INPUT HANDLER
    if (argc != 5){
        printf("Using default parameters for the execution : \nscene located in : %s\nimage located in : %s\nwidth : %d\nheight : %d\n", scene_path, img_path, width, height);
    }
    else{
        scene_path = argv[1];
        img_path = argv[2];
        width = atoi(argv[3]);
        height = atoi(argv[4]);
    }

    // SCENE OPENING
    scene_info scene;
    int errn = load_scene(scene_path, &scene);
    if (errn != 0 ){
        printf("LOAD SCENE ERROR %d \n", errn);
    }
    // IMG OPENING
    ppm img;
    errn = empty_image(img_path, &img, width, height);
    if (errn != 0 ){
        printf("EMPTY IMAGE ERROR %d \n", errn);
    }
    // RAYTRAYCING
    errn = raytraicing(scene, &img, width, height);
    if (errn != 0 ){
        printf("RAYTRACING ERROR %d \n", errn);
    }
    // IMG CLOSING
    errn = close_image(&img);
    if (errn != 0 ){
        printf("CLOSE IMAGE ERROR %d \n", errn);
    }
    // SCENE CLOSING
    errn = free_scene(&scene);
    if (errn != 0 ){
        printf("CLOSE SCENE ERROR %d \n", errn);
    }
    printf("Process Done. We remember you that you'll find the image at the %s location.\n", img_path);
    return 0;
}