# coding: utf-8
import numpy as np


class L2(object):
    """L2 regularization on single and pair emission potentials"""

    def __init__(self, lambda_single, lambda_pair_factor, scaling, center_x_single):
        self.lambda_single = lambda_single
        self.lambda_pair = lambda_pair_factor * scaling
        self.lambda_pair_factor = lambda_pair_factor
        self.center_x_single = center_x_single


    def __call__(self, x_single, x_pair):
        x_ofs = x_single - self.center_x_single[:, :x_single.shape[1]]

        # log likelihood uses:
        #   - lambda_single    * sum_i sum_a (v_ia - center_x_single)^2
        #   - lambda_pair / 2  * sum_i sum_j sum_a sum_b (w_ijab)^2
        #   w_ijab == w_jiba --> potentials are symmetric

        # gradient computes as:
        #   - 2 * lambda_single * (v_ia - center_x_single)
        #   - lambda_pair * w_ijab

        g_single = 2 * self.lambda_single * x_ofs
        g_pair = self.lambda_pair * x_pair

        fx_reg = self.lambda_single * np.sum(x_ofs * x_ofs) + 0.5 * self.lambda_pair * np.sum(x_pair * x_pair)

        return fx_reg, g_single, g_pair

    def __repr__(self):
        return "L₂ regularization (λsingle={0} λpairfactor={1} λpair={2})".format(self.lambda_single, self.lambda_pair_factor, self.lambda_pair)

class L3(object):
    """L3 regularization on single and pair emission potentials
       added by yang Li
    """
    
    def __init__(self, lambda_single, lambda_pair_factor, scaling, center_x_single,pair_mat):
        self.lambda_single = lambda_single
        self.lambda_pair = lambda_pair_factor * scaling
        self.lambda_pair_factor = lambda_pair_factor
        self.center_x_single = center_x_single
        self.pair_mat=pair_mat

    def __call__(self, x_single, x_pair):
        x_ofs = x_single - self.center_x_single[:, :x_single.shape[1]]

        # log likelihood uses:
        #   - lambda_single    * sum_i sum_a (v_ia - center_x_single)^2
        #   - lambda_pair / 2  * sum_i sum_j sum_a sum_b (w_ijab)^2
        #   w_ijab == w_jiba --> potentials are symmetric

        # gradient computes as:
        #   - 2 * lambda_single * (v_ia - center_x_single)
        #   - lambda_pair * w_ijab

        g_single = 2 * self.lambda_single * x_ofs
        g_pair = self.pair_mat * x_pair

        fx_reg = self.lambda_single * np.sum(x_ofs * x_ofs) + 0.5 * np.sum(x_pair * x_pair * self.pair_mat)

        return fx_reg, g_single, g_pair

    def __repr__(self):
        return "L₂ regularization (λsingle={0} λpairfactor={1} λpair={2})".format(self.lambda_single, self.lambda_pair_factor, self.lambda_pair)