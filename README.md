# IC52Rational — Método Racional IC 5.2-IC

[![QGIS](https://img.shields.io/badge/QGIS-3.40%2B-green)](https://qgis.org)
[![License](https://img.shields.io/badge/License-GPL%20v2-blue)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-orange)](https://github.com/pedroiba94/IC52Rational/releases)

QGIS plugin for peak flow calculation using the **Rational Method** of the Spanish Road Drainage Standard (**Norma 5.2-IC**, Chapter 2, BOE 2016). Computes design flows QT for 8 return periods simultaneously, with full traceability of all intermediate variables.

> Developed by **Pedro Bohorquez Aliaga** and **Hugo Bohorquez Aliaga** 

---

## Features

- **8 simultaneous return periods**: T = 2, MCO (≈2.5, interpolated), 5, 10, 25, 50, 100 and 500 years
- **Full formula chain** per IC 5.2-IC Chapter 2: KA → tc → Id → Fa/Fb → Fint → I(T,tc) → C → Kt → **QT**
- **Heterogeneous catchment** (§2.2.4): Σ[Ci·Ai] per land use from CLC layer
- **P0i automatic calculation** from Corine Land Cover layer loaded in QGIS (Table 2.3 — same approach as [CLC2Manning](https://plugins.qgis.org/plugins/CLC2Manning/))
- **Regional β corrector** — all regions from Table 2.5, with log-linear FT interpolation for MCO and T=50
- **Pd from P_media + Cv** — automatic calculation using DGC publication table (linear interpolation)
- **Levante/SE method** §2.3 for regions 72, 821 and 822 with T > 25 years
- **Contextual ArcGIS Online maps**:
  - Tab ② Precipitation → β regions map (Fig. 2.9)
  - Tab ③ Soil → Hydrological groups map (Fig. 2.7)
- **Excel export** — colour-coded results table (.xlsx)
- Compatible with **QGIS 3.40+** (Qt5) and **QGIS 4.0+** (Qt6)

---

## Screenshots

| Pestaña ② Precipitación | Pestaña ③ Suelo / P₀ | Pestaña ④ Resultados |
|:-:|:-:|:-:|
| Mapa regiones β (Fig. 2.9) | Mapa grupos hidrológicos (Fig. 2.7) | QT para 8 períodos de retorno |

---

## Installation

### From QGIS Plugin Manager (recommended)
1. Open QGIS → **Plugins → Manage and Install Plugins**
2. Search for `IC52Rational`
3. Click **Install**

### From ZIP (manual)
1. Download the latest [release ZIP](https://github.com/pedroiba94/IC52Rational/releases)
2. QGIS → **Plugins → Manage and Install Plugins → Install from ZIP**
3. Select the downloaded file

---

## Usage

### Tab ① — Catchment
Enter manually:
- **A** (km²) — catchment area
- **Lc** (km) — main channel length
- **Jc** (m/m) — mean channel slope

The plugin calculates KA, tc and Kt automatically.

### Tab ② — Precipitation
- **Pd for each T** — enter directly, or use the **Cv/P_media calculator** (DGC table, linear interpolation)
- **I₁/Id** — torrentiality index from Fig. 2.4 map (displayed automatically when on this tab)
- **β region** — select from Fig. 2.9 map (displayed automatically)
- **Work type** — transversal drainage (DT) or platform/margins (PM)

### Tab ③ — Soil / P₀
- Select **hydrological group** A/B/C/D (Fig. 2.7 map displayed automatically)
- Select **CLC layer** loaded in QGIS → click **Load land uses from CLC**
- The plugin reads CODE_18 codes, resolves them to Table 2.3 canonical codes, and computes weighted P0i per land use
- **P0i values are editable** — adjust if needed

### Tab ④ — Results
- Full intermediate variable table for all 8 return periods
- Colour-coded QT summary boxes
- **Export to Excel (.xlsx)** button

---

## Requirements

- QGIS 3.40 or later
- Internet connection (for ArcGIS Online reference maps — optional, does not affect calculation)
- `openpyxl` for Excel export (included in most QGIS installations)

---

## Formulas implemented

| Variable | Formula | Reference |
|---|---|---|
| KA | 1 − log₁₀(A)/15 | §2.2.2.3 |
| tc | 0.3 · Lc^0.76 · Jc^−0.19 | §2.2.2.5 |
| Id | Pd · KA / 24 | §2.2.2.2 |
| Fa | (I₁/Id)^(3.5287 − 2.5287·tc^0.1) | §2.2.2.4 |
| C | f(Pd·KA/P₀) | §2.2.3.1 |
| Kt | 1 + tc^1.25 / (tc^1.25 + 14) | §2.2.5 |
| QT | I·C·A·Kt / 3.6 | §2.2.1 |
| QT (heterog.) | Kt·I·Σ[Ci·Ai] / 3.6 | §2.2.4 |
| β | βm · FT (PM) or (βm − Δ50) · FT (DT) | §2.2.3.4 |

---

## Related plugins

| Plugin | Description |
|---|---|
| [BetaSpainMap](https://github.com/pedroiba94/BetaSpainMap) | Interactive β and FT coefficient lookup by map click |
| [CLC2Manning](https://plugins.qgis.org/plugins/CLC2Manning/) | Manning coefficient from Corine Land Cover |
| [SIOSE2CN](https://plugins.qgis.org/plugins/SIOSE2CN/) | Curve Number and P0 from SIOSE |

---

## Reference

**Norma 5.2-IC Drenaje Superficial** — Instrucción de Carreteras  
BOE núm. 60, de 10 de marzo de 2016  
[https://www.boe.es/boe/dias/2016/03/10/pdfs/BOE-A-2016-2405.pdf](https://www.boe.es/boe/dias/2016/03/10/pdfs/BOE-A-2016-2405.pdf)

**Publicación DGC — Mapas para el cálculo de máximas precipitaciones**  
Dirección General de Carreteras, MOPU  
[https://www.transportes.gob.es/recursos_mfom/0610300.pdf](https://www.transportes.gob.es/recursos_mfom/0610300.pdf)

---

## License

This plugin is released under the [GNU General Public License v2](LICENSE).

© 2026 Pedro Bohorquez Aliaga, Hugo Bohorquez Aliaga
