"""
Laminar Burning Velocity of H2/CH4 Blends
==========================================
Computational Methods in Combustion
Warsaw University of Technology, 2026

Author: Volodymyr Dolhopiatov (335822)
Supervisor: dr inż. Mateusz Żbikowski

Description:
    Computes laminar burning velocity and adiabatic flame temperature
    for H2/CH4/air mixtures using Cantera FreeFlame solver and
    GRI-Mech 3.0 reaction mechanism.

Requirements:
    pip install cantera numpy matplotlib
"""

import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import csv

# ----------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------
MECHANISM  = "gri30.yaml"       # GRI-Mech 3.0 (bundled with Cantera)
T_UNBURNED = 300.0              # Initial temperature [K]
P_UNBURNED = ct.one_atm         # Initial pressure [Pa] = 101325 Pa

phi_range  = np.linspace(0.6, 1.6, 13)         # Equivalence ratio sweep
alpha_vals = [0.0, 0.25, 0.50, 0.75, 1.0]      # H2 mole fractions in fuel


# ----------------------------------------------------------------
# Helper: build fuel composition string
# ----------------------------------------------------------------
def fuel_string(alpha: float) -> str:
    """Return Cantera fuel composition for a given H2 fraction alpha."""
    if alpha == 0.0:
        return "CH4:1"
    elif alpha == 1.0:
        return "H2:1"
    else:
        ch4_frac = 1.0 - alpha
        return f"H2:{alpha:.4f},CH4:{ch4_frac:.4f}"


# ----------------------------------------------------------------
# Main sweep
# ----------------------------------------------------------------
results = {}   # dict: alpha -> list of (phi, S_L, T_ad)

for alpha in alpha_vals:
    print(f"\n=== alpha = {alpha*100:.0f}% H2 ===")
    fuel = fuel_string(alpha)
    data = []

    # Initialise gas and flame for first phi value
    gas = ct.Solution(MECHANISM)
    gas.set_equivalence_ratio(phi_range[0], fuel, "O2:1,N2:3.76",
                              basis="mole")
    gas.TP = T_UNBURNED, P_UNBURNED

    flame = ct.FreeFlame(gas, width=0.03)       # 3 cm domain
    flame.set_refine_criteria(ratio=3, slope=0.06, curve=0.12, prune=0.01)
    flame.transport_model = "mixture-averaged"
    flame.solve(loglevel=0, auto=True)

    for i, phi in enumerate(phi_range):
        gas.set_equivalence_ratio(phi, fuel, "O2:1,N2:3.76", basis="mole")
        gas.TP = T_UNBURNED, P_UNBURNED
        flame.inlet.X = gas.X
        flame.inlet.T = T_UNBURNED

        # Warm-start from previous solution for faster convergence
        flame.solve(loglevel=0, auto=(i == 0))

        S_L  = flame.velocity[0] * 100     # m/s -> cm/s
        T_ad = flame.T[-1]                 # adiabatic post-flame temperature [K]
        data.append((phi, S_L, T_ad))
        print(f"  phi={phi:.2f}  S_L={S_L:7.2f} cm/s  T_ad={T_ad:8.1f} K")

    results[alpha] = data


# ----------------------------------------------------------------
# Save results to CSV
# ----------------------------------------------------------------
with open("sl_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["alpha", "phi", "SL_cm_per_s", "Tad_K"])
    for alpha, rows in results.items():
        for phi, sl, tad in rows:
            writer.writerow([alpha, phi, sl, tad])

print("\nResults saved to sl_results.csv")


# ----------------------------------------------------------------
# Plot 1: S_L vs equivalence ratio (all blends)
# ----------------------------------------------------------------
labels = {
    0.00: r"$\alpha=0\%$  (pure CH$_4$)",
    0.25: r"$\alpha=25\%$",
    0.50: r"$\alpha=50\%$",
    0.75: r"$\alpha=75\%$",
    1.00: r"$\alpha=100\%$ (pure H$_2$)",
}

fig1, ax1 = plt.subplots(figsize=(9, 5))
for alpha, data in results.items():
    phis = [d[0] for d in data]
    sls  = [d[1] for d in data]
    ax1.plot(phis, sls, marker="o", label=labels[alpha])

ax1.set_xlabel(r"Equivalence ratio $\varphi$ [-]", fontsize=12)
ax1.set_ylabel(r"Laminar burning velocity $S_L$ [cm/s]", fontsize=12)
ax1.set_title("Laminar Burning Velocity vs Equivalence Ratio", fontsize=13)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
fig1.tight_layout()
fig1.savefig("sl_vs_phi.pdf", dpi=300)
print("Figure saved: sl_vs_phi.pdf")


# ----------------------------------------------------------------
# Plot 2: S_L vs hydrogen fraction at phi = 1.0
# ----------------------------------------------------------------
phi_target   = 1.0
alphas_pct   = []
sls_at_stoich = []

for alpha, data in results.items():
    for phi, sl, tad in data:
        if abs(phi - phi_target) < 1e-6:
            alphas_pct.append(alpha * 100)
            sls_at_stoich.append(sl)
            break

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.plot(alphas_pct, sls_at_stoich, "b-o", lw=2, markersize=7)
ax2.set_xlabel(r"Hydrogen mole fraction $\alpha$ [%]", fontsize=12)
ax2.set_ylabel(r"$S_L$ at $\varphi=1.0$ [cm/s]", fontsize=12)
ax2.set_title(r"Burning Velocity vs H$_2$ Fraction at $\varphi=1.0$", fontsize=13)
ax2.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig("sl_vs_alpha.pdf", dpi=300)
print("Figure saved: sl_vs_alpha.pdf")


# ----------------------------------------------------------------
# Plot 3: Adiabatic flame temperature vs equivalence ratio
# ----------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(9, 5))
for alpha, data in results.items():
    phis = [d[0] for d in data]
    tads = [d[2] for d in data]
    ax3.plot(phis, tads, marker="s", label=labels[alpha])

ax3.set_xlabel(r"Equivalence ratio $\varphi$ [-]", fontsize=12)
ax3.set_ylabel(r"Adiabatic flame temperature $T_{ad}$ [K]", fontsize=12)
ax3.set_title("Adiabatic Flame Temperature vs Equivalence Ratio", fontsize=13)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)
fig3.tight_layout()
fig3.savefig("temperature_vs_phi.pdf", dpi=300)
print("Figure saved: temperature_vs_phi.pdf")

plt.show()
print("\nDone.")
