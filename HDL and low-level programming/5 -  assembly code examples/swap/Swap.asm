// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
@i
M=0
@j
M=0
@R14
A=M
D=M
@MAX
M=D
@MIN
M=D
@R14
D=M
@MAXI
M=D
@MINI
M=D
//find max of array
//loop over array, 
(LOOPMAX)
    //check if at end of array
    @i
    M=M+1
    D=M+1
    @R15
    D=D-M
    @LOOPMIN
    D;JGT
    //each time comparing arr[i] to min
    //if arr[i] > max, max=arr[i] 
    @i
    D=M
    @R14
    A=A+D
    D=M
    @MAX
    D=M-D
    //if arr[i] < MAX go to top of loop, else continue
    @LOOPMAX
    D;JGE
    //set MAXI to new index
    @i
    D=M
    @MAXI
    M=M+D
    //set MAX to arr[i]
    @i
    D=M
    @R14
    D=D+M
    A=D
    D=M
    @MAX
    M=D
    @LOOPMAX
    0;JMP
    
    




//find min of array
//loop over array
(LOOPMIN)
    //   each time comparing arr[i] to min
        //check if at end of array
    @j
    M=M+1
    D=M+1
    @R15
    D=D-M
    @LOOPSWAP
    D;JGT
    
    //each time comparing arr[j] to min
    //if arr[j] > MAX, MAX=arr[j] 
    @j
    D=M
    @R14
    A=A+D
    D=M
    @MIN
    D=D-M  
    //if arr[j] > MIN go to top of loop, else continue
    @LOOPMIN
    D;JGE
    //set MINI to new index
    @j
    D=M
    @MINI
    M=M+D
    //set MIN to arr[j]
    @i
    D=M
    @R14
    D=D+M
    A=D
    D=M
    @MIN
    M=D
    @LOOPMAX
    0;JMP

//swap min and max


//min = temp
(LOOPSWAP)
    //temp = max
    @MAX
    D=M
    //save max val in temp
    @TEMP
    M=D
    //max = min
    @MIN
    D=M
    //go to max index
    @MAXI
    A=M
    //place min in max
    M=D
    //get max val from temp
    @TEMP
    D=M
    //go to min index 
    @MINI
    A=M
    //place max in min
    M=D

(END)
    @END
    0;JMP
