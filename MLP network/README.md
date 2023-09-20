# MLP Network
### This program was given as the first assignment in the CPP part of the C\CPP workshop course in the Computer Science program of the Hebrew University. This program implements a MLP NN designed to read images of handwritten digits with high predictability, helping learn concepts in OOP and CPP such as classes, const & const return types, references and operator overloading.

## Network Architecture
The architecture of this NN is 4 layered with each layer's input being multiplied by a matrix of row dimensions matching the next layer's input size (the weights). Following the linear transformation implemented by the matrix multiplication, a bias is added and an activation function used before passing the output on as the next layers input. Exact dimensions and functions used in each layer are presented in this table:
| Layer | Linear Transformation | Weight Dimensions | Bias | Activation Function |
|:-------:|:-----------------------:|:-------------------:|:------:|:---------------------:|
|   1   | <img src="https://render.githubusercontent.com/render/math?math=T:\mathbb{R}^{784}\rightarrow\mathbb{R}^{128}"> | <img src="https://render.githubusercontent.com/render/math?math=W \in M_{128\times784}"> | <img src="https://render.githubusercontent.com/render/math?math=b_{1} \in \mathbb{R}^{128}"> | <img src="https://render.githubusercontent.com/render/math?math=Relu">|
|   2   | <img src="https://render.githubusercontent.com/render/math?math=T:\mathbb{R}^{128}\rightarrow\mathbb{R}^{64}"> | <img src="https://render.githubusercontent.com/render/math?math=W \in M_{64\times128}"> | <img src="https://render.githubusercontent.com/render/math?math=b_{2} \in \mathbb{R}^{64}"> | <img src="https://render.githubusercontent.com/render/math?math=Relu">|
|   3   | <img src="https://render.githubusercontent.com/render/math?math=T:\mathbb{R}^{64}\rightarrow\mathbb{R}^{20}"> | <img src="https://render.githubusercontent.com/render/math?math=W \in M_{20\times64}"> | <img src="https://render.githubusercontent.com/render/math?math=b_{3} \in \mathbb{R}^{20}"> | <img src="https://render.githubusercontent.com/render/math?math=Relu">|
|   4   | <img src="https://render.githubusercontent.com/render/math?math=T:\mathbb{R}^{20}\rightarrow\mathbb{R}^{10}"> | <img src="https://render.githubusercontent.com/render/math?math=W \in M_{10\times20}"> | <img src="https://render.githubusercontent.com/render/math?math=b_{4} \in \mathbb{R}^{10}"> | <img src="https://render.githubusercontent.com/render/math?math=SoftMax">|

After going through the network, each coordinate in the vector is assigned a probability with the number assigned the highest probability being the correct prediction.
We note that this program was built with trained weights and biases already available, with no training implemented in this program.

## Program Input
Trained biases and weights are provided in separate files for each layer, as an array of floats of length of the multiplication of the relevant matrix or vector. The program file can be called with these files given as parameters. Subsequently, the user will be asked to enter a path as an image to be processed - the image shall be coded as a binary matrix of pixels of shades of gray of the following dimensions - <img src="https://render.githubusercontent.com/render/math?math=M_{28\times28}"> again vectorized as an array of floats.

## Code Design
The program was designed with 4 main class used:
1. Matrix - Implements the mathematical abstraction of a Matrix including various mathematical operations on Matrices.
2. Activation - Implements the different activation functions used in the different layers.
3. Dense - Implements a layer in the NN including applying a layer to an input.
4. MlpNetwork - Implements the whole NN, including applying the network to an input.