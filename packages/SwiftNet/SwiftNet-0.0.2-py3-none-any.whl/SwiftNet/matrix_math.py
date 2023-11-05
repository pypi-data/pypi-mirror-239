import random
import numpy as np



class matrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.values = []

        for i in range(rows):
            self.values.append([])
            for j in range(cols):
                self.values[i].append(0)
    
    def multiply(self, n):
        if(type(n)==matrix):

            result = np.multiply(self.values, n.values)
            self.values = result

        else:
            # Scalar Product
            for i in range(self.rows):
                for j in range(self.cols):
                    self.values[i][j] *= n

    def map(self, fn):
        # appyl a function to every element of a matrix
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.values[i][j]
                self.values[i][j] = fn(val)

    def add(self, n):
        if type(n)==matrix:
         
             result = np.add(self.values, n.values)
             self.values = result

        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.values[i][j] += n

    def randomize(self, multiplier):
        for i in range(self.rows):
            for j in range(self.cols):
                self.values[i][j] = random.uniform(-1*multiplier, 1*multiplier)



    
    def to_array(self):
        arr = []
        for i in range(self.rows):
            for j in range(self.cols):
                arr.append(self.values[i][j])

        return arr

    def log(self):
        for i in range(self.rows):
            print(self.values[i])
        print("###################")
        return True


def map(a, fn):

    result = matrix(a.rows, a.cols)

    # appyl a function to every element of a matrix
    for i in range(a.rows):
        for j in range(a.cols):
            val = a.values[i][j]
            result.values[i][j] = fn(val)

    return result

def transpose(a):
    result = matrix(a.cols, a.rows)

    result.values = np.array(a.values).transpose()
    
    return result

def from_array(arr):
    m = matrix(len(arr), 1)
    for i in range(len(arr)):
        m.values[i][0] = arr[i]

    return m

def subtract(a, b):
    result = matrix(a.rows, a.cols)
    result.values = np.subtract(a.values, b.values)

    return result

def multiply(a, b):
    #Matrix Product
    if a.cols != b.rows:
        print("Matrix Multiply Size miss match(cols must = rows)")
        return False
    
    result = matrix(a.rows, b.cols)

    result.values = np.dot(a.values, b.values)

    return result


def main():
    pass



if __name__ == "__main__":
    main()