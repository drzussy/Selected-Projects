// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

// Put your code here.
//whiten screen
@KBD
D=A
@SCREEN
D=D-A
@MAX
M=D
@i
M=0
(LOOP)
    //check if at end of screen
    //if i>max then end loop
    //else keep whitening screen and i=i+1
    @i
    D=M
    @MAX
    D=D-M
    // D=D+1
    @LOOP1
    D;JGE
    @i
    D=M
    @SCREEN
    A=A+D
    M=0
    @i
    M=M+1
    @LOOP
    D;JMP
//run infinite loop
(LOOP1)
//if key is pressed, blacken screen
//check if kbd is not pressed or pressed
    @i
    M=0
    @KBD
    D=M
    @LOOP
    D;JEQ
    //if not, blacken
    //loop to blacken all of screen, loop over rows of 16 bit registers from @SCREEN to 8192+SCREEN
    (LOOP2)
        @i
        D=M
        @MAX
        D=D-M
        @LOOP1
        D;JGE
        @i
        D=M
        @SCREEN
        A=A+D
        M=-1
        @i
        M=M+1
        @LOOP2
        0;JMP