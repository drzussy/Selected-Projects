from image_editor import *

image = [[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]], [
    [1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]


def separate_channels_test():
    assert separate_channels([[1, 1, 1]]) == [[1], [1], [1]]
    assert separate_channels([[[1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]], [
        [1, 2, 3], [1, 2, 3], [1, 2, 3]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]) == [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]], [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]], [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]


separate_channels()


# print(apply_kernel([[0, 128, 255]], blur_kernel(3)))
# print(apply_kernel([[10, 20, 30, 40, 50], [8, 16, 24, 32, 40], [
#       6, 12, 18, 24, 30], [4, 8, 12, 16, 20]], blur_kernel(5)))
# print(apply_kernel([[5, 2]], blur_kernel(3)))


# print(RGB2grayscale([[[200, 0, 14], [15, 6, 50]]]))
def bilinear_interpolation_test():
    assert (bilinear_interpolation([[0, 64], [128, 255]], 0, 0) == 0)
    assert (bilinear_interpolation([[0, 64], [128, 255]], 1, 1) == 255)
    assert (bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) == 112)
    assert (bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1) == 160)
    assert (bilinear_interpolation([[15, 30, 45, 60, 75], [90, 105, 120, 135, 150], [
        165, 180, 195, 210, 225]], (4/5), (8/3)) == 115)

# mat = [[2, 4, 6],
#        [3, 8, 12],
#        [16, 5, 11]]

# print(resize([[0, 10], [10, 0]], 2, 2))  # [[0, 10], [10, 0]]
# print(resize([[0, 10], [10, 0]], 3, 3))  # [0, 5, 10], [5, 5, 5], [10, 5, 0]]
# print(resize(mat, 2, 2))  # == [[2, 6], [16, 11]]
# print([[2, 3, 4, 4, 5, 6], [2, 4, 5, 6, 7, 8], [3, 5, 6, 8, 9, 11], [
#       6, 6, 7, 8, 10, 12], [11, 9, 7, 7, 9, 11], [16, 12, 7, 6, 9, 11]])
# print(resize(mat, 6, 6), "\n")
# print([[2, 3, 4, 4, 5, 6], [3, 5, 7, 9, 10, 12], [16, 12, 7, 6, 9, 11]])
# print(resize(mat, 3, 6), "\n")
# print([[2, 4, 6], [2, 6, 8], [3, 7, 11], [
#       6, 7, 12], [11, 6, 11], [16, 5, 11]])
# print(resize(mat, 6, 3), "\n")

# print(resize(mat, 4, 4), "\n")
# print([[2, 3, 5, 6], [3, 5, 8, 10], [7, 7, 9, 12], [16, 9, 7, 11]])


# print(rotate_90([[1, 2, 3], [4, 5, 6]], "R"))
# print(rotate_90([[1, 2, 3], [4, 5, 6]], "L"))
# print(rotate_90([[[1, 2, 3], [4, 5, 6]], [[0, 5, 9], [255, 200, 7]]], 'L'))