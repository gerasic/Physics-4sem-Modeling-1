import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

mu0 = 4 * np.pi * 1e-7

def plot_fields():
    try:
        I       = float(entries['I'].get())
        mu_rs   = [float(x) for x in entries['mu_r'].get().split(',')]
        dirc    = float(entries['direction'].get())
        D_t     = float(entries['D_toroid'].get())
        d_sec   = float(entries['d_section'].get())
        N_t     = int(entries['N_toroid'].get())
        N_c     = int(entries['N_cyl'].get())
        L_c     = float(entries['L_cyl'].get())
    except Exception as e:
        messagebox.showerror("Input Error", f"Неверный ввод: {e}")
        return

    R_t = D_t/2
    a   = d_sec/2
    R_c = d_sec/2

    x0_t = R_t/2
    x0_c = R_c/2

    z = np.linspace(-3*max(R_t,R_c), 3*max(R_t,R_c), 1000)

    plt.figure(figsize=(10,6))

    for mu_r in mu_rs:
        R1 = (R_t + a) - x0_t
        R2 = (R_t - a) - x0_t

        B_t = dirc * mu_r * mu0 * N_t * I / 2 * (
            R1**2 / ( (R1**2 + z**2)**1.5 ) -
            R2**2 / ( (R2**2 + z**2)**1.5 )
        )
        plt.plot(z, B_t, label=f"Тороид μr={mu_r}")

    n = N_c / L_c
    R_eff = np.sqrt(R_c**2 + x0_c**2)
    for mu_r in mu_rs:
        B_c = dirc * mu_r * mu0 * n * I / 2 * (
            ( (z + L_c/2) / np.sqrt(R_eff**2 + (z + L_c/2)**2) ) -
            ( (z - L_c/2) / np.sqrt(R_eff**2 + (z - L_c/2)**2) )
        )
        plt.plot(z, B_c, '--', label=f"Соленоид μr={mu_r}")

    plt.title("B(z) по оси, смещённой на R/2 от центра катушки")
    plt.xlabel("z, м")
    plt.ylabel("B, Тл")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("Магнитное поле: тороид vs. соленоид (ось смещена на R/2)")

entries = {}
params = [
    ("Ток I, A",         'I',         "1.0"),
    ("μr (через запятую)",'mu_r',      "1,100,1000"),
    ("Направление (±1)",  'direction', "1"),
    ("Диаметр тора D, м",'D_toroid',  "0.5"),
    ("Диаметр попереч. d, м",'d_section',"0.1"),
    ("Витков в тороиде Nₜ",'N_toroid', "100"),
    ("Витков в соленоиде N꜀",'N_cyl',    "100"),
    ("Длина соленоида L, м",'L_cyl',   "0.2"),
]

for text, var, default in params:
    frm = ttk.Frame(root)
    frm.pack(fill='x', padx=8, pady=4)
    ttk.Label(frm, text=text).pack(side='left')
    e = ttk.Entry(frm); e.insert(0, default); e.pack(side='right', expand=True, fill='x')
    entries[var] = e

ttk.Button(root, text="Построить графики", command=plot_fields).pack(pady=10)

root.mainloop()
