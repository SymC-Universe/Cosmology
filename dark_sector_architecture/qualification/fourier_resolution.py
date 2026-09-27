"""Fourier-overlap utilities for paired-resolution qualification.

All FFT coefficients are normalized by the number of grid cells so equal
continuous periodic modes can be compared across grid sizes without the raw
NumPy FFT size factor.

These utilities measure realization/phase compatibility and common-grid field
differences. They do not impose scientific acceptance thresholds.
"""

from __future__ import annotations

import numpy as np


def signed_mode_numbers(n: int) -> np.ndarray:
    if n < 2:
        raise ValueError("grid size must be at least 2")
    return np.rint(np.fft.fftfreq(n) * n).astype(int)


def normalized_fft(field: np.ndarray) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 3 or len(set(arr.shape)) != 1:
        raise ValueError("field must be a cubic 3D scalar grid")
    if not np.all(np.isfinite(arr)):
        raise ValueError("field must be finite")
    return np.fft.fftn(arr) / arr.size


def _mode_index(n: int, mode: int) -> int:
    if mode >= 0:
        if mode >= n:
            raise ValueError("mode out of range")
        return mode
    index = n + mode
    if index < 0:
        raise ValueError("mode out of range")
    return index


def active_overlap_modes(low_n: int) -> list[tuple[int, int, int]]:
    """Return nonzero signed modes inside gevolution's low-grid k sphere.

    gevolution basic ICs use kmax = N/2 - 1 and zero modes with
    |k_index| >= kmax or spherical radius >= kmax when k-domain=sphere.
    """
    if low_n % 2 != 0 or low_n < 6:
        raise ValueError("qualification currently requires even low_n >= 6")
    kmax = (low_n // 2) - 1
    modes = signed_mode_numbers(low_n)
    selected: list[tuple[int, int, int]] = []
    for kx in modes:
        for ky in modes:
            for kz in modes:
                if kx == ky == kz == 0:
                    continue
                radius2 = int(kx * kx + ky * ky + kz * kz)
                if radius2 >= kmax * kmax:
                    continue
                if abs(kx) >= kmax or abs(ky) >= kmax or abs(kz) >= kmax:
                    continue
                selected.append((int(kx), int(ky), int(kz)))
    return selected


def coefficient_at(spectrum: np.ndarray, mode: tuple[int, int, int]) -> complex:
    n = spectrum.shape[0]
    if spectrum.shape != (n, n, n):
        raise ValueError("spectrum must be cubic")
    idx = tuple(_mode_index(n, m) for m in mode)
    return complex(spectrum[idx])


def phase_overlap_report(
    low_field: np.ndarray,
    high_field: np.ndarray,
) -> dict:
    low = np.asarray(low_field, dtype=float)
    high = np.asarray(high_field, dtype=float)
    if low.ndim != 3 or high.ndim != 3:
        raise ValueError("phase fields must be scalar 3D grids")
    if len(set(low.shape)) != 1 or len(set(high.shape)) != 1:
        raise ValueError("phase fields must be cubic")
    low_n = low.shape[0]
    high_n = high.shape[0]
    if high_n <= low_n or high_n % low_n != 0:
        raise ValueError("high grid must be an integer refinement of low grid")

    low_ft = normalized_fft(low)
    high_ft = normalized_fft(high)
    modes = active_overlap_modes(low_n)

    low_selected = np.array([coefficient_at(low_ft, mode) for mode in modes])
    high_selected = np.array([coefficient_at(high_ft, mode) for mode in modes])

    low_scale = float(np.max(np.abs(low_selected))) if low_selected.size else 0.0
    high_scale = float(np.max(np.abs(high_selected))) if high_selected.size else 0.0
    eps = np.finfo(float).eps
    numerical_floor = max(low_scale, high_scale, 1.0) * eps * 1024.0
    valid = (
        (np.abs(low_selected) > numerical_floor)
        & (np.abs(high_selected) > numerical_floor)
    )

    if not np.any(valid):
        raise ValueError("no numerically nonzero overlapping active modes")

    a = low_selected[valid]
    b = high_selected[valid]
    phase_delta = np.angle(b * np.conj(a))
    abs_phase = np.abs(phase_delta)
    amplitude_ratio = np.abs(b) / np.abs(a)

    cross = np.sum(b * np.conj(a))
    denom = np.sqrt(np.sum(np.abs(a) ** 2) * np.sum(np.abs(b) ** 2))
    weighted_coherence = float(np.abs(cross) / denom) if denom > 0 else None
    circular_phase_coherence = float(
        np.abs(np.mean(np.exp(1j * phase_delta)))
    )

    def q(values: np.ndarray) -> dict[str, float]:
        v = np.asarray(values, dtype=float)
        qs = np.quantile(v, [0.0, 0.05, 0.5, 0.95, 1.0])
        return {
            "min": float(qs[0]),
            "q05": float(qs[1]),
            "median": float(qs[2]),
            "q95": float(qs[3]),
            "max": float(qs[4]),
        }

    return {
        "low_grid": int(low_n),
        "high_grid": int(high_n),
        "selected_active_mode_count": int(len(modes)),
        "valid_nonzero_mode_count": int(np.count_nonzero(valid)),
        "excluded_numeric_zero_mode_count": int(np.count_nonzero(~valid)),
        "numeric_zero_floor": float(numerical_floor),
        "circular_phase_coherence": circular_phase_coherence,
        "weighted_complex_coherence": weighted_coherence,
        "absolute_phase_difference_radians": q(abs_phase),
        "absolute_phase_difference_degrees": q(np.degrees(abs_phase)),
        "amplitude_ratio_high_over_low": q(amplitude_ratio),
    }


def spectral_restrict_to_grid(field: np.ndarray, target_n: int) -> np.ndarray:
    """Restrict a periodic scalar field to shared non-Nyquist Fourier modes."""
    source = np.asarray(field, dtype=float)
    if source.ndim != 3 or len(set(source.shape)) != 1:
        raise ValueError("source must be a cubic 3D scalar grid")
    source_n = source.shape[0]
    if target_n >= source_n or source_n % target_n != 0:
        raise ValueError("target_n must be a smaller integer divisor")
    if target_n % 2 != 0:
        raise ValueError("target_n must be even")

    source_ft = normalized_fft(source)
    target_ft_normalized = np.zeros((target_n, target_n, target_n), dtype=complex)
    target_modes = signed_mode_numbers(target_n)

    # Exclude the target Nyquist plane because +N/2 and -N/2 alias there.
    nyquist = target_n // 2
    for kx in target_modes:
        if abs(int(kx)) == nyquist:
            continue
        for ky in target_modes:
            if abs(int(ky)) == nyquist:
                continue
            for kz in target_modes:
                if abs(int(kz)) == nyquist:
                    continue
                mode = (int(kx), int(ky), int(kz))
                target_ft_normalized[
                    _mode_index(target_n, mode[0]),
                    _mode_index(target_n, mode[1]),
                    _mode_index(target_n, mode[2]),
                ] = coefficient_at(source_ft, mode)

    restricted = np.fft.ifftn(target_ft_normalized * (target_n**3)).real
    return restricted


def spectral_restrict_vector_to_grid(
    velocity: np.ndarray, target_n: int
) -> np.ndarray:
    vel = np.asarray(velocity, dtype=float)
    if vel.ndim != 4 or vel.shape[0] != 3:
        raise ValueError("velocity must have shape (3,N,N,N)")
    return np.stack(
        [spectral_restrict_to_grid(vel[i], target_n) for i in range(3)],
        axis=0,
    )
