import os
import csv
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.animation as animation

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, "flight_data.csv")

clean_rows = []
header = None

with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
    sample = f.read(2048)
    f.seek(0)
    delimiter = ';' if ';' in sample else (',' if ',' in sample else None)
    
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('Event'):
            continue
        
        parts = [p.strip() for p in (line.split(delimiter) if delimiter else line.split())]
        
        if header is None:
            try:
                float(parts[0])
                header = [f"col_{i}" for i in range(len(parts))]
                clean_rows.append([float(p) for p in parts])
            except ValueError:
                header = [p.lower() for p in parts]
                continue
        else:
            try:
                vals = [float(p) for p in parts[:len(header)]]
                clean_rows.append(vals)
            except ValueError:
                continue

data = np.array(clean_rows)

def get_col_index(keywords, default_idx):
    for kw in keywords:
        for idx, name in enumerate(header):
            if kw in name:
                return idx
    return default_idx

time_idx = get_col_index(['time', 't', 'zaman'], 0)
alt_idx = get_col_index(['altitude', 'alt', 'irtifa', 'height'], 1)
vel_idx = get_col_index(['velocity', 'speed', 'hız', 'vel'], 2 if data.shape[1] > 2 else None)

time = data[:, time_idx]
altitude = data[:, alt_idx]
velocity = data[:, vel_idx] if vel_idx is not None else np.gradient(altitude, time)

drift_x = 0.05 * altitude + 2 * np.sin(time / 2)
drift_y = 0.03 * altitude + 1.5 * np.cos(time / 2)

# ==========================================================
# 1. 3D ROKET GEOMETRİSİ + YÖRÜNGE (PLOTLY INTERACTIVE)
# ==========================================================
fig = go.Figure()

# Uçuş İzi
fig.add_trace(go.Scatter3d(
    x=drift_x, y=drift_y, z=altitude,
    mode='lines',
    line=dict(color=velocity, colorscale='Turbo', width=5),
    name='Uçuş Yörüngesi'
))

# Apogee Konumu
max_idx = np.argmax(altitude)
rx, ry, rz = drift_x[max_idx], drift_y[max_idx], altitude[max_idx]

# 1) Silindir Gövde
body_radius = 5.0
body_length = 60.0
z_body = np.linspace(rz - body_length, rz, 15)
theta = np.linspace(0, 2 * np.pi, 15)
theta_grid, z_grid = np.meshgrid(theta, z_body)
x_body = rx + body_radius * np.cos(theta_grid)
y_body = ry + body_radius * np.sin(theta_grid)

fig.add_trace(go.Surface(
    x=x_body, y=y_body, z=z_grid,
    colorscale=[[0, '#e6edf3'], [1, '#8b949e']],
    showscale=False,
    name='Gövde'
))

# 2) Konik Burun
nose_length = 30.0
z_nose = np.linspace(rz, rz + nose_length, 15)
theta_n, z_n = np.meshgrid(theta, z_nose)
cone_radius = body_radius * (1 - (z_n - rz) / nose_length)
x_nose = rx + cone_radius * np.cos(theta_n)
y_nose = ry + cone_radius * np.sin(theta_n)

fig.add_trace(go.Surface(
    x=x_nose, y=y_nose, z=z_n,
    colorscale=[[0, '#ff4d4d'], [1, '#b30000']],
    showscale=False,
    name='Burun Konisi'
))

# 3) Kanatçıklar (Mesh3d ile katı yüzey)
fin_span = 14.0
z_bottom = rz - body_length
z_top = rz - body_length + 18.0

# Sağ Fin (+X)
fig.add_trace(go.Mesh3d(
    x=[rx + body_radius, rx + body_radius + fin_span, rx + body_radius],
    y=[ry, ry, ry],
    z=[z_bottom, z_bottom, z_top],
    color='#ff7b00', opacity=0.9, name='Kanatçıklar'
))
# Sol Fin (-X)
fig.add_trace(go.Mesh3d(
    x=[rx - body_radius, rx - body_radius - fin_span, rx - body_radius],
    y=[ry, ry, ry],
    z=[z_bottom, z_bottom, z_top],
    color='#ff7b00', opacity=0.9, showlegend=False
))
# Ön Fin (+Y)
fig.add_trace(go.Mesh3d(
    x=[rx, rx, rx],
    y=[ry + body_radius, ry + body_radius + fin_span, ry + body_radius],
    z=[z_bottom, z_bottom, z_top],
    color='#ff7b00', opacity=0.9, showlegend=False
))
# Arka Fin (-Y)
fig.add_trace(go.Mesh3d(
    x=[rx, rx, rx],
    y=[ry - body_radius, ry - body_radius - fin_span, ry - body_radius],
    z=[z_bottom, z_bottom, z_top],
    color='#ff7b00', opacity=0.9, showlegend=False
))

# Apogee Etiketi
fig.add_trace(go.Scatter3d(
    x=[rx], y=[ry], z=[rz + nose_length + 12],
    mode='text',
    text=[f"🚀 Apogee: {rz:.1f} m"],
    textposition="top center",
    textfont=dict(color="white", size=14),
    showlegend=False
))

fig.update_layout(
    title="3D Model Roket Uçuş Yörüngesi ve Zirve Noktası",
    scene=dict(
        xaxis_title="Doğu Drift (m)",
        yaxis_title="Kuzey Drift (m)",
        zaxis_title="İrtifa (m)",
        aspectmode='data'
    ),
    template="plotly_dark"
)

html_output = os.path.join(script_dir, "flight_trajectory.html")
fig.write_html(html_output)
print(f"3D Model Roket kaydedildi: {html_output}")

# ==========================================
# 2. CANLI TELEMETRİ ANİMASYONU
# ==========================================
fig_anim, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
fig_anim.patch.set_facecolor('#0d1117')

for ax in (ax1, ax2):
    ax.set_facecolor('#161b22')
    ax.tick_params(colors='white')
    ax.grid(True, linestyle='--', alpha=0.3)

ax1.set_title("Canlı İrtifa Profili", color='white', fontweight='bold')
ax1.set_xlim(0, max(time))
ax1.set_ylim(0, max(altitude) * 1.1)
ax1.set_xlabel("Zaman (s)", color='white')
ax1.set_ylabel("İrtifa (m)", color='white')

ax2.set_title("Canlı Hız Profili", color='white', fontweight='bold')
ax2.set_xlim(0, max(time))
ax2.set_ylim(min(velocity) * 1.1, max(velocity) * 1.1)
ax2.set_xlabel("Zaman (s)", color='white')
ax2.set_ylabel("Hız (m/s)", color='white')

line1, = ax1.plot([], [], color='#58a6ff', lw=2.5)
line2, = ax2.plot([], [], color='#f85149', lw=2.5)
point1, = ax1.plot([], [], 'o', color='white', markersize=6)
point2, = ax2.plot([], [], 'o', color='white', markersize=6)

step = max(1, len(time) // 200)
frame_indices = list(range(0, len(time), step))

def update(frame):
    idx = frame_indices[frame]
    line1.set_data(time[:idx], altitude[:idx])
    point1.set_data([time[idx]], [altitude[idx]])
    line2.set_data(time[:idx], velocity[:idx])
    point2.set_data([time[idx]], [velocity[idx]])
    return line1, point1, line2, point2

ani = animation.FuncAnimation(fig_anim, update, frames=len(frame_indices), interval=30, blit=True)
plt.tight_layout()
plt.show()