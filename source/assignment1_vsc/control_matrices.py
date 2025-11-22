import numpy as np

# LQR Matrices
class LQRController:

    def __init__(self):
        self.Q = np.array([
            [1.000000000000, 0.000000000000],
            [0.000000000000, 1.000000000000]])

        self.R = np.array([
            [0.200000000000]])

        self.P = np.array([
            [3.389425601462, 1.024695076596],
            [1.024695076596, 1.980390094004]])

        self.K = np.array([
            [-1.068346690576, -1.810540812138]])

class TerminalSet:

    def compute_x_lims(self, plans, thetas, N):
        b_left = np.zeros((len(thetas), len(self.b_invariant)))
        b_right = np.zeros((len(thetas), len(self.b_invariant)))
        x_lim_b_reduced = np.zeros((len(thetas), 2))

        for t in range(len(thetas)):

            for i in range(len(self.b_invariant)):
                if abs(self.A_invariant[i, 0]) < 1e-5:
                    b_left[t, i] = -5 # invisible
                    b_right[t, i] = 1e6
                    continue

                if self.A_invariant[i, 0] > 0.:
                    b_right[t, i] = self.b_invariant[i] - self.A_invariant[i, 1] * plans[1, N, t] - self.A_invariant[i, 2] * thetas[t]
                    b_right[t, i] /= self.A_invariant[i, 0]
                    b_left[t, i] = -5
                else:
                    b_left[t, i] = self.b_invariant[i] - self.A_invariant[i, 1] * plans[1, N, t] - self.A_invariant[i, 2] * thetas[t]
                    b_left[t, i] /= self.A_invariant[i, 0]
                    b_right[t, i] = 1e6

            # Select the extreme constraints
            max_min = -10
            min_max = 1e6
            for i in range(len(b_left[t, :])):
                # Left side
                if b_left[t, i] > max_min:
                    x_lim_b_reduced[t, 0] = b_left[t, i]
                    max_min = b_left[t, i]

                # right side
                if b_right[t, i] < min_max:
                    x_lim_b_reduced[t, 1] = b_right[t, i]
                    min_max = b_right[t, i]

        self.x_lim_b = x_lim_b_reduced

    def __init__(self):

        # Terminal set matrices
        self.A_invariant = np.array([
            [-0.283527537682, -0.151271618793, -0.946957777688],
            [0.000000000000, 0.000000000000, 1.000000000000],
            [-0.082091857205, -0.047139306620, -0.995509323287],
            [-0.152334914111, -0.084942858275, -0.984671917326],
            [-0.510621419225, -0.253612560679, -0.821551237169],
            [-0.088681137550, 0.992104486274, 0.088681137550],
            [-0.693337525794, -0.196382663823, 0.693337525794],
            [0.693337525794, 0.196382663823, -0.693337525794],
            [0.786353151772, 0.342166470751, 0.514364488463],
            [-0.786353151772, -0.342166470751, -0.514364488463],
            [-0.943427805315, -0.297994805023, -0.145406575980],
            [0.943427805315, 0.297994805023, 0.145406575980],
            [0.704785091291, -0.080968822316, -0.704785091291],
            [-0.704785091291, 0.080968822316, 0.704785091291],
            [0.088681137550, -0.992104486274, -0.088681137550],
            [1.000000000000, 0.000000000000, 0.000000000000],
            [-1.000000000000, 0.000000000000, 0.000000000000],
            [0.000000000000, 0.000000000000, -1.000000000000]])

        self.b_invariant = np.array([
            [1.230485315370],
            [99.000000000000],
            [1.077601180492],
            [1.137006831438],
            [1.332172656394],
            [8.554478094730],
            [10.534910439216],
            [10.534910439216],
            [130.071764023525],
            [1.300717640235],
            [1.088834381295],
            [108.883438129491],
            [9.935937541852],
            [9.935937541852],
            [8.554478094730],
            [100.000000000000],
            [1.000000000000],
            [0.990000000000]])

        self.T = np.array([
            [338.942560146197, 102.469507659596],
            [102.469507659596, 198.039009400420]])

        self.M_t = np.array([
            [1.000000000000],
            [0.000000000000],
            [0.000000000000]])

        self.N_t = np.array([
            [1.000000000000]])