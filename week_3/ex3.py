def input_list():
    '''prompts user for numbers (ints or floats), returns a list of the user inputs and also
    returns the sum of the inputs'''
    sum = 0
    num_list = []
    while True:
        cur_num = input()
        if cur_num == "":
            break
        sum += float(cur_num)
        num_list.append(float(cur_num))
    num_list.append(sum)
    return num_list

def inner_product(vec_1, vec_2):
    '''return inner product of two vectors'''
    if len(vec_1) != len(vec_2):
        return
    product = 0
    for i in range(len(vec_1)):
        product += vec_1[i] * vec_2[i]
    return product

def sequence_monotonicity(seq):
    '''check for sequence type'''
    seq_types = [True, True, True, True]
    if len(seq) == 0:
        return seq_types
    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1]:
            seq_types[1] = False
            seq_types[3] = False
        if seq[i] > seq[i - 1]:
            seq_types[2] = False
            seq_types[3] = False
        if seq[i] < seq[i - 1]:
            seq_types[0] = False
            seq_types[1] = False
    return seq_types

def monotonicity_inverse(bool_list):
    '''return a 4 number example of a sequence requested by user'''
    #predetermined examples
    UP = [1,1,1,2]
    DOWN = [2,1,1,1]
    RL_UP = [0,1,2,3]
    RL_DOWN = [3,2,1,0]
    CONST = [1,1,1,1]
    RANDOM = [1,0,1,0]
    if True not in bool_list:
        return RANDOM
    if False not in bool_list:
        return
    #check for one legal true
    if bool_list[1] and sequence_monotonicity(RL_UP) == bool_list:
        return RL_UP
    if bool_list[3] and sequence_monotonicity(RL_DOWN) == bool_list:
        return RL_DOWN
    #check up
    if bool_list[0]:
        #checks for both up and down
        if bool_list[2] and sequence_monotonicity(CONST) == bool_list:
            return CONST
        elif sequence_monotonicity(UP) == bool_list:
            return UP   
    if bool_list[2] and sequence_monotonicity(DOWN) == bool_list:
        return DOWN

def convolve(mat):
    '''returns the matrix of the convolve values of a given matrix'''
    if not len(mat):
        return
    prod = []
    for i in range(1, len(mat)-1):  # iterate over rows excluding first and last
        prod.append([])
        for j in range(1, len(mat[0])-1):#iterate over columns excluding first and last
            cur_sum = 0
            for s in range(3): #calculate convolve
                cur_sum += sum(mat[i-1+s][j-1:j+2])
            prod[i-1].append(cur_sum) #add to final product
    return prod


def sum_of_vectors(vec_list):
    '''returns a vector that is the sum of a list of vectors'''
    if not len(vec_list):
        return
    if not len(vec_list[0]):
        return []
    prod = [0] * len(vec_list[0])
    for i in range(len(vec_list)):
        for j in range(len(vec_list[i])):
            prod[j] += vec_list[i][j]
    return prod

def num_of_orthogonal(vectors):
    '''return the amount of orthogonal pairs in a list of vectors'''
    counter = 0
    for i in range(len(vectors)):
        for j in range(i+1, len(vectors)):
            if not inner_product(vectors[i], vectors[j]):
                counter += 1
    return counter

if __name__ == "__main__":
    input_list()
    inner_product()
    sequence_monotonicity()
    monotonicity_inverse()
    convolve()
    sum_of_vectors()
    num_of_orthogonal()