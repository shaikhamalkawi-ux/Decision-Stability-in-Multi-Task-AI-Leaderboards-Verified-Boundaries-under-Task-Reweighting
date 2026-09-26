from __future__ import annotations

import math
import unittest

import numpy as np
from scipy.optimize import linprog

from independent_verify import pairwise_transport


def pairwise_lp(z: np.ndarray, inside: int, outside: int, w0: np.ndarray) -> float:
    d = len(w0)
    objective = np.concatenate([np.zeros(d), np.full(d, 0.5)])
    rows = []
    rhs = []
    for task in range(d):
        row = np.zeros(2 * d)
        row[task] = 1.0
        row[d + task] = -1.0
        rows.append(row)
        rhs.append(w0[task])
        row = np.zeros(2 * d)
        row[task] = -1.0
        row[d + task] = -1.0
        rows.append(row)
        rhs.append(-w0[task])
    row = np.zeros(2 * d)
    row[:d] = z[:, outside] - z[:, inside]
    rows.append(row)
    rhs.append(0.0)
    equality = np.zeros((1, 2 * d))
    equality[0, :d] = 1.0
    result = linprog(
        objective,
        A_ub=np.vstack(rows),
        b_ub=np.asarray(rhs),
        A_eq=equality,
        b_eq=np.array([1.0]),
        bounds=[(0.0, None)] * (2 * d),
        method="highs",
    )
    return float(result.fun) if result.success else float("inf")


class OrderedTransferTests(unittest.TestCase):
    def test_matches_lp_on_random_problems(self) -> None:
        rng = np.random.default_rng(20260920)
        for d in (3, 7, 15):
            for _ in range(40):
                z = rng.normal(size=(d, 2))
                w0 = rng.dirichlet(np.ones(d))
                observed = pairwise_transport(z, 0, 1, w0).radius
                expected = pairwise_lp(z, 0, 1, w0)
                if math.isinf(expected):
                    self.assertTrue(math.isinf(observed))
                else:
                    self.assertAlmostEqual(observed, expected, places=9)

    def test_zero_radius_for_nominal_tie(self) -> None:
        z = np.array([[0.0, 1.0], [1.0, 0.0]])
        w0 = np.array([0.5, 0.5])
        self.assertEqual(pairwise_transport(z, 0, 1, w0).radius, 0.0)

    def test_infinite_when_inside_strictly_dominates(self) -> None:
        z = np.array([[0.0, 1.0], [0.0, 2.0]])
        w0 = np.array([0.5, 0.5])
        self.assertTrue(math.isinf(pairwise_transport(z, 0, 1, w0).radius))


if __name__ == "__main__":
    unittest.main()
