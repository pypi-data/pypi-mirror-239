import matplotlib.pyplot as plt
import random

class VectorPlot:
    def __init__(self, *vectors, labels, title='VectorPlot', xlabel='x-axis', ylabel='y-axis'):
        self.vectors = vectors
        self.labels = labels
        self.__min_max()  # Call the __min_max method in the constructor
        self.xlabel = xlabel
        self.ylabel = ylabel

    def __min_max(self):
        self.x_min = min(v[0] for v in self.vectors)
        self.x_max = max(v[0] for v in self.vectors)
        self.y_min = min(v[1] for v in self.vectors)
        self.y_max = max(v[1] for v in self.vectors)


    def __repr__(self):
        return f"<object> VectorPlot at {hex(id(self))}\ncan be visualized by self.show() ['self' is the instance of object.]\nExample:\na = VectorPlot([1,2])\na.show()"

    def show(self):
        for i in range(len(self.vectors)):
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            vector = self.vectors[i]
            plt.quiver(0, 0, vector[0], vector[1], scale=1, 
                       scale_units='xy', angles='xy', 
                       color=(red/255, green/255, blue/255), 
                       label=self.labels[i])
            plt.text(vector[0], vector[1], f"{self.labels[i]}")  # Fixed the reference to 'labels'
        plt.legend(frameon = False)
        # Set plot limits with some padding
        plt.xlim(self.x_min - 5, self.x_max + 4)
        plt.ylim(self.y_min - 5, self.y_max + 4)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.grid()
        plt.show()

    def save(self, file):
        plt.savefig(file)

# Example usage:
#a = vector([1, 2])
#b = vector([3, 4])
#c = a + b
#labels = ['a', 'b', 'a+b']
#vector_plot = VectorPlot(a, b, c, labels=labels)
#vector_plot.show()
