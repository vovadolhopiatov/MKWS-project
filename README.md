# Laminar Burning Velocity of H₂/CH₄ Blends

**Warsaw University of Technology**  
Faculty of Power and Aeronautical Engineering  
*Computational Methods in Combustion — 2026*

**Author:** Volodymyr Dolhopiatov (335822)  
**Supervisor:** dr inż. Mateusz Żbikowski

---

## Topic

Numerical study of the laminar burning velocity and adiabatic flame temperature of hydrogen–methane (H₂/CH₄) blends as a function of equivalence ratio φ and hydrogen blend fraction α.

## Tools

| Tool | Purpose |
|------|---------|
| [Cantera 3.0](https://cantera.org) | 1D FreeFlame solver |
| GRI-Mech 3.0 | Chemical kinetic mechanism (53 species, 325 reactions) |
| Python 3 | Simulation & plotting |
| LaTeX + pgfplots | Report |

## Initial Conditions

| Parameter | Value |
|-----------|-------|
| Temperature | 300 K |
| Pressure | 1 atm (101 325 Pa) |
| Equivalence ratio φ | 0.6 – 1.6 |
| H₂ blend fraction α | 0%, 25%, 50%, 75%, 100% |

## Results

- Burning velocity increases nonlinearly with hydrogen fraction — from ~37 cm/s (pure CH₄) to ~252 cm/s (pure H₂) at φ = 1.0
- Peak velocity shifts towards richer conditions as α increases (Lewis number effect)
- Adiabatic flame temperature rises by ~250 K from pure methane to pure hydrogen
- H₂ combustion eliminates CO₂ and CO but retains NOₓ emissions

## Files

```
├── burning_velocity.py       # Main simulation script (Cantera)
├── combustion_project.tex    # Full LaTeX report
├── combustion_project.pdf    # Compiled report
└── pw_logo.png               # Warsaw University of Technology logo
```

## How to Run

```bash
pip install cantera numpy matplotlib
python burning_velocity.py
```
