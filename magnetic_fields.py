import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

mu0 = 4 * np.pi * 1e-7

def plot_fields():
    try:
        I = float(entries['I'].get())
        mu_r_values = [float(x) for x in entries['mu_r'].get().split(',')]
        direction = float(entries['direction'].get())
        D_toroid = float(entries['D_toroid'].get())
        d_section = float(entries['d_section'].get())
        N_t = int(entries['N_toroid'].get())
        N_c = int(entries['N_cyl'].get())
        L_c = float(entries['L_cyl'].get())
    except Exception as e:
        messagebox.showerror("Input Error", f"Неверный ввод: {e}")
        return

    R_t = D_toroid / 2
    a = d_section / 2
    R_c = d_section / 2

    z = np.linspace(-3 * max(R_t, R_c), 3 * max(R_t, R_c), 1000)

    plt.figure(figsize=(10, 6))

    for mu_r in mu_r_values:
        B_t = direction * mu_r * mu0 * N_t * I / 2 * (
            ((R_t + a)**2 / ((R_t + a)**2 + z**2)**1.5) -
            ((R_t - a)**2 / ((R_t - a)**2 + z**2)**1.5)
        )
        plt.plot(z, B_t, label=f"Тороид μr={mu_r}")

    for mu_r in mu_r_values:
        n = N_c / L_c
        B_c = direction * mu_r * mu0 * n * I / 2 * (
            ((z + L_c/2) / np.sqrt(R_c**2 + (z + L_c/2)**2)) -
            ((z - L_c/2) / np.sqrt(R_c**2 + (z - L_c/2)**2))
        )
        plt.plot(z, B_c, '--', label=f"Соленоид μr={mu_r}")

    plt.title("Индукция магнитного поля B(z)\nтороидальная vs. цилиндрическая катушка")
    plt.xlabel("z, м")
    plt.ylabel("B, Тл")
    plt.legend()
    plt.grid(True)
    plt.show()

root = tk.Tk()
root.title("Магнитное поле: Toroid & Solenoid")

entries = {}
params = [
    ("Ток I (А)", 'I', "1.0"),
    ("Проницаемость μr (через запятую)", 'mu_r', "1,100,1000"),
    ("Направление тока (±1)", 'direction', "1"),
    ("Диаметр тора D (м)", 'D_toroid', "0.5"),
    ("Диаметр сечения d (м)", 'd_section', "0.1"),
    ("Витков в тороиде Nt", 'N_toroid', "100"),
    ("Витков в соленоиде Nc", 'N_cyl', "100"),
    ("Длина соленоида L (м)", 'L_cyl', "0.2"),
]

for label_text, var, default in params:
    frame = ttk.Frame(root)
    frame.pack(fill='x', padx=8, pady=4)
    ttk.Label(frame, text=label_text).pack(side='left')
    entry = ttk.Entry(frame)
    entry.insert(0, default)
    entry.pack(side='right', expand=True, fill='x')
    entries[var] = entry

ttk.Button(root, text="Построить графики", command=plot_fields).pack(pady=10)

root.mainloop()
