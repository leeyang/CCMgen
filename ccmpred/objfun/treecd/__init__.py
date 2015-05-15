import numpy as np

import ccmpred.raw
import ccmpred.counts
import ccmpred.objfun
import ccmpred.objfun.cd
import ccmpred.objfun.treecd.cext


class TreeContrastiveDivergence(ccmpred.objfun.cd.ContrastiveDivergence):

    def __init__(self, msa, tree, seq0, weights, lambda_single, lambda_pair, n_samples):
        super(TreeContrastiveDivergence).__init__(self, msa, weights, lambda_single, lambda_pair, len(tree.get_leaves()))

        self.tree = tree
        self.seq0 = 0

        tree_bfs = [c for c in bfs_iterator(tree.clade)]

        self.n_children = np.array([len(c.clades) for c in tree_bfs], dtype=int)
        self.branch_lengths = np.array([c.branch_length for c in tree_bfs], dtype=np.dtype('float64'))

    def init_sample_alignment(self):
        return np.zeros((self.n_samples, self.msa.shape[1]), dtype="uint8")

    @classmethod
    def init_from_raw(cls, msa, tree, seq0, weights, raw, lambda_single=1e4, lambda_pair=lambda msa: (msa.shape[1] - 1) * 0.2, n_samples=1000):
        res = cls(msa, tree, seq0, weights, lambda_single, lambda_pair, n_samples)

        if msa.shape[1] != raw.ncol:
            raise Exception('Mismatching number of columns: MSA {0}, raw {1}'.format(msa.shape[1], raw.ncol))

        x_single = raw.x_single
        x_pair = np.transpose(raw.x_pair, (0, 2, 1, 3))
        x = np.hstack((x_single.reshape((-1,)), x_pair.reshape((-1),)))

        res.centering_x_single[:] = x_single

        return x, res

    def sample_sequences(self, x):
        # TODO TODO
        return ccmpred.objfun.cd.cext.sample_sequences(self.msa_sampled, x)


def bfs_iterator(clade):
    """Breadth-first iterator along a tree clade"""

    def inner(clade):
        yield from clade.clades
        for c in clade.clades:
            yield from inner(c)

    yield clade
    yield from inner(clade)