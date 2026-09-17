# Model Rocket Aerodynamic Design & 3D Flight Telemetry

A personal engineering project focused on designing a high-power model rocket in OpenRocket and building a Python pipeline to process flight data, reconstruct 3D trajectories, and visualize real-time telemetries.
<img width="1920" height="1200" alt="openrocket_plot" src="https://github.com/user-attachments/assets/836b80a4-8d24-4000-8b97-901c414c51ec" />
<img width="1920" height="1200" alt="openrocket_simulation" src="https://github.com/user-attachments/assets/0a819417-a117-4d97-b37e-8ca6e915d351" />
<img width="1920" height="1140" alt="openrocket" src="https://github.com/user-attachments/assets/e7e2e292-d14c-4861-b737-58c0aea9cabb" />

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
