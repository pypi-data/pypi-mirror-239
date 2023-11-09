"""Utility programs used in `min_distance.py`.
"""
from dataclasses import dataclass
from typing import cast

import numpy as np
import scipy.linalg as spla
from bs_python_utils.bsnputils import npmaxabs
from bs_python_utils.bsutils import print_stars


def compute_estimates(
    M: np.ndarray, S_mat: np.ndarray, d: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Returns the QGLS estimates and their variance-covariance.

    Args:
        M: an (XY,p) matrix
        S_mat: an (XY, XY) weighting matrix
        d: an XY-vector

    Returns:
        the p-vector of estimates and their estimated (p,p) variance
    """
    M_T = M.T
    M_S_d = M_T @ S_mat @ d
    M_S_M = M_T @ S_mat @ M
    est_coeffs = -spla.solve(M_S_M, M_S_d)
    varcov_coeffs = spla.inv(M_S_M)
    return est_coeffs, varcov_coeffs


@dataclass
class MDEResults:
    """
    The results from minimum-distance estimation and testing.

    Args:
        X: the number of types of men
        Y: the number of types of women
        K: the number of bases
        number_households: the number of households in the sample
        estimated_coefficients: the estimated coefficients
        varcov_coefficients: their eetimated var-covar
        stderrs_coefficients: their estimated stderrs
        estimated_Phi: the estimated joint surplus
        test_statistic: the value of the misspecification statistic
        test_pvalue: the p-value of the test
        ndf: the number of degrees of freedom
        parameterized_entropy: True if the derivative of the entropy has unknown parameters
    """

    X: int
    Y: int
    K: int
    number_households: int
    estimated_coefficients: np.ndarray
    varcov_coefficients: np.ndarray
    stderrs_coefficients: np.ndarray
    estimated_Phi: np.ndarray
    test_statistic: float
    test_pvalue: float
    ndf: int
    parameterized_entropy: bool | None = False

    def __str__(self):
        line_stars = "*" * 80 + "\n"
        if self.parameterized_entropy:
            n_alpha = self.estimated_coefficients.size - self.K
            entropy_str = f"     The entropy has {n_alpha} parameters."
        else:
            entropy_str = "     The entropy is parameter-free."
            n_alpha = 0
        model_str = f"The data has {self.number_households} households\n\n"
        model_str += f"The model has {self.X}x{self.Y} margins\n {entropy_str} \n"
        model_str += f"We use {self.K} basis functions.\n\n"
        repr_str = line_stars + model_str
        repr_str += "The estimated coefficients (and their standard errors) are\n\n"
        if self.parameterized_entropy:
            for i, coeff in enumerate(self.estimated_coefficients[:n_alpha]):
                repr_str += (
                    f"   alpha({i + 1}): {coeff: > 10.3f}  "
                    + f"({self.stderrs_coefficients[i]: .3f})\n"
                )
            repr_str += "\n"
        for i, coeff in enumerate(self.estimated_coefficients[n_alpha:]):
            repr_str += (
                f"   base {i + 1}: {coeff: > 10.3f} "
                + f"({self.stderrs_coefficients[n_alpha + i]: .3f})\n"
            )
        repr_str += "\nSpecification test:\n"
        repr_str += (
            f"   the value of the test statistic is {self.test_statistic: > 10.3f}\n"
        )
        repr_str += (
            f"     for a chi2({self.ndf}), the p-value is {self.test_pvalue: > 10.3f}\n"
        )
        return repr_str + line_stars

    def print_results(
        self, true_coeffs: np.ndarray | None = None, n_alpha: int = 0
    ) -> None | float:
        estimates = self.estimated_coefficients
        stderrs = self.stderrs_coefficients

        if true_coeffs is not None:
            repr_str = (
                "The true and estimated coefficients "
                + "(and their standard errors) are\n\n"
            )
            for i, coeff in enumerate(estimates[:n_alpha]):
                repr_str += f"   alpha({i + 1}): {true_coeffs[i]: > 10.3f}"
                repr_str += f"{coeff: > 10.3f}  ({stderrs[i]: > 10.3f})\n"
                repr_str += "\n"
            for i, coeff in enumerate(estimates[n_alpha:]):
                j = n_alpha + i
                repr_str += (
                    f"   base {i + 1}: {true_coeffs[j]: > 10.3f}  "
                    + f"{coeff: > 10.3f}  ({stderrs[j]: > 10.3f})\n"
                )
            print_stars(repr_str)
            discrepancy = npmaxabs(true_coeffs - estimates)
            print_stars(
                "The largest difference between true and estimated coefficients is"
                f" {discrepancy: .2e}"
            )
        else:
            repr_str = (
                "The estimated coefficients " + "(and their standard errors) are\n\n"
            )
            for i, coeff in enumerate(estimates[:n_alpha]):
                repr_str + f"{coeff: > 10.3f}  ({stderrs[i]: > 10.3f})\n"
                repr_str += "\n"
            for i, coeff in enumerate(estimates[n_alpha:]):
                j = n_alpha + i
                repr_str += f"{coeff: > 10.3f}  ({stderrs[j]: > 10.3f})\n"
            print_stars(repr_str)

        repr_str = "\nSpecification test:\n"
        repr_str += (
            "   the value of the test statistic is "
            + f"{self.test_statistic: > 10.3f}\n"
        )
        repr_str += (
            f"     for a chi2({self.ndf}), "
            + f"the p-value is {self.test_pvalue: > 10.3f}\n"
        )
        print_stars(repr_str)
        if true_coeffs is not None:
            return cast(float, discrepancy)
        return None
