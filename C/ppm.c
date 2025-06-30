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
#include "ppm.h"

int empty_image(char * path, ppm_ptr img, int width, int height)
{
  /*
    Create an empty image and the open it

    parameters : 
        char * path -> indicates the path of the image
        ppm_ptr img -> indicates the pointer to the struct retaining the data for the image
        int width -> indicates the width (in pixel) of the image
        int height -> indicates the height (in pixel) of the image
    returns (int) : 
        it returns the error code raised by the function
        0 : everything went well
        -1 : problem occurred while opening the requested path with fopen in written+ mode
        others : refere to open image return error code 
    notes : 
        1. this function does not load the struct ppm_ptr now. this will be done by map_image
        2*. we must multiply width*height by the dimension of the struct rgb (3*sizeof(u_int8_t))
  */
  FILE * fd = fopen(path, "w+"); 
  if (fd == NULL) {
    return -1;
  }
  // writing the header
  int written = fprintf(fd, "P6\n%d %d\n255\n", width, height);
  // resizing the dimension of the file at the correct one
  // 2*
  int errn = ftruncate(fileno(fd), written + width * height * sizeof(rgb)); 
  if (errn != 0){
    printf("ERROR OCCURRED WHILE USING FTRUNCATE\n");
  }
  fclose(fd);
  return open_image(path, img);
}

int open_image(char * path, ppm_ptr img)
{
  /*
    Open an image an map it with mmap
    
    parameters : 
        char * path -> indicates the path of the image
        ppm_ptr img -> indicates the struct retaining the data for the image
    returns (int) : 
        it returns the error code raised by the function
        0 : everything went well
        -2 : problem occurred while opening the requested path with fopen in reading+ mode
        -3 : problem occurred while reading the header of the file
        -4 : problem occurred while mapping the file with mmap 
    notes :
        1. at the end of the function we actually have access to the single pixel of the file like if they were an array thanks to mmap
  */
  FILE * fd = fopen(path, "r+");
  img->fd = fd;
  if (fd == NULL){
    return -2;
  }
  //obtaining total dimension
  struct stat fileStat;
  stat(path, &fileStat);
  img->size = fileStat.st_size;
  //reading the header
  if (fscanf(fd, "P6\n%d %d\n255\n", &img->width, &img->height) != 2){
    fclose(fd);
    return -3;
  }
  //finding the offset
  img->offset = ftell(fd);
  //mmaping the file 
  img->data = mmap(NULL, img->size, PROT_READ | PROT_WRITE, MAP_SHARED, fileno(fd), 0);
  if (img->data == MAP_FAILED) {
    fclose(fd);
    return -4;
  }
  return 0;
}

rgb * pixel_at(ppm_ptr img, int x, int y)
{
  /*
    Return the pixel of an image in at coordinate (x, y)
    
    parameters : 
        ppm_ptr img -> indicates the struct retaining the data for the image
        int x -> indicates the x coordinate of the pixel
        int y -> indicates the y coordinate of the pixel
    returns (struct rgb *) : 
        it returns the pointer to the pixel. 
        OTHERWISE
        NULL : image is NULL or (x, y) are invalid coordinates

    notes :
        1*. we must perform the cast to obtain the correct index. we start with the char * 
            just to have something with 1byte dimension (we could have used also u_int8_t)
            then we find the right position and then we cast to rgb *

  */
  if (img == NULL){
    return NULL;
  }
  if ( (x >= img->width) || (y >= img->height) || (x < 0) || (y < 0)){
    return NULL;
  }
  // 1*
  return (rgb *)((char * )img->data + img->offset + (y*img->width + x)*sizeof(rgb));
}

int close_image(ppm_ptr img)
{
  /*
    Deallocate the img
    
    parameters : 
        ppm_ptr img -> indicates the struct retaining the data for the image
    returns (struct rgb *) : 
        0 : everything went well
        -1 : image is NULL or (x, y) are invalid coordinates

    notes:

  */
  if (img == NULL){
    return -1;
  }
  munmap(img->data, img->size);
  fclose(img->fd);
  return 0;
}
