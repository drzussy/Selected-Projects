# C++ compiler
CC = g++

# Archiver program
AR = ar

# Archiver flags (create, insert, index)
ARFLAGS = rcs

# Target static library name
TARGET = libuthreads.a

# Source file
SRCS = uthreads.cpp

# Object file
OBJS = $(SRCS:.cpp=.o)

# Compiler flags (warnings, debug info)
CFLAGS = -std=c++11 -Wall

# Default target: build the library
all: $(TARGET)

# Rule to build the library from object files
$(TARGET): $(OBJS)
	$(AR) $(ARFLAGS) $@ $^

# Rule to compile .cpp to .o
%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

# Clean target: remove generated files
clean:
	rm -f $(OBJS) $(TARGET)

# Phony targets
.PHONY: all clean