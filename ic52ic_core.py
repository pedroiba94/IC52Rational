# -*- coding: utf-8 -*-
"""
ic52ic_core.py — IC 5.2-IC Rational Method: pure calculation engine.
All formulas from Chapter 2 of Norma 5.2-IC (Drenaje Superficial).
No QGIS dependencies — fully unit-testable.
"""

import math
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


# ---------------------------------------------------------------------------
# TABLE 2.5 — Beta corrector coefficient (region → βm, Δ50, Δ67, Δ90, FT)
# FT keys: 2, 5, 10, 25, 100, 500
# Note: F10 = 1.00 for all regions (per norm).
# ---------------------------------------------------------------------------
TABLE_2_5 = {
    11:   dict(bm=0.90, d50=0.20, d67=0.30, d90=0.50, FT={2:0.80, 5:0.90, 10:1.00, 25:1.13, 100:1.34, 500:1.59}),
    12:   dict(bm=0.95, d50=0.20, d67=0.25, d90=0.45, FT={2:0.75, 5:0.90, 10:1.00, 25:1.14, 100:1.33, 500:1.56}),
    13:   dict(bm=0.60, d50=0.15, d67=0.25, d90=0.40, FT={2:0.74, 5:0.90, 10:1.00, 25:1.15, 100:1.34, 500:1.55}),
    21:   dict(bm=1.20, d50=0.20, d67=0.35, d90=0.55, FT={2:0.74, 5:0.88, 10:1.00, 25:1.18, 100:1.47, 500:1.90}),
    22:   dict(bm=1.50, d50=0.15, d67=0.20, d90=0.35, FT={2:0.74, 5:0.90, 10:1.00, 25:1.12, 100:1.27, 500:1.37}),
    23:   dict(bm=0.70, d50=0.20, d67=0.35, d90=0.55, FT={2:0.77, 5:0.89, 10:1.00, 25:1.15, 100:1.44, 500:1.82}),
    24:   dict(bm=1.10, d50=0.15, d67=0.20, d90=0.35, FT={2:0.76, 5:0.90, 10:1.00, 25:1.14, 100:1.36, 500:1.63}),
    25:   dict(bm=0.60, d50=0.15, d67=0.20, d90=0.35, FT={2:0.82, 5:0.92, 10:1.00, 25:1.12, 100:1.29, 500:1.48}),
    31:   dict(bm=0.90, d50=0.20, d67=0.30, d90=0.50, FT={2:0.87, 5:0.93, 10:1.00, 25:1.10, 100:1.26, 500:1.45}),
    32:   dict(bm=1.00, d50=0.20, d67=0.30, d90=0.50, FT={2:0.82, 5:0.91, 10:1.00, 25:1.12, 100:1.31, 500:1.54}),
    33:   dict(bm=2.15, d50=0.25, d67=0.40, d90=0.65, FT={2:0.70, 5:0.88, 10:1.00, 25:1.15, 100:1.38, 500:1.62}),
    41:   dict(bm=1.20, d50=0.20, d67=0.25, d90=0.45, FT={2:0.91, 5:0.96, 10:1.00, 25:1.00, 100:1.00, 500:1.00}),
    42:   dict(bm=2.25, d50=0.20, d67=0.35, d90=0.55, FT={2:0.67, 5:0.86, 10:1.00, 25:1.18, 100:1.46, 500:1.78}),
    511:  dict(bm=2.15, d50=0.10, d67=0.15, d90=0.20, FT={2:0.81, 5:0.91, 10:1.00, 25:1.12, 100:1.30, 500:1.50}),
    512:  dict(bm=0.70, d50=0.20, d67=0.30, d90=0.50, FT={2:1.00, 5:1.00, 10:1.00, 25:1.00, 100:1.00, 500:1.00}),
    52:   dict(bm=0.95, d50=0.20, d67=0.25, d90=0.45, FT={2:0.89, 5:0.94, 10:1.00, 25:1.09, 100:1.22, 500:1.36}),
    53:   dict(bm=2.10, d50=0.25, d67=0.35, d90=0.60, FT={2:0.68, 5:0.87, 10:1.00, 25:1.16, 100:1.38, 500:1.56}),
    61:   dict(bm=2.00, d50=0.25, d67=0.35, d90=0.60, FT={2:0.77, 5:0.91, 10:1.00, 25:1.10, 100:1.18, 500:1.17}),
    71:   dict(bm=1.20, d50=0.15, d67=0.20, d90=0.35, FT={2:0.82, 5:0.94, 10:1.00, 25:1.00, 100:1.00, 500:1.00}),
    72:   dict(bm=2.10, d50=0.30, d67=0.45, d90=0.70, FT={2:0.67, 5:0.86, 10:1.00, 25:1.00, 100:None, 500:None}),
    81:   dict(bm=1.30, d50=0.25, d67=0.35, d90=0.60, FT={2:0.76, 5:0.90, 10:1.00, 25:1.14, 100:1.34, 500:1.58}),
    821:  dict(bm=1.30, d50=0.35, d67=0.50, d90=0.85, FT={2:0.82, 5:0.91, 10:1.00, 25:1.07, 100:None, 500:None}),
    822:  dict(bm=2.40, d50=0.25, d67=0.35, d90=0.60, FT={2:0.70, 5:0.86, 10:1.00, 25:1.16, 100:None, 500:None}),
    83:   dict(bm=2.30, d50=0.15, d67=0.25, d90=0.40, FT={2:0.63, 5:0.85, 10:1.00, 25:1.21, 100:1.51, 500:1.85}),
    91:   dict(bm=0.85, d50=0.15, d67=0.25, d90=0.40, FT={2:0.72, 5:0.88, 10:1.00, 25:1.19, 100:1.52, 500:1.95}),
    92:   dict(bm=1.45, d50=0.30, d67=0.40, d90=0.70, FT={2:0.82, 5:0.94, 10:1.00, 25:1.00, 100:1.00, 500:1.00}),
    93:   dict(bm=1.70, d50=0.20, d67=0.25, d90=0.45, FT={2:0.77, 5:0.92, 10:1.00, 25:1.00, 100:1.00, 500:1.00}),
    941:  dict(bm=1.80, d50=0.15, d67=0.20, d90=0.35, FT={2:0.68, 5:0.87, 10:1.00, 25:1.17, 100:1.39, 500:1.64}),
    942:  dict(bm=1.20, d50=0.15, d67=0.25, d90=0.40, FT={2:0.77, 5:0.91, 10:1.00, 25:1.11, 100:1.24, 500:1.32}),
    951:  dict(bm=1.70, d50=0.30, d67=0.40, d90=0.70, FT={2:0.72, 5:0.88, 10:1.00, 25:1.17, 100:1.43, 500:1.78}),
    952:  dict(bm=0.85, d50=0.15, d67=0.25, d90=0.40, FT={2:0.77, 5:0.90, 10:1.00, 25:1.13, 100:1.32, 500:1.54}),
    101:  dict(bm=1.75, d50=0.30, d67=0.40, d90=0.70, FT={2:0.76, 5:0.90, 10:1.00, 25:1.12, 100:1.27, 500:1.39}),
    1021: dict(bm=1.45, d50=0.15, d67=0.25, d90=0.40, FT={2:0.79, 5:0.93, 10:1.00, 25:1.00, 100:1.00, 500:1.00}),
    1022: dict(bm=2.05, d50=0.15, d67=0.25, d90=0.40, FT={2:0.79, 5:0.93, 10:1.00, 25:1.00, 100:1.00, 500:1.00}),
}

# Levante/SE regions (Table 2.6) — T>25 years only
TABLE_2_6 = {
    72:  {50: (3.0, 1.08), 100: (4.0, 1.18), 200: (7.6, 1.13), 500: (13.3, 1.08)},
    821: {50: (3.0, 1.07), 100: (4.0, 1.10), 200: (6.5, 1.10), 500: (10.4, 1.07)},
    822: {50: (3.0, 1.07), 100: (4.0, 1.10), 200: (6.5, 1.10), 500: (10.4, 1.07)},
}

LEVANTE_REGIONS = {72, 821, 822}

# Standard return periods supported (MCO = 2.5 years, interpolated)
PERIODOS_STANDARD = [2, "MCO", 5, 10, 25, 50, 100, 500]
T_MCO = 2.5  # effective T for MCO interpolation

# Table 2.1 — diffuse flow coefficient ndif
NDIF = {
    "paved":         0.015,
    "bare_soil":     0.050,
    "sparse_veg":    0.120,
    "medium_veg":    0.320,
    "dense_veg":     1.000,
}

# Work type codes
OBRA_PM = "PM"  # plataforma/márgenes / vías auxiliares
OBRA_DT = "DT"  # drenaje transversal principal


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CuencaInput:
    """Geometría de la cuenca — introducida manualmente."""
    nombre: str = ""
    area_km2: float = 0.0          # A (km²)
    longitud_cauce_km: float = 0.0  # Lc (km)
    pendiente_cauce: float = 0.0   # Jc (m/m, adim)
    tipo_cuenca: str = "principal"  # "principal" | "secundaria"
    # Solo para cuenca secundaria (flujo difuso):
    ldif_m: float = 0.0
    ndif_tipo: str = "bare_soil"
    jdif: float = 0.0


@dataclass
class PrecipInput:
    """Datos de precipitación por período de retorno."""
    Pd: dict = field(default_factory=dict)   # {10: mm, 100: mm, 500: mm}
    I1_Id: float = 9.0                        # índice de torrencialidad
    region_beta: int = 32                     # código región Fig. 2.9
    tipo_obra: str = OBRA_DT                  # PM o DT
    # IDF opcional para Fb
    usar_IDF: bool = False
    IIDF_tc: Optional[float] = None          # I_IDF(T, tc) mm/h
    IIDF_24: Optional[float] = None          # I_IDF(T, 24) mm/h
    kb: float = 1.13


@dataclass
class SueloInput:
    """
    Datos de suelo/escorrentía.
    - clc_rows no vacío → cuenca heterogénea §2.2.4: QT = Kt/3.6 · I · Σ[Ci·Ai]
    - clc_rows vacío    → cuenca homogénea con P0i único
    clc_rows items: {"code": str, "area_km2": float, "P0i": float}
    """
    P0i: Optional[float] = None   # umbral único (cuenca homogénea)
    grupo_hid: str = "B"          # A, B, C, D
    clc_rows: list = field(default_factory=list)


@dataclass
class ResultadoT:
    """Resultado completo para un período de retorno T."""
    T: int
    KA: float
    tc_h: float
    Id_mmh: float
    Fa: float
    Fb: Optional[float]
    Fint: float
    I_mmh: float
    beta_m: float
    FT: float
    beta: float
    P0i: float
    P0: float
    C: float
    Kt: float
    QT_m3s: float
    # heterogeneous catchment
    heterogeneo: bool = False
    suma_CiAi: float = 0.0
    # flags
    levante_method: bool = False
    warnings: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Core formulas
# ---------------------------------------------------------------------------

def calc_KA(area_km2: float) -> float:
    """Factor reductor precipitación por área (§2.2.2.3)."""
    if area_km2 < 1.0:
        return 1.0
    return 1.0 - math.log10(area_km2) / 15.0


def calc_tc_principal(Lc_km: float, Jc: float) -> float:
    """Tiempo concentración cuenca principal (h) — §2.2.2.5.
    Returns tc in hours. Raises ValueError if Jc <= 0."""
    if Jc <= 0:
        raise ValueError("La pendiente media del cauce Jc debe ser > 0.")
    if Lc_km <= 0:
        raise ValueError("La longitud del cauce Lc debe ser > 0.")
    return 0.3 * (Lc_km ** 0.76) * (Jc ** -0.19)


def calc_tdif_min(Ldif_m: float, ndif: float, Jdif: float) -> float:
    """Tiempo flujo difuso (minutos) — §2.2.2.5."""
    if Jdif <= 0:
        raise ValueError("La pendiente Jdif debe ser > 0.")
    return 2.0 * (Ldif_m ** 0.408) * (ndif ** 0.312) * (Jdif ** -0.209)


def apply_tc_table22(tdif_min: float) -> float:
    """Tabla 2.2 — tc en condiciones de flujo difuso (minutos)."""
    if tdif_min <= 5:
        return 5.0
    elif tdif_min <= 40:
        return tdif_min
    else:
        return 40.0


def calc_Id(Pd_mm: float, KA: float) -> float:
    """Intensidad media diaria corregida (mm/h) — §2.2.2.2."""
    return Pd_mm * KA / 24.0


def calc_Fa(I1_Id: float, tc_h: float) -> float:
    """Factor Fa a partir del índice de torrencialidad — §2.2.2.4."""
    exp = 3.5287 - 2.5287 * (tc_h ** 0.1)
    return I1_Id ** exp


def calc_Fb(IIDF_tc: float, IIDF_24: float, kb: float = 1.13) -> float:
    """Factor Fb a partir de curvas IDF — §2.2.2.4."""
    if IIDF_24 <= 0:
        raise ValueError("IIDF_24 debe ser > 0.")
    return kb * IIDF_tc / IIDF_24


def calc_C(Pd_mm: float, KA: float, P0_mm: float) -> float:
    """Coeficiente de escorrentía C — §2.2.3.1."""
    ratio = Pd_mm * KA / P0_mm if P0_mm > 0 else 0.0
    if ratio <= 1.0:
        return 0.0
    return ((ratio - 1) * (ratio + 23)) / ((ratio + 11) ** 2)


def calc_Kt(tc_h: float) -> float:
    """Coeficiente de uniformidad temporal — §2.2.5."""
    tc125 = tc_h ** 1.25
    return 1.0 + tc125 / (tc125 + 14.0)


def calc_QT(I_mmh: float, C: float, A_km2: float, Kt: float) -> float:
    """Caudal punta QT (m³/s) — §2.2.1."""
    return (I_mmh * C * A_km2 * Kt) / 3.6


def get_beta_data(region: int) -> dict:
    """Retrieve Table 2.5 data for a region. Raises KeyError if not found."""
    if region not in TABLE_2_5:
        raise KeyError(f"Región {region} no encontrada en la Tabla 2.5.")
    return TABLE_2_5[region]


def interpolate_FT(FT_dict: dict, T_real: float) -> float:
    """
    Log-linear interpolation of FT for non-tabulated return periods.
    Uses the two bracketing tabulated T values.
    T_real: effective return period (e.g. 2.5 for MCO, 50 for T=50).
    Tabulated keys available: 2, 5, 10, 25, 100, 500.
    """
    tabulated = sorted(k for k, v in FT_dict.items() if v is not None)
    if T_real in tabulated:
        return FT_dict[T_real]
    # Find bracketing values
    lower = [t for t in tabulated if t <= T_real]
    upper = [t for t in tabulated if t >= T_real]
    if not lower or not upper:
        raise ValueError(f"T={T_real} fuera del rango de la Tabla 2.5.")
    T1, T2 = max(lower), min(upper)
    if T1 == T2:
        return FT_dict[T1]
    # Log-linear interpolation in T
    import math as _math
    w = _math.log(T_real / T1) / _math.log(T2 / T1)
    return FT_dict[T1] + w * (FT_dict[T2] - FT_dict[T1])


def calc_beta(region: int, T_key, tipo_obra: str) -> tuple[float, float]:
    """
    Compute β for a given region, T and obra type.
    T_key: integer T in years, or "MCO" (→ 2.5 years, interpolated).
    Returns (beta_value, FT_value).
    tipo_obra: OBRA_PM or OBRA_DT.
    """
    data = get_beta_data(region)
    bm = data["bm"]
    d50 = data["d50"]

    # Resolve effective T
    if T_key == "MCO":
        T_real = T_MCO
    else:
        T_real = float(T_key)

    # T=50 and MCO need interpolation; T=10 always = 1.00 per norm
    direct = data["FT"].get(int(T_real)) if T_real == int(T_real) else None
    if direct is not None and direct is not None:
        FT = direct
    else:
        FT = interpolate_FT(data["FT"], T_real)

    if FT is None:
        raise ValueError(
            f"FT no disponible para región {region} y T={T_key} "
            f"(zona Levante/SE — usar método §2.3)."
        )

    if tipo_obra == OBRA_PM:
        beta = bm * FT
    else:  # DT
        beta = (bm - d50) * FT
    return beta, FT


def calc_QT_levante(Q10_m3s: float, region: int, T: int) -> float:
    """
    Levante/SE method for T > 25 years — §2.3.
    QT = φ · Q10^λ
    """
    if region not in TABLE_2_6:
        raise ValueError(f"Región {region} no está en zonas Levante/SE.")
    params = TABLE_2_6[region]
    if T not in params:
        raise ValueError(f"T={T} no disponible en Tabla 2.6 para región {region}.")
    phi, lam = params[T]
    return phi * (Q10_m3s ** lam)


# ---------------------------------------------------------------------------
# Main calculation orchestrator
# ---------------------------------------------------------------------------

def calcular_metodo_racional(
    cuenca: CuencaInput,
    precip: PrecipInput,
    suelo: SueloInput,
    periodos: List = None,   # list of int or "MCO"; default = all 8 standard
) -> List:
    """
    Run the full IC 5.2-IC rational method for all requested return periods.
    periodos: list of T values — integers or "MCO". Default: [2,"MCO",5,10,25,50,100,500].
    Returns a list of ResultadoT, one per T in the same order.
    """
    if periodos is None:
        periodos = PERIODOS_STANDARD

    resultados = []

    # --- Geometry ---
    A = cuenca.area_km2
    KA = calc_KA(A)

    # --- Time of concentration ---
    warnings_tc = []
    if cuenca.tipo_cuenca == "principal":
        tc_h = calc_tc_principal(cuenca.longitud_cauce_km, cuenca.pendiente_cauce)
        if tc_h <= 0.25:
            warnings_tc.append(
                f"tc = {tc_h:.3f} h ≤ 0.25 h: aplicar método de cuenca secundaria (§2.2.2.5)."
            )
    else:
        ndif = NDIF.get(cuenca.ndif_tipo, 0.05)
        tdif_min = calc_tdif_min(cuenca.ldif_m, ndif, cuenca.jdif)
        tc_min = apply_tc_table22(tdif_min)
        tc_h = tc_min / 60.0

    Kt = calc_Kt(tc_h)

    # --- Beta region data (once, same region for all T) ---
    beta_data = get_beta_data(precip.region_beta)
    bm = beta_data["bm"]
    is_levante = precip.region_beta in LEVANTE_REGIONS

    # --- Loop over return periods ---
    Q10_cache: Optional[float] = None

    for T_key in periodos:
        warns = list(warnings_tc)

        # Resolve numeric T for Pd lookup and Levante check
        T_real = T_MCO if T_key == "MCO" else float(T_key)
        T_label = T_key  # "MCO" or int

        Pd = precip.Pd.get(T_key)
        if Pd is None:
            raise ValueError(f"No se proporcionó Pd para T={T_key}.")

        # Intensity chain
        Id = calc_Id(Pd, KA)
        Fa = calc_Fa(precip.I1_Id, tc_h)
        Fb = None
        if precip.usar_IDF and precip.IIDF_tc and precip.IIDF_24:
            Fb = calc_Fb(precip.IIDF_tc, precip.IIDF_24, precip.kb)
        Fint = max(Fa, Fb) if Fb is not None else Fa
        I = Id * Fint

        # Beta & P0
        use_levante = is_levante and T_real > 25
        try:
            beta, FT = calc_beta(precip.region_beta, T_key, precip.tipo_obra)
        except ValueError as e:
            if use_levante:
                beta, FT = calc_beta(precip.region_beta, 10, precip.tipo_obra)
                warns.append(str(e))
            else:
                raise

        # ── Heterogeneous §2.2.4 vs homogeneous ──────────────────────────────
        heterogeneo = bool(suelo.clc_rows)
        suma_CiAi = 0.0
        total_Ai  = 0.0

        if heterogeneo:
            for row in suelo.clc_rows:
                P0_row = row["P0i"] * beta
                C_row  = calc_C(Pd, KA, P0_row) if P0_row > 0 else 0.0
                suma_CiAi += C_row * row["area_km2"]
                total_Ai  += row["area_km2"]
            P0i_eff = (sum(r["P0i"] * r["area_km2"] for r in suelo.clc_rows)
                       / total_Ai) if total_Ai > 0 else 0.0
            P0_eff  = P0i_eff * beta
            C_eff   = suma_CiAi / total_Ai if total_Ai > 0 else 0.0
        else:
            P0_eff  = (suelo.P0i or 0.0) * beta
            C_eff   = calc_C(Pd, KA, P0_eff) if P0_eff > 0 else 0.0
            suma_CiAi = C_eff * A
            P0i_eff = suelo.P0i or 0.0
            total_Ai  = A

        # ── QT ────────────────────────────────────────────────────────────
        if use_levante:
            if Q10_cache is None:
                Pd10 = precip.Pd.get(10)
                if Pd10 is None:
                    raise ValueError("Se necesita Pd para T=10 para QT Levante.")
                Id10 = calc_Id(Pd10, KA)
                I10  = Id10 * calc_Fa(precip.I1_Id, tc_h)
                beta10, _ = calc_beta(precip.region_beta, 10, precip.tipo_obra)
                if heterogeneo:
                    s10 = sum(
                        calc_C(Pd10, KA, r["P0i"] * beta10) * r["area_km2"]
                        for r in suelo.clc_rows
                    )
                    Q10_cache = Kt * I10 * s10 / 3.6
                else:
                    P010 = (suelo.P0i or 0.0) * beta10
                    Q10_cache = calc_QT(I10, calc_C(Pd10, KA, P010), A, Kt)

            T_lev = int(T_real) if T_real == int(T_real) else 50
            QT_lev = calc_QT_levante(Q10_cache, precip.region_beta, T_lev)
            beta_ft1, _ = calc_beta(precip.region_beta, 10, precip.tipo_obra)
            if heterogeneo:
                s_ft1 = sum(
                    calc_C(Pd, KA, r["P0i"] * beta_ft1) * r["area_km2"]
                    for r in suelo.clc_rows
                )
                QT_rat = Kt * I * s_ft1 / 3.6
            else:
                P0_ft1 = (suelo.P0i or 0.0) * beta_ft1
                QT_rat = calc_QT(I, calc_C(Pd, KA, P0_ft1), A, Kt)
            QT = max(QT_lev, QT_rat)
            warns.append(f"T={T_key}: método Levante/SE §2.3 aplicado.")
            levante_flag = True
        else:
            if heterogeneo:
                QT = Kt * I * suma_CiAi / 3.6   # §2.2.4
            else:
                QT = calc_QT(I, C_eff, A, Kt)
            levante_flag = False

        # Cache Q10
        if T_key == 10 and Q10_cache is None:
            Q10_cache = QT

        resultados.append(ResultadoT(
            T=T_key, KA=KA, tc_h=tc_h, Id_mmh=Id, Fa=Fa, Fb=Fb,
            Fint=Fint, I_mmh=I, beta_m=bm, FT=FT, beta=beta,
            P0i=round(P0i_eff, 3), P0=round(P0_eff, 3), C=round(C_eff, 5),
            Kt=Kt, QT_m3s=QT,
            heterogeneo=heterogeneo, suma_CiAi=round(suma_CiAi, 6),
            levante_method=levante_flag, warnings=warns,
        ))

    return resultados
