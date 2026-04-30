# -*- coding: utf-8 -*-
"""
ic52ic_p0table.py — Table 2.3 lookup: P0i (mm) by CLC code, slope and soil group.
Codes follow Corine Land Cover 2000 used in IC 5.2-IC.
slope_pct: slope in % (threshold is 3%).
grupo_hid: "A", "B", "C" or "D".
"""

from typing import Optional

# ---------------------------------------------------------------------------
# TABLE 2.3 structure:
# key: (clc_code_str, practica, pendiente_ge3)
#   practica: None | "R" | "N" | "RN"  (only for some agricultural codes)
#   pendiente_ge3: True if slope >= 3%, False if slope < 3%
# value: {A: int, B: int, C: int, D: int}
#
# For codes without slope distinction, both True/False entries are identical.
# ---------------------------------------------------------------------------

# Compact representation: list of tuples
# (code, practica, ge3, A, B, C, D)
# practica: "*" = any (no practice distinction)
_RAW = [
    # Urban / artificial
    ("11100", "*", True,  1,  1,  1,  1),
    ("11100", "*", False, 1,  1,  1,  1),
    ("11200", "*", True,  24, 14,  8,  6),
    ("11200", "*", False, 24, 14,  8,  6),
    ("11210", "*", True,  24, 14,  8,  6),
    ("11210", "*", False, 24, 14,  8,  6),
    ("11220", "*", True,  24, 14,  8,  6),
    ("11220", "*", False, 24, 14,  8,  6),
    ("12100", "*", True,   6,  4,  3,  3),
    ("12100", "*", False,  6,  4,  3,  3),
    ("12110", "*", True,  12,  7,  5,  4),
    ("12110", "*", False, 12,  7,  5,  4),
    ("12120", "*", True,   6,  4,  3,  3),
    ("12120", "*", False,  6,  4,  3,  3),
    ("12200", "*", True,   1,  1,  1,  1),
    ("12200", "*", False,  1,  1,  1,  1),
    ("12210", "*", True,   1,  1,  1,  1),
    ("12210", "*", False,  1,  1,  1,  1),
    ("12220", "*", True,  12,  7,  5,  4),
    ("12220", "*", False, 12,  7,  5,  4),
    ("12300", "*", True,   1,  1,  1,  1),
    ("12300", "*", False,  1,  1,  1,  1),
    ("12400", "*", True,  24, 14,  8,  6),
    ("12400", "*", False, 24, 14,  8,  6),
    ("13100", "*", True,  16,  9,  6,  5),
    ("13100", "*", False, 16,  9,  6,  5),
    ("13200", "*", True,  20, 11,  8,  6),
    ("13200", "*", False, 20, 11,  8,  6),
    ("13300", "*", True,  24, 14,  8,  6),
    ("13300", "*", False, 24, 14,  8,  6),
    ("14100", "*", True,  53, 23, 14, 10),
    ("14100", "*", False, 53, 23, 14, 10),
    ("14200", "*", True,  79, 32, 18, 13),
    ("14200", "*", False, 79, 32, 18, 13),
    ("14210", "*", True,  79, 32, 18, 13),
    ("14210", "*", False, 79, 32, 18, 13),
    ("14220", "*", True,  53, 23, 14, 10),
    ("14220", "*", False, 53, 23, 14, 10),
    # Agricultural — cereales
    ("21100", "R",  True,  29, 17, 10,  8),
    ("21100", "N",  True,  32, 19, 12, 10),
    ("21100", "RN", False, 34, 21, 14, 12),
    # viveros
    ("21100_V", "*", True,  62, 28, 15, 10),
    ("21100_V", "*", False, 75, 34, 19, 14),
    # hortalizas
    ("21100_H", "R",  True,  23, 13,  8,  6),
    ("21100_H", "N",  True,  25, 16, 11,  8),
    ("21100_H", "RN", False, 29, 19, 14, 11),
    # tierras abandonadas
    ("21100_A", "*", True,  16, 10,  7,  5),
    ("21100_A", "*", False, 20, 14, 11,  8),
    # Terrenos regados
    ("21200", "R",  True,  37, 20, 12,  9),
    ("21200", "N",  True,  42, 23, 14, 11),
    ("21200", "RN", False, 47, 25, 16, 13),
    ("21210", "R",  True,  37, 20, 12,  9),
    ("21210", "N",  True,  42, 23, 14, 11),
    ("21210", "RN", False, 47, 25, 16, 13),
    ("21220", "R",  True,  37, 20, 12,  9),
    ("21220", "N",  True,  42, 23, 14, 11),
    ("21220", "RN", False, 47, 25, 16, 13),
    ("21300", "*", True,  47, 25, 16, 13),
    ("21300", "*", False, 47, 25, 16, 13),
    # Viñedos
    ("22100", "*", True,  62, 28, 15, 10),
    ("22100", "*", False, 75, 34, 19, 14),
    ("22110", "*", True,  62, 28, 15, 10),
    ("22110", "*", False, 75, 34, 19, 14),
    ("22120", "*", True,  62, 28, 15, 10),
    ("22120", "*", False, 75, 34, 19, 14),
    # Frutales
    ("22200", "*", True,  80, 34, 19, 14),
    ("22200", "*", False, 95, 42, 22, 15),
    ("22210", "*", True,  62, 28, 15, 10),
    ("22210", "*", False, 75, 34, 19, 14),
    ("22220", "*", True,  80, 34, 19, 14),
    ("22220", "*", False, 95, 42, 22, 15),
    ("22221", "*", True,  80, 34, 19, 14),
    ("22221", "*", False, 95, 42, 22, 15),
    ("22222", "*", True,  80, 34, 19, 14),
    ("22222", "*", False, 95, 42, 22, 15),
    ("22223", "*", True,  80, 34, 19, 14),
    ("22223", "*", False, 95, 42, 22, 15),
    # Olivares
    ("22300", "*", True,  62, 28, 15, 10),
    ("22300", "*", False, 75, 34, 19, 14),
    ("22310", "*", True,  62, 28, 15, 10),
    ("22310", "*", False, 75, 34, 19, 14),
    ("22320", "*", True,  62, 28, 15, 10),
    ("22320", "*", False, 75, 34, 19, 14),
    # Prados y praderas
    ("23100", "*", True,  70, 33, 18, 13),
    ("23100", "*", False, 120, 55, 22, 14),
    # Sistemas agroforestales
    ("24110", "*", True,  39, 20, 12,  8),
    ("24110", "*", False, 66, 29, 15, 10),
    ("24120", "*", True,  75, 33, 18, 14),
    ("24120", "*", False, 106, 48, 22, 15),
    ("24211", "R",  True,  26, 15,  9,  6),
    ("24211", "N",  True,  28, 17, 11,  8),
    ("24211", "RN", False, 30, 19, 13, 10),
    ("24212", "*", True,  62, 28, 15, 10),
    ("24212", "*", False, 75, 34, 19, 14),
    ("24213", "*", True,  39, 20, 12,  8),
    ("24213", "*", False, 66, 29, 15, 10),
    ("24221", "R",  True,  37, 20, 12,  9),
    ("24221", "N",  True,  42, 23, 14, 11),
    ("24221", "RN", False, 47, 25, 16, 13),
    ("24222", "*", True,  80, 34, 19, 14),
    ("24222", "*", False, 95, 42, 22, 15),
    ("24223", "*", True,  75, 33, 18, 14),
    ("24223", "*", False, 106, 48, 22, 15),
    ("24230", "R",  True,  31, 17, 10,  8),
    ("24230", "N",  True,  34, 20, 13, 10),
    ("24230", "RN", False, 37, 22, 14, 11),
    ("24310", "R",  True,  26, 15,  9,  6),
    ("24310", "N",  True,  28, 17, 11,  8),
    ("24310", "RN", False, 30, 19, 13, 10),
    ("24320", "R",  True,  37, 20, 12,  9),
    ("24320", "N",  True,  42, 23, 14, 11),
    ("24320", "RN", False, 47, 25, 16, 13),
    ("24330", "*", True,  70, 33, 18, 13),
    ("24330", "*", False, 120, 55, 22, 14),
    ("24400", "*", True,  53, 23, 14,  9),
    ("24400", "*", False, 80, 35, 17, 10),
    ("24410", "*", True,  53, 23, 14,  9),
    ("24410", "*", False, 80, 35, 17, 10),
    ("24420", "*", True,  53, 23, 14,  9),
    ("24420", "*", False, 80, 35, 17, 10),
    # Forests
    ("31100", "*", True,  90, 47, 31, 23),
    ("31100", "*", False, 90, 47, 31, 23),
    ("31110", "*", True,  90, 47, 31, 23),
    ("31110", "*", False, 90, 47, 31, 23),
    ("31120", "*", True,  90, 47, 31, 23),
    ("31120", "*", False, 90, 47, 31, 23),
    ("31130", "*", True,  79, 34, 19, 14),
    ("31130", "*", False, 94, 42, 22, 15),
    ("31140", "*", True,  90, 47, 31, 23),
    ("31140", "*", False, 90, 47, 31, 23),
    ("31150", "*", True,  76, 34, 22, 16),
    ("31150", "*", False, 76, 34, 22, 16),
    ("31160", "*", True,  90, 47, 31, 23),
    ("31160", "*", False, 90, 47, 31, 23),
    ("31200", "*", True,  90, 47, 31, 23),
    ("31200", "*", False, 90, 47, 31, 23),
    ("31210", "*", True,  90, 47, 31, 23),
    ("31210", "*", False, 90, 47, 31, 23),
    ("31220", "*", True,  90, 47, 31, 23),
    ("31220", "*", False, 90, 47, 31, 23),
    ("31300", "*", True,  90, 47, 31, 23),
    ("31300", "*", False, 90, 47, 31, 23),
    # Shrubland / open areas
    ("32100", "*", True,  53, 23, 14,  9),
    ("32100", "*", False, 80, 35, 17, 10),
    ("32110", "*", True,  70, 33, 18, 13),
    ("32110", "*", False, 120, 55, 22, 14),
    ("32111", "*", True,  70, 33, 18, 13),
    ("32111", "*", False, 120, 55, 22, 14),
    ("32112", "*", True,  24, 14,  8,  6),
    ("32112", "*", False, 57, 25, 12,  7),
    ("32121", "*", True,  53, 23, 14,  9),
    ("32121", "*", False, 79, 35, 17, 10),
    ("32122", "*", True,  24, 14,  8,  6),
    ("32122", "*", False, 57, 25, 12,  7),
    ("32200", "*", True,  76, 34, 22, 16),
    ("32200", "*", False, 76, 34, 22, 16),
    ("32210", "*", True,  76, 34, 22, 16),
    ("32210", "*", False, 76, 34, 22, 16),
    ("32220", "*", True,  60, 24, 14, 10),
    ("32220", "*", False, 60, 24, 14, 10),
    ("32300", "*", True,  60, 24, 14, 10),
    ("32300", "*", False, 60, 24, 14, 10),
    ("32311", "*", True,  75, 34, 22, 16),
    ("32311", "*", False, 75, 34, 22, 16),
    ("32312", "*", True,  60, 24, 14, 10),
    ("32312", "*", False, 60, 24, 14, 10),
    ("32320", "*", True,  40, 17,  8,  5),
    ("32320", "*", False, 40, 17,  8,  5),
    ("32400", "*", True,  75, 34, 22, 16),
    ("32400", "*", False, 75, 34, 22, 16),
    ("32410", "*", True,  75, 34, 22, 16),
    ("32410", "*", False, 75, 34, 22, 16),
    ("32420", "*", True,  75, 34, 22, 16),
    ("32420", "*", False, 75, 34, 22, 16),
    ("32430", "*", True,  75, 34, 22, 16),
    ("32430", "*", False, 75, 34, 22, 16),
    # Open spaces
    ("33110", "*", True,  152, 152, 152, 152),
    ("33110", "*", False, 152, 152, 152, 152),
    ("33120", "*", True,  15,  8,  6,  4),
    ("33120", "*", False, 15,  8,  6,  4),
    ("33200", "*", True,   2,  2,  2,  2),
    ("33200", "*", False,  2,  2,  2,  2),
    ("33210", "*", True,   2,  2,  2,  2),
    ("33210", "*", False,  2,  2,  2,  2),
    ("33220", "*", True,   2,  2,  2,  2),
    ("33220", "*", False,  4,  4,  4,  4),
    ("33230", "*", True,   3,  3,  3,  3),
    ("33230", "*", False,  5,  5,  5,  5),
    ("33300", "*", True,  24, 14,  8,  6),
    ("33300", "*", False, 58, 25, 12,  7),
    ("33310", "*", True,  24, 14,  8,  6),
    ("33310", "*", False, 58, 25, 12,  7),
    ("33320", "*", True,  15,  8,  6,  4),
    ("33320", "*", False, 15,  8,  6,  4),
    ("33330", "*", True,  24, 14,  8,  6),
    ("33330", "*", False, 58, 25, 12,  7),
    ("33400", "*", True,  15,  8,  6,  4),
    ("33400", "*", False, 15,  8,  6,  4),
    ("33500", "*", True,   0,  0,  0,  0),
    ("33500", "*", False,  0,  0,  0,  0),
    # Wetlands
    ("41100", "*", True,   2,  2,  2,  2),
    ("41100", "*", False,  2,  2,  2,  2),
    ("41200", "*", True,  248, 99, 25, 16),
    ("41200", "*", False, 248, 99, 25, 16),
    ("42100", "*", True,   2,  2,  2,  2),
    ("42100", "*", False,  2,  2,  2,  2),
    ("42200", "*", True,   5,  5,  5,  5),
    ("42200", "*", False,  5,  5,  5,  5),
    ("42300", "*", True,   0,  0,  0,  0),
    ("42300", "*", False,  0,  0,  0,  0),
    # Water bodies
    ("51100", "*", True,   0,  0,  0,  0),
    ("51100", "*", False,  0,  0,  0,  0),
    ("51110", "*", True,   0,  0,  0,  0),
    ("51110", "*", False,  0,  0,  0,  0),
    ("51120", "*", True,   0,  0,  0,  0),
    ("51120", "*", False,  0,  0,  0,  0),
    ("51210", "*", True,   0,  0,  0,  0),
    ("51210", "*", False,  0,  0,  0,  0),
    ("51220", "*", True,   0,  0,  0,  0),
    ("51220", "*", False,  0,  0,  0,  0),
    ("52100", "*", True,   0,  0,  0,  0),
    ("52100", "*", False,  0,  0,  0,  0),
    ("52200", "*", True,   0,  0,  0,  0),
    ("52200", "*", False,  0,  0,  0,  0),
    ("52300", "*", True,   0,  0,  0,  0),
    ("52300", "*", False,  0,  0,  0,  0),
]

# Build lookup dict: (code, practica, ge3) → {A, B, C, D}
_LOOKUP: dict = {}
for row in _RAW:
    code, prac, ge3, A, B, C, D = row
    _LOOKUP[(code, prac, ge3)] = {"A": A, "B": B, "C": C, "D": D}


# ---------------------------------------------------------------------------
# 3-digit CLC prefix → preferred 5-digit code (Table 2.3 parent code)
# When a layer stores 3-digit codes (e.g. CLC2Manning), we resolve to the
# most representative 5-digit code. For ambiguous groups the parent xxxx0
# is preferred; if unavailable the most conservative (highest P0i) sub-code
# is used and flagged for user review.
# ---------------------------------------------------------------------------
_PREFIX3_TO_CODE5 = {
    "111": "11100",
    "112": "11200",   # parent; 11210/11220 are refinements
    "121": "12100",
    "122": "12200",
    "123": "12300",
    "124": "12400",
    "131": "13100",
    "132": "13200",
    "133": "13300",
    "141": "14100",
    "142": "14200",
    "211": "21100",   # cereales R/N ≥3% — conservative default
    "212": "21200",
    "213": "21300",
    "221": "22100",
    "222": "22200",
    "223": "22300",
    "231": "23100",
    "241": "24110",   # secano — conservative
    "242": "24211",   # mosaico secano — conservative
    "243": "24310",   # mosaico con veg. natural secano — conservative
    "244": "24400",
    "311": "31100",
    "312": "31200",
    "313": "31300",
    "321": "32100",
    "322": "32200",
    "323": "32300",
    "324": "32400",
    "331": "33110",
    "332": "33200",
    "333": "33300",
    "334": "33400",
    "335": "33500",
    "411": "41100",
    "412": "41200",
    "421": "42100",
    "422": "42200",
    "423": "42300",
    "511": "51100",
    "512": "51210",
    "521": "52100",
    "522": "52200",
    "523": "52300",
}


def _resolve_code(clc_code: str) -> tuple[str, bool]:
    """
    Resolve a raw CLC code (3, 4 or 5 digits) to a canonical 5-digit code.
    Returns (resolved_code, was_approximated).
    """
    c = clc_code.strip()
    # Already 5 digits — use directly (strip internal suffixes like _V, _H, _A)
    if len(c) == 5 and c.isdigit():
        return c, False
    # 4 digits — pad with trailing zero
    if len(c) == 4 and c.isdigit():
        return c + "0", True
    # 3 digits — use prefix map
    if len(c) == 3 and c.isdigit():
        resolved = _PREFIX3_TO_CODE5.get(c, c + "00")
        approximated = resolved != c + "00"
        return resolved, approximated
    return c, False


def get_P0i_CLC(
    clc_code: str,
    slope_pct: float,
    grupo_hid: str,
    practica: str = "*",
) -> Optional[float]:
    """
    Return P0i (mm) for a given CLC code, slope (%), hydrological group and
    agricultural practice.

    Accepts 3-digit codes (e.g. "211"), 4-digit ("2110") or full 5-digit ("21100").
    3-digit codes are resolved via _PREFIX3_TO_CODE5 (most conservative choice).
    practica: "*" (default), "R", "N", "RN"
    Returns None only if truly unresolvable.
    """
    ge3 = slope_pct >= 3.0
    grupo_hid = grupo_hid.upper()
    code, _ = _resolve_code(clc_code)

    # 1. Direct lookup with requested practice
    key = (code, practica, ge3)
    if key in _LOOKUP:
        return float(_LOOKUP[key][grupo_hid])

    # 2. Wildcard practice
    key_any = (code, "*", ge3)
    if key_any in _LOOKUP:
        return float(_LOOKUP[key_any][grupo_hid])

    # 3. Opposite slope (edge case: slope exactly at threshold)
    key_alt = (code, practica, not ge3)
    if key_alt in _LOOKUP:
        return float(_LOOKUP[key_alt][grupo_hid])
    key_alt2 = (code, "*", not ge3)
    if key_alt2 in _LOOKUP:
        return float(_LOOKUP[key_alt2][grupo_hid])

    # 4. Try parent code (first 4 digits + "0")
    parent = code[:4] + "0" if len(code) == 5 else None
    if parent and parent != code:
        for prac in (practica, "*"):
            for ge in (ge3, not ge3):
                k = (parent, prac, ge)
                if k in _LOOKUP:
                    return float(_LOOKUP[k][grupo_hid])

    # 5. Any practice for same code (R/N/RN when no wildcard exists)
    for prac_try in ("R", "N", "RN", "R/N"):
        for ge in (ge3, not ge3):
            k = (code, prac_try, ge)
            if k in _LOOKUP:
                return float(_LOOKUP[k][grupo_hid])

    # 6. Prefix scan — find any code starting with same 3 digits, take max P0i
    prefix3 = code[:3]
    candidates = [
        _LOOKUP[k][grupo_hid]
        for k in _LOOKUP
        if k[0].startswith(prefix3) and k[2] == ge3
    ]
    if candidates:
        return float(max(candidates))

    return None


def get_P0i_info(clc_code: str, slope_pct: float, grupo_hid: str) -> tuple[Optional[float], str]:
    """
    Like get_P0i_CLC but also returns a note string explaining the resolution.
    Returns (P0i, note).
    """
    ge3 = slope_pct >= 3.0
    grupo_hid = grupo_hid.upper()
    code, approximated = _resolve_code(clc_code)

    val = get_P0i_CLC(clc_code, slope_pct, grupo_hid)
    if val is None:
        return None, f"Código {clc_code} no encontrado en Tabla 2.3"

    note = ""
    if approximated or code != clc_code:
        note = f"Código {clc_code} → {code} (valor conservador, editable)"
    elif clc_code in ("21100",):
        note = "Cereales R/N ≥3% (valor por defecto, editable)"

    return val, note


def list_codes() -> list[str]:
    """Return all CLC codes present in Table 2.3."""
    return sorted({k[0] for k in _LOOKUP.keys()})


# ---------------------------------------------------------------------------
# CLC name resolution helper
# ---------------------------------------------------------------------------

def get_clc_name(clc_code: str) -> str:
    """
    Return human-readable land use name for a CLC code.
    Tries: exact match → prefix-3 canonical → prefix-3 padded → fallback label.
    Handles codes like "24300" (padded from "243") that don't exist in the table
    by resolving through _PREFIX3_TO_CODE5.
    """
    # 1. Direct match
    name = CLC_NAMES.get(clc_code)
    if name:
        return name

    # 2. Resolve via _resolve_code (handles 3/4 digit codes)
    resolved, _ = _resolve_code(clc_code)
    name = CLC_NAMES.get(resolved)
    if name:
        return name

    # 3. Use prefix-3 canonical mapping (handles "24300" → "24310" via "243")
    prefix3 = clc_code[:3]
    canonical = _PREFIX3_TO_CODE5.get(prefix3)
    if canonical:
        name = CLC_NAMES.get(canonical)
        if name:
            return name

    # 4. Fallback
    return f"Código CLC {clc_code}"


# ---------------------------------------------------------------------------
# CLC code → human-readable land use name (Spanish, from Table 2.3)
# ---------------------------------------------------------------------------
CLC_NAMES = {
    "11100": "Tejido urbano continuo",
    "11200": "Tejido urbano discontinuo",
    "11210": "Estructura urbana abierta",
    "11220": "Urbanizaciones exentas/ajardinadas",
    "12100": "Zonas industriales y comerciales",
    "12110": "Zonas industriales",
    "12120": "Grandes superficies equipamiento/servicios",
    "12200": "Redes viarias, ferroviarias y terrenos asociados",
    "12210": "Autopistas, autovías y terrenos asociados",
    "12220": "Complejos ferroviarios",
    "12300": "Zonas portuarias",
    "12400": "Aeropuertos",
    "13100": "Zonas de extracción minera",
    "13200": "Escombreras y vertederos",
    "13300": "Zonas de construcción",
    "14100": "Zonas verdes urbanas",
    "14200": "Instalaciones deportivas y recreativas",
    "14210": "Campos de golf",
    "14220": "Resto instalaciones deportivas/recreativas",
    "21100": "Tierras de labor en secano",
    "21200": "Terrenos regados permanentemente",
    "21210": "Cultivos herbáceos en regadío",
    "21220": "Otras zonas de irrigación",
    "21300": "Arrozales",
    "22100": "Viñedos",
    "22110": "Viñedos en secano",
    "22120": "Viñedos en regadío",
    "22200": "Frutales y plantaciones de bayas",
    "22210": "Frutales en secano",
    "22220": "Frutales en regadío",
    "22221": "Cítricos",
    "22222": "Frutales tropicales",
    "22223": "Otros frutales en regadío",
    "22300": "Olivares",
    "22310": "Olivares en secano",
    "22320": "Olivares en regadío",
    "23100": "Prados y praderas",
    "24110": "Cultivos anuales con cultivos permanentes (secano)",
    "24120": "Cultivos anuales con cultivos permanentes (regadío)",
    "24211": "Mosaico cultivos anuales con prados (secano)",
    "24212": "Mosaico cultivos permanentes en secano",
    "24213": "Mosaico cultivos anuales con permanentes (secano)",
    "24221": "Mosaico cultivos anuales con prados (regadío)",
    "24222": "Mosaico cultivos permanentes en regadío",
    "24223": "Mosaico cultivos anuales con permanentes (regadío)",
    "24230": "Mosaico cultivos mixtos secano y regadío",
    "24310": "Mosaico agrícola secano con vegetación natural",
    "24320": "Mosaico agrícola regadío con vegetación natural",
    "24330": "Mosaico prados con vegetación natural",
    "24400": "Sistemas agroforestales",
    "24410": "Pastizales/prados con arbolado adehesado",
    "24420": "Cultivos agrícolas con arbolado adehesado",
    "31100": "Frondosas",
    "31110": "Perennifolias",
    "31120": "Caducifolias y marcescentes",
    "31130": "Otras frondosas de plantación",
    "31140": "Mezclas de frondosas",
    "31150": "Bosques de ribera",
    "31160": "Laurisilva macaronésica",
    "31200": "Bosques de coníferas",
    "31210": "Bosques de coníferas de hojas aciculares",
    "31220": "Bosques de coníferas de hojas cupresáceo",
    "31300": "Bosque mixto",
    "32100": "Pastizales naturales",
    "32110": "Pastizales supraforestales",
    "32111": "Pastizales supraforestales templado-oceánicos",
    "32112": "Pastizales supraforestales mediterráneos",
    "32121": "Otros pastizales templado oceánicos",
    "32122": "Otros pastizales mediterráneos",
    "32200": "Landas y matorrales mesófilas",
    "32210": "Landas y matorrales en climas húmedos",
    "32220": "Fayal-brezal macaronésico",
    "32300": "Vegetación esclerófila",
    "32311": "Grandes formaciones de matorral denso",
    "32312": "Matorrales subarbustivos muy poco densos",
    "32320": "Matorrales xerófilos macaronésicos",
    "32400": "Matorral boscoso de transición",
    "32410": "Matorral boscoso de frondosas",
    "32420": "Matorral boscoso de coníferas",
    "32430": "Matorral boscoso de bosque mixto",
    "33110": "Playas y dunas",
    "33120": "Ramblas con poca o sin vegetación",
    "33200": "Roquedo",
    "33210": "Rocas desnudas con fuerte pendiente",
    "33220": "Afloramientos rocosos y canchales",
    "33230": "Coladas lávicas cuaternarias",
    "33300": "Espacios con vegetación escasa",
    "33310": "Xeroestepa subdesértica",
    "33320": "Cárcavas y/o zonas en proceso de erosión",
    "33330": "Espacios orófilos altitudinales con veg. escasa",
    "33400": "Zonas quemadas",
    "33500": "Glaciares y nieves permanentes",
    "41100": "Humedales y zonas pantanosas",
    "41200": "Turberas y prados turbosos",
    "42100": "Marismas",
    "42200": "Salinas",
    "42300": "Zonas llanas intermareales",
    "51100": "Cursos de agua",
    "51110": "Ríos y cauces naturales",
    "51120": "Canales artificiales",
    "51210": "Lagos y lagunas",
    "51220": "Embalses",
    "52100": "Lagunas costeras",
    "52200": "Estuarios",
    "52300": "Mares y océanos",
}


# ---------------------------------------------------------------------------
# Cv / YT table for automatic Pd calculation (DGC methodology)
# YT factors by Cv (rows) and T in years (columns): 2, 5, 10, 25, 50, 100, 200, 500
# Source: IC 5.2-IC / MOPU publication
# ---------------------------------------------------------------------------
CV_YT_TABLE = {
    0.30: {2:0.935, 5:1.194, 10:1.377, 25:1.625, 50:1.823, 100:2.022, 200:2.251, 500:2.541},
    0.31: {2:0.932, 5:1.198, 10:1.385, 25:1.640, 50:1.854, 100:2.068, 200:2.296, 500:2.602},
    0.32: {2:0.929, 5:1.202, 10:1.400, 25:1.671, 50:1.884, 100:2.098, 200:2.342, 500:2.663},
    0.33: {2:0.927, 5:1.209, 10:1.415, 25:1.686, 50:1.915, 100:2.144, 200:2.388, 500:2.724},
    0.34: {2:0.924, 5:1.213, 10:1.423, 25:1.717, 50:1.930, 100:2.174, 200:2.434, 500:2.785},
    0.35: {2:0.921, 5:1.217, 10:1.438, 25:1.732, 50:1.961, 100:2.220, 200:2.480, 500:2.831},
    0.36: {2:0.919, 5:1.225, 10:1.446, 25:1.747, 50:1.991, 100:2.251, 200:2.525, 500:2.892},
    0.37: {2:0.917, 5:1.232, 10:1.461, 25:1.778, 50:2.022, 100:2.281, 200:2.571, 500:2.953},
    0.38: {2:0.914, 5:1.240, 10:1.469, 25:1.793, 50:2.052, 100:2.327, 200:2.617, 500:3.014},
    0.39: {2:0.912, 5:1.243, 10:1.484, 25:1.808, 50:2.083, 100:2.357, 200:2.663, 500:3.067},
    0.40: {2:0.909, 5:1.247, 10:1.492, 25:1.839, 50:2.113, 100:2.403, 200:2.708, 500:3.128},
    0.41: {2:0.906, 5:1.255, 10:1.507, 25:1.854, 50:2.144, 100:2.434, 200:2.754, 500:3.189},
    0.42: {2:0.904, 5:1.259, 10:1.514, 25:1.884, 50:2.174, 100:2.480, 200:2.800, 500:3.250},
    0.43: {2:0.901, 5:1.263, 10:1.534, 25:1.900, 50:2.205, 100:2.510, 200:2.846, 500:3.311},
    0.44: {2:0.898, 5:1.270, 10:1.541, 25:1.915, 50:2.220, 100:2.556, 200:2.892, 500:3.372},
    0.45: {2:0.896, 5:1.274, 10:1.549, 25:1.945, 50:2.251, 100:2.586, 200:2.937, 500:3.433},
    0.46: {2:0.894, 5:1.278, 10:1.564, 25:1.961, 50:2.281, 100:2.632, 200:2.983, 500:3.494},
    0.47: {2:0.892, 5:1.286, 10:1.579, 25:1.991, 50:2.312, 100:2.663, 200:3.044, 500:3.555},
    0.48: {2:0.890, 5:1.289, 10:1.595, 25:2.007, 50:2.342, 100:2.708, 200:3.098, 500:3.616},
    0.49: {2:0.887, 5:1.293, 10:1.603, 25:2.022, 50:2.373, 100:2.739, 200:3.128, 500:3.677},
    0.50: {2:0.885, 5:1.297, 10:1.610, 25:2.052, 50:2.403, 100:2.785, 200:3.189, 500:3.738},
    0.51: {2:0.883, 5:1.301, 10:1.625, 25:2.068, 50:2.434, 100:2.815, 200:3.220, 500:3.799},
    0.52: {2:0.881, 5:1.308, 10:1.640, 25:2.098, 50:2.464, 100:2.861, 200:3.281, 500:3.860},
}

_CV_SORTED = sorted(CV_YT_TABLE.keys())


def get_YT(cv: float, T: int) -> Optional[float]:
    """
    Interpolate YT for a given Cv and return period T.
    Uses linear interpolation between adjacent Cv rows.
    T must be one of: 2, 5, 10, 25, 50, 100, 200, 500.
    Returns None if T not in table or Cv out of range.
    """
    T_keys = [2, 5, 10, 25, 50, 100, 200, 500]
    if T not in T_keys:
        return None
    cv = round(cv, 10)

    # Exact match
    if cv in CV_YT_TABLE:
        return CV_YT_TABLE[cv][T]

    # Out of range
    if cv < _CV_SORTED[0] or cv > _CV_SORTED[-1]:
        return None

    # Linear interpolation
    for i in range(len(_CV_SORTED) - 1):
        cv_lo = _CV_SORTED[i]
        cv_hi = _CV_SORTED[i + 1]
        if cv_lo <= cv <= cv_hi:
            yt_lo = CV_YT_TABLE[cv_lo][T]
            yt_hi = CV_YT_TABLE[cv_hi][T]
            frac = (cv - cv_lo) / (cv_hi - cv_lo)
            return yt_lo + frac * (yt_hi - yt_lo)
    return None


def calc_Pd_from_P_Cv(P_media: float, cv: float, T: int) -> Optional[float]:
    """
    Compute Pd (mm/day) for return period T from:
      P_media: mean annual daily max precipitation (mm)
      cv: coefficient of variation
      T: return period in years (2,5,10,25,50,100,200,500)
    Returns Pd = P_media * YT(cv, T), or None if out of range.
    """
    yt = get_YT(cv, T)
    if yt is None:
        return None
    return P_media * yt
