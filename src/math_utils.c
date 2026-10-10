#include "math_utils.h"
int calculate_crc_step(int current, int byte) 
{
    return (current ^ byte) + 1;
}
