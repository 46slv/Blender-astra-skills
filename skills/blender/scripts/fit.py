"""Small bounded finite-difference visual servo. NumPy only (ships in Blender).

The caller chooses meaningful parameters and residuals, e.g. projected landmarks.
Fit camera with fixed shape first, then shape with fixed camera. This is local
least squares, not reconstruction; unseen geometry is unconstrained.
"""
import numpy as np


def solve(initial, evaluate, steps, bounds=None, iterations=25, tolerance=0.5):
    """evaluate(x) applies x and returns finite residual vector (typically pixels).

Leaves the scene at the best accepted x, including on exceptions. Steps encode
parameter units (e.g. meters vs radians); bounds are (lower, upper). Reports
observable rank, which helps expose ambiguous/insufficient correspondences.
"""
    x = np.asarray(initial, dtype=float).copy()
    h = np.asarray(steps, dtype=float)
    if h.shape != x.shape or np.any(h <= 0):
        raise ValueError('Provide a positive finite-difference step per parameter')
    lo, hi = (np.full_like(x, -np.inf), np.full_like(x, np.inf)) if bounds is None else map(lambda a: np.asarray(a, dtype=float), bounds)
    if np.any(lo > hi) or np.any(x < lo) or np.any(x > hi):
        raise ValueError('Initial parameters must lie within valid bounds')

    def residual(p):
        r = np.asarray(evaluate(p.tolist()), dtype=float).reshape(-1)
        if not r.size or not np.all(np.isfinite(r)):
            raise ValueError('Residuals must be nonempty and finite; check camera/landmarks')
        return r

    history, rank, damping = [], 0, 1e-3
    try:
        r = residual(x)
        for _ in range(iterations):
            rms = float(np.sqrt(np.mean(r*r)))
            history.append(rms)
            if rms <= tolerance:
                break
            columns = []
            for j in range(len(x)):
                plus, minus = x.copy(), x.copy()
                plus[j], minus[j] = min(hi[j], x[j]+h[j]), max(lo[j], x[j]-h[j])
                span = plus[j] - minus[j]
                columns.append((residual(plus)-residual(minus)) * h[j] / span if span else np.zeros_like(r))
            jac = np.column_stack(columns)
            rank = int(np.linalg.matrix_rank(jac))
            delta = np.linalg.lstsq(jac.T@jac + damping*np.eye(len(x)), -jac.T@r, rcond=None)[0]
            # Cap each proposal to avoid a huge jump across visibility/projection changes.
            delta /= max(1, float(np.max(np.abs(delta))) / 20)
            candidate = np.clip(x + delta*h, lo, hi)
            candidate_r = residual(candidate)
            if np.dot(candidate_r, candidate_r) < np.dot(r, r):
                x, r = candidate, candidate_r
                damping = max(1e-9, damping/3)
            else:
                damping *= 10
                if damping > 1e9:
                    break
        final = residual(x)
        rms = float(np.sqrt(np.mean(final*final)))
        return {'parameters': x.tolist(), 'rms': rms, 'converged': rms <= tolerance,
                'rank': rank, 'parameter_count': len(x), 'history_rms': history}
    finally:
        evaluate(x.tolist())
