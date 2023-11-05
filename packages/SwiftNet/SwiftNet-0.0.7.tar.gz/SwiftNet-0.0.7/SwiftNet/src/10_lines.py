import nn

images, labels, test_images, test_labels = nn.load_MNIST()

network = nn.NeuralNetwork(784, [10], 10, nn.sigmoid)  # creates network
accuracy = network.test_and_train(test_images, test_labels, images, labels, 1)
print(accuracy)
network.save_net(f"saved_nets/[10] {accuracy[0]}")
