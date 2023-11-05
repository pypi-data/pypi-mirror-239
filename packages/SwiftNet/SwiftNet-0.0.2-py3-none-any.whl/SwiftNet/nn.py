import matrix_math as mm
import numpy as np
import pickle
from mnist import MNIST


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def fake_desigmoid(x):
    return x * (1 - x)


def get_max(x):
    index = 0
    max = x[0]
    for i in range(len(x)):
        if x[i] > max:
            max = x[i]
            index = i

    return index


def load_MNIST():
    mndata = MNIST("samples")
    images, labels = mndata.load_training()
    test_images, test_labels = mndata.load_testing()

    return images, labels, test_images, test_labels


def get_correct(label):
    x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    x[label] = 1
    return x


class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, activation_function):
        # num of neurons for each layer
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.hidden_nodes = hidden_nodes
        self.bias_multiplier = 10
        self.weight_multiplier = 0.1

        self.weights = []

        # loops through the hidden_nodes list to create a 2D list off all the weights
        for i in range(len(self.hidden_nodes) + 1):
            # checks if its the first hidden layer
            if i == 0:
                y = self.input_nodes
            else:
                y = self.hidden_nodes[i - 1]

            # checks if its the last layer
            if i == len(self.hidden_nodes):
                x = self.output_nodes
            else:
                x = self.hidden_nodes[i]

            # adds the matrix to the list randomizes the weights to a between -1 and 1 times the multiplier
            self.weights.append(mm.matrix(x, y))
            self.weights[i].randomize(0.1)

        # loops through the num of hidden layers and creates a 1d matrix of the biases with a random value from -1 to 1 times the multiplier
        self.bias = []

        for i in range(len(self.hidden_nodes)):
            self.bias.append(mm.matrix(hidden_nodes[i], 1))
            self.bias[i].randomize(10)

        # adds the bias matrix for the outputs
        self.bias.append(mm.matrix(output_nodes, 1))
        self.bias[-1].randomize(10)

        # sets learning rate
        self.learning_rate = 0.3

        self.activation_function = activation_function

        self.net = [self.weights, self.bias]

    def reset_net(self):
        for weights in self.net[0]:
            self.weight.randomize(self.weight_multiplier)
        for bias in self.net[1]:
            self.bias.randomize(self.bias_multiplier)

    def load(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)

        if "[" in path:
            self.weights = data[0]
            self.bias = data[1]
        else:
            self.weights[0] = data[0]
            self.weights[1] = data[1]
            self.bias[0] = data[2]
            self.bias[1] = data[3]

    def save_net(self, path):
        with open(f"{path}.pickle", "wb") as f:
            pickle.dump(self.net, f)
            f.close()

    def feed_forward(self, input_array):
        # loads the input to a matrix
        inputs = mm.from_array(input_array)

        # loops through every  hidden layer and feeds the inputs forward
        activations = [inputs]
        for i in range(len(self.weights)):
            # multiples the prevoius layers activations by the weights and then adds the bias then applies the activation function
            activations.append(mm.multiply(self.weights[i], activations[i]))
            activations[i + 1].add(self.bias[i])
            activations[i + 1].map(self.activation_function)

        # returns the last layer activations as an array
        rtn = []
        for layer in activations:
            rtn.append(layer.to_array())
        return rtn

    def train(self, inputs_array, targets_array):
        # feeds the input through the net using the feed forward function
        activations = self.feed_forward(inputs_array)

        errors = [
            mm.subtract(mm.from_array(targets_array), mm.from_array(activations[-1]))
        ]

        # calculates the gradients and bias for each layer then it adds the gradients to the current layer
        for i in range(len(activations) - 1):
            # subtracts the targets and outputs to get the error
            errors.append(
                mm.multiply(
                    mm.transpose(self.weights[len(activations) - (i + 2)]), errors[i]
                )
            )

            # calculates the gradient by  multiplying the activation of the layer by the error of the next layer times the learning rate
            gradients = activations[len(activations) - (i + 1)]
            gradients = mm.from_array(gradients)
            gradients.multiply(errors[i])
            gradients.multiply(self.learning_rate)

            # calculates the deltas by multiplying the gradients by the weight
            activations_t = mm.transpose(
                mm.from_array(activations[len(activations) - (i + 2)])
            )
            weight_deltas = mm.multiply(gradients, activations_t)

            # adds the deltas and the gradients to the weights and bias
            self.weights[len(self.weights) - (1 + i)].add((weight_deltas))

    def test_net(self, test_images, test_labels):
        print("testing . . .")

        correct = 0
        total = 0
        for i in range(len(test_images)):
            output = self.feed_forward(test_images[i])
            if get_max(output[-1]) == test_labels[i]:
                correct += 1
            total += 1

        return (correct / total) * 100

    def test_and_train(
        self, test_images, test_labels, train_images, train_labels, iterations
    ):
        test_accuracys = []

        for j in range(iterations):
            print("training . . .")
            for i, image in enumerate(train_images):
                self.train(image, get_correct(train_labels[i]))
                print(f"{j},  {(i/len(train_images)*100)}")

            print("testing . . . ")
            test_accuracys.append(self.test_net(test_images, test_labels))

        return test_accuracys


def main():
    return


if __name__ == "__main__":
    main()
