#include <gtest/gtest.h>
extern "C" {
#include "math_utils.h"
}

TEST(MathUtilsTest, BasicCheck) 
{
    EXPECT_EQ(calculate_crc_step(0x00, 0xAA), 0xAB);
}
