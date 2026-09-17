# Model Rocket Aerodynamic Design & 3D Flight Telemetry

A personal engineering project focused on designing a high-power model rocket in OpenRocket and building a Python pipeline to process flight data, reconstruct 3D trajectories, and visualize real-time telemetries.

---

## Design & Aerodynamics
The main goal was to achieve stable vertical flight while maintaining a safe stability margin across the burn profile.

* **Airframe:** 50 mm diameter, ~1100 mm overall length
* **Nose Cone:** Low-drag Ogive profile
* **Fins:** 4-fin trapezoidal geometry
* **Stability Margin:** **1.09 cal** (Calculated at launch rail exit; stays within the 1.0–2.0 safe envelope to prevent both under-stabilization and excessive weathercocking)

---

## Flight Performance & 3D Visualization
Flight metrics were exported from OpenRocket numerical logs and post-processed using Python.

![3D Flight Trajectory](trajectory_3d.png)

* **Apogee:** ~875.7 m
* **Interactive Visualization:** The repository includes `flight_trajectory.html`. Opening it in any browser provides an interactive 3D model of the trajectory with speed-mapped coloring and airframe orientation at apogee.
* **Telemetry Animation:** `simulation_flight.py` also runs an animated dual-plot tracking real-time altitude and velocity profiles.

---

## Stack
* **Aerodynamic Sizing & Simulation:** OpenRocket
* **Data Processing & Plotting:** Python (`numpy`, `pandas`, `matplotlib`, `plotly`)

---

## How to Run
```bash
git clone [https://github.com/](https://github.com/)<kullanici-adin>/model-rocket-aerodynamic-trajectory.git
cd model-rocket-aerodynamic-trajectory
pip install numpy pandas matplotlib plotly
python simulation_flight.py