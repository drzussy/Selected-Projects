#################################################################
# FILE : image_editor.py
# WRITER : Noam Susman , noam.susman , 318528304
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that edits an image
# STUDENTS I DISCUSSED THE EXERCISE WITH: .
# WEB PAGES I USED: Geeks for# Geeks, stack overflow, we3schools
# NOTES: ...
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from typing import Optional
import copy
import math
import sys

##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_one_channel(image: list, color: int) -> list:
    '''This function recieves an image as a three dimensional list and
    strips one channel into an image in channel color and returns it as
    a two dimensional list. Variables - image(list) and color (The indicator
    which channel in the pixel to use)'''

    channel = [[pixel[color] for pixel in image[row]]
               for row in range(len(image))]
    return channel


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    '''this function recieves an image and returns a list of each channel'''

    channel_list = [separate_one_channel(image, color)
                    for color in range(len(image[0][0]))]
    return channel_list


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    '''this function recieves a list of images by channel and combines the
    into one colorful image'''
    image = []
    for row in range(len(channels[0])):
        image.append([])
        for pixel in range(len(channels[0][row])):
            image[row].append([])
            for i in range(len(channels)):
                image[row][pixel].append(channels[i][row][pixel])

    return image
    ...


def gray_pixelate(pixel: list) -> int:
    '''recieves a color pixel and returns a grayscale value for the pixel'''
    return round(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    '''generate a grayscale image from a colored image'''
    gray_image = [[gray_pixelate(pixal) for pixal in row]
                  for row in colored_image]
    return gray_image
    ...


def blur_kernel(size: int) -> Kernel:
    '''generates a blur for an odd positive integer'''
    size = int(size)
    return [[(1 / pow(size, 2)) for i in range(size)] for j in range(size)]
    ...


def validate_kernalized_pixel(pixel: int) -> int:
    '''makes sure all values of a kernelized pixel are between
    0 and 255 and corrects if not'''
    if pixel < 0:
        pixel = 0
    if pixel > 255:
        pixel = 255
    return round(pixel)


# def find_pixel_area_avg(row: int, col: int, image: list, size: int) -> int:
#     '''this function iterates over the span of a kernel relative to
#     a center starting point of any pixel in the image and returns the
#     kernelized pixel value'''
#     center = (size // 2)
#     pixel = 0
#     counter = 0
#     # iterate over span of kernel relative to center
#     for i in range(row - center, size - center + row):
#         for j in range(col - center, size - center + col):
#             # if not inside image (to the left or up)
#             if i < 0 or j < 0:
#                 counter += 1
#                 continue
#             # try to add current pixel, if error then add to counter
#             try:
#                 pixel += image[i][j]
#             except IndexError:
#                 counter += 1
#     # add overflow add kernelize pixel
#     pixel += (counter * image[row][col])
#     pixel = pixel / (size ** 2)
#     return int(validate_kernalized_pixel(pixel))

def find_pixel_area_avg(row: int, col: int, image: list, size: int) -> int:
    '''this function iterates over the span of a kernel relative to
    a center starting point of any pixel in the image and returns the
    kernelized pixel value'''
    center = (size // 2)
    pixel = 0
    counter = 0
    # iterate over span of kernel relative to center
    for i in range(row - center, size - center + row):
        for j in range(col - center, size - center + col):
            # if not inside image (to the left or up)
            if i < 0 or j < 0 or i >= len(image) or j >= len(image[0]):
                counter += 1
                continue
            pixel += image[i][j]
    # add overflow add kernelize pixel
    pixel = pixel / (size ** 2)
    return int(validate_kernalized_pixel(pixel))


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    '''applies any given kernel of an odd number size to in image and returns a
    kernelized image'''
    new_image = [[find_pixel_area_avg(i, j, image, len(kernel)) for j in range(
        len(image[i]))] for i in range(len(image))]
    return new_image


def check_corner(height: int, width: int, y: int, x: int) -> bool:
    '''check if pixel is a corner'''
    if y == 0 and x == 0:
        return True
    if y+1 == height and x == 0:
        return True
    if x+1 == width and y == 0:
        return True
    if x+1 == width and y+1 == height:
        return True
    return False


def find_delta(y: float, x: float):
    '''Find delta of a float'''
    y = float(y)
    x = float(x)
    if y.is_integer():
        delta_y = 1
    else:
        delta_y = y - math.floor(y)
    if x.is_integer():
        delta_x = 1
    else:
        delta_x = x - math.floor(x)
    return delta_y, delta_x


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    '''Interpolate a pixel from a new resized image based on the original image'''
    delta_y, delta_x = find_delta(y, x)
    # find natural number coordinates
    # check if corner and  if so interpolate
    if check_corner(len(image), len(image[0]), y, x):
        return image[y][x]
    # if check_side(image, y, x):
    x = math.ceil(x)
    y = math.ceil(y)
    # interpolate and return
    pixel = image[max(0, y-1)][max(0, x-1)]*(1-delta_x)*(1-delta_y) + image[y][max(0, x-1)]*delta_y*(
        1-delta_x) + image[max(0, y-1)][x]*delta_x*(1-delta_y) + image[y][x]*delta_x*delta_y
    # print(math.ceil(pixel))
    return round(pixel)


def find_relative_coordinates(new_height: int, new_width: int, i: int, j: int, image) -> tuple:
    '''Finds a pixels position from a resized image in the original image '''
    y = i / (new_height - 1) * (len(image)-1)
    x = j / (new_width - 1) * (len(image[0])-1)
    return y, x


def find_corner(image, new_height, new_width, i, j):
    '''Checks if a given relative loction is a corner and returns corner value'''
    if i == new_height - 1 and j == new_width - 1:
        return image[len(image)-1][len(image[0])-1]
    if i == new_height - 1 and j == 0:
        return image[len(image)-1][0]
    if i == 0 and j == new_width - 1:
        return image[0][len(image[0])-1]
    if i == 0 and j == 0:
        return image[0][0]


def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    '''this function resizes a unichannel image into a new size based on bilinear interpolation'''
    new_image = [[find_corner(image, new_height, new_width, i, j) if check_corner(new_height, new_width, i, j)
                  else bilinear_interpolation(image, *find_relative_coordinates(new_height, new_width, i, j, image))
                  for j in range(new_width)] for i in range(new_height)]
    return new_image
    ...


def rotate_90(image: Image, direction: str) -> Image:
    '''Rotate an image left or right (input is either 'L' or 'R') '''
    new_image = []
    for i in range(len(image[0])):
        new_image.append([])
        for j in range(len(image)):
            if direction == "L":
                new_image[i].append(copy.deepcopy(image[j][-i-1]))
                ...
            if direction == "R":
                new_image[i].append(
                    copy.deepcopy(image[len(image)-j - 1][i]))
    return new_image


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    '''generate an edge picture'''
    # blur image

    blur_size = int(blur_size)
    image = apply_kernel(image, blur_kernel(blur_size))
    new_image = []
    for i in range(len(image)):
        new_image.append([])
        for j in range(len(image[0])):
            threshold = find_pixel_area_avg(i, j, image, block_size) - c
            if image[i][j] < threshold:
                new_image[i].append(0)
            else:
                new_image[i].append(255)
    return new_image
    ...


def quantize_formula(pixel: int, n: int) -> float:
    '''runs a a unicolor pixel through a qunitization formula '''
    pixel = int(pixel)
    n = int(n)
    return round(math.floor(pixel * n / 256) * (255 / (n - 1)))


def quantize(image: SingleChannelImage, n: int) -> SingleChannelImage:
    '''Quanitizes a single channel image using the formula in quanitize_formula()'''
    new_image = [[quantize_formula(image[row][col], n) for col in range(
        len(image[0]))] for row in range(len(image))]
    return new_image
    ...


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    channels = separate_channels(image)
    quantized_channels = [quantize(channels[color], N)
                          for color in range(len(channels))]
    new_image = combine_channels(quantized_channels)
    return new_image
    ...


def check_valid_kernel_size(size: str) -> bool:
    if size.isnumeric():
        if int(size) % 2 == 1:
            return True
    return False


def is_rgb(image) -> bool:
    try:
        RGB2grayscale(image)
        return True
    except TypeError:
        return False


def blur_image(image):
    '''Blur any uni color and rgb image.'''
    size = input("What size kernel would you like to apply? ")
    if check_valid_kernel_size(size):
        size = int(size)
        if not is_rgb(image):
            new_image = apply_kernel(image, blur_kernel(size))
        else:
            channels = separate_channels(image)
            blurred_channels = [apply_kernel(channels[color], blur_kernel(size))
                                for color in range(len(channels))]
            new_image = combine_channels(blurred_channels)
            return new_image
    else:
        print("Invalid kernel size. Must be a positive odd whole number")


def check_valid_new_size(sizes):
    if "," in sizes:
        y, x = sizes.split(sep=",")
        if y.isnumeric() and x.isnumeric():
            if float(y) > 1 and float(x) > 1:
                if float(y).is_integer() and float(x).is_integer():
                    return True
    return False


def check_blur_sizes(variables):
    for i in range(len(variables) - 1):
        if check_valid_kernel_size(variables[i]):
            return True
    if check_positive_int(variables[2]):
        return True
    return False


def main_resize(image):
    new_size = input("What size image would you like? (Height,Width) ")
    if check_valid_new_size(new_size):
        sizes = new_size.split(sep=",")
        x = int(sizes[0])
        y = int(sizes[1])
        print(x, y)
        new_image = resize(image, y, x)
        return new_image
    else:
        print("Invalid input. Make sure that you inputed 'height,width' while\
            height and width are whole positive numbers that are larger them 1\
            and divided by a comma.")


def edges(image, blur_size, block_size, c):
    if is_rgb(image):
        new_image = get_edges(RGB2grayscale(image), int(
            blur_size), int(block_size), int(c))
    else:
        new_image = get_edges(image, int(blur_size), int(block_size), int(c))
    return new_image


def check_positive_int(str):
    if str.isnumeric():
        if int(str) > 1:
            return True
    return False


def quantize_any_image(image, N):
    if is_rgb(image):
        return quantize_colored_image(image, n)
    else:
        return quantize(image, n)
    ...


def check_command_line(sysargv):
    if len(sys.argv) != 2:
        print("Don't be a dumbass!")
        sys.exit()


if __name__ == '__main__':
    check_command_line(sys.argv)
    image = load_image(sys.argv[1])
    while True:
        flag = False
        user_input = input("How would you like to edit your image? \
            [1 - GrayScale, 2 - Blur, 3 - Resize, 4 - Rotate 90 degrees,\
            5 - Edges, 6 - Quanitize, 7 - Show image, 8 - Exit]\n")
        if user_input == "1":  # gray_scale
            if is_rgb(image):
                new_image = RGB2grayscale(image)
            else:
                print("Image is already grayscale")

        if user_input == "2":  # blur
            new_image = blur_image(image)

        if user_input == "3":  # resize
            new_image = main_resize(image)

        if user_input == "4":  # rotate
            direction = input("Which direction to rotate (L,R)? ")
            if direction in "LR":
                new_image = rotate_90(image, direction)
            else:
                print("Wrong input, function only accepts L or R")

        if user_input == "5":  # edges
            variables = input(
                "Choose Blur size, Block size and consant divided by commas: ")
            if variables.count(",") == 2:
                variables = list(variables.split(sep=","))
                variables = [float(variables[i])
                             for i in range(len(variables))]
                new_image = edges(
                    image, variables[0], variables[1], variables[2])

        if user_input == "6":  # quanitize image
            n = input("How many shades do you want? (0 <= int <= 256): ")
            if check_positive_int(n):
                new_image = quantize_any_image(image, int(n))
            else:
                print("Invalid input.\n")

        if user_input == "7":  # show image
            show_image(image)

        if user_input == "8":  # exit program
            while True:
                path = input("Where to save image to? ")
                try:
                    save_image(image, path)
                except ValueError:
                    continue
                break
            flag = True
        if flag == True:
            sys.exit()

        if 'new_image' in locals():  # save image before next loop
            if new_image != None:
                image = new_image
