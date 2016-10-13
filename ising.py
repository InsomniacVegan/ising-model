import numpy as np

class IsingModel:
    """
    IsingModel controls the behaviour of the Ising model for use with the demonstration.
    It handles the initialising of the model and its evolution through time. The inputs/outputs
    of the model are handled by main.py for interfacing with different input devices and displays.
    """

    def __init__(self, nx=25, ny=25, init_state_filename=None, spin_config=None):
        """
        Initialise state array and populate either from given file or as all 1.0.
        """

        # Record
        self.dim = [nx, ny]

        self.state_matrix = np.empty([nx, ny])
        if init_state_filename is not None:
            self.state_matrix = np.loadtxt(init_state_filename, comments='#')
        elif spin_config is not None:
            self.state_matrix.fill(1.0)
        elif spin_config is None:
            self.state_matrix.fill(1.0)

        # Initialise probability matrix and seed NumPy's random number generator
        self.prob_matrix = {}
        np.random.seed()

    def update_params(self, temp, ext_field):
        """Updates model parameters"""

        self.temp = temp
        self.ext_field = ext_field

        self._calc_prob_matrix()

    def evolve_model(self):
        """Evolves the model one time step"""

        # Choose random site
        x = np.random.randint(0, self.dim[0])
        y = np.random.randint(0, self.dim[1])

        # Calculate energy change in flipping spin
        dE = 2.0*self.state_matrix[x,y]*(self._sum_nn(x,y)+self.ext_field)

        # Flip spin if it lowers energy
        if dE < 0.00000001:
            self.state_matrix[x,y] *= -1
        # Otherwise test against random number and probability matrix
        elif (np.random.random() <
                  self.prob_matrix[(self.state_matrix[x,y]*self._sum_nn(x,y))/2.0]):
            self.state_matrix[x,y] *= -1

    def _calc_prob_matrix(self):
        """Uses symmetry to calculate all necessary probability values"""

        for i in range(-4, 5, 2):
            dE = 2.0*(i+self.ext_field)
            self.prob_matrix[i/2] = np.exp(-dE/self.temp)

    def _sum_nn(self, x, y):
        """Calculates the sum of spins of nearest neighbours"""

        return (self.state_matrix[np.mod(x-1, self.dim[0]), y] +
               self.state_matrix[np.mod(x+1, self.dim[0]), y] +
               self.state_matrix[x, np.mod(y-1, self.dim[1])] +
               self.state_matrix[x, np.mod(y+1, self.dim[1])]
                )
