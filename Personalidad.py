import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from bascon import obtener_preguntas, guardar_resultado_usuario
from motorInter import motor_inferencia
from reglas import reglas_preguntas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

preguntas = obtener_preguntas()

class NeuroTypeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroType")
        self.root.geometry("420x800")
        self.root.resizable(False, False)

        # Fondo principal
        self.fondo_img = Image.open("fondo.png").resize((420, 800))
        self.fondo_tk = ImageTk.PhotoImage(self.fondo_img)

        self.pregunta_actual = 0
        self.respuestas_usuario = []

        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
        self.limpiar_ventana()

        portada_img = Image.open("portada.png").resize((420, 800))
        self.portada_tk = ImageTk.PhotoImage(portada_img)

        portada_label = tk.Label(self.root, image=self.portada_tk, borderwidth=0)
        portada_label.place(x=0, y=0, relwidth=1, relheight=1)

        boton_comenzar = tk.Button(self.root, text="Comenzar Test", command=self.mostrar_preguntas_lote,
                                   bg="#66bb6a", fg="white", font=("Helvetica", 12, "bold"), padx=15, pady=5, bd=0)
        boton_comenzar.place(relx=0.5, rely=0.9, anchor="center")

    def mostrar_preguntas_lote(self):
        self.limpiar_ventana()

        frame = tk.Frame(self.root, bg="#fdf6f0")
        frame.pack(expand=True, pady=60)

        preguntas_lote = preguntas[self.pregunta_actual:self.pregunta_actual + 3]
        self.botones_respuestas = []

        for idx, pregunta in enumerate(preguntas_lote):
            card = tk.Frame(frame, bg="#fdf6f0")
            card.pack(padx=20, pady=15, fill="both")

            tk.Label(card, text=pregunta, wraplength=300, font=("Helvetica", 14), bg="#fdf6f0", fg="black").pack(pady=10)
            botones_frame = tk.Frame(card, bg="#fdf6f0")
            botones_frame.pack(pady=5)

            var = tk.IntVar(value=-1)
            self.botones_respuestas.append(var)

            tk.Radiobutton(botones_frame, variable=var, value=0, bg="#ef5350", fg="white", width=4, height=1, bd=0,
                           relief="flat", indicatoron=0).grid(row=0, column=0, padx=30, pady=5)
            tk.Radiobutton(botones_frame, variable=var, value=1, bg="#66bb6a", fg="white", width=4, height=1, bd=0,
                           relief="flat", indicatoron=0).grid(row=0, column=1, padx=30, pady=5)

        boton_frame = tk.Frame(self.root, bg="#fdf6f0")
        boton_frame.pack(side="bottom", anchor="e", padx=15, pady=15)

        tk.Button(boton_frame, text="➡", command=self.registrar_respuestas_lote,
                  font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#000", relief="flat", padx=10, pady=5).pack()

    def registrar_respuestas_lote(self):
        for var in self.botones_respuestas:
            valor = var.get()
            self.respuestas_usuario.append(valor if valor in [0, 1] else 0)

        self.pregunta_actual += 3
        if self.pregunta_actual < len(preguntas):
            self.mostrar_preguntas_lote()
        else:
            self.mostrar_resultado()

    def mostrar_resultado(self):
        self.limpiar_ventana()

        nombre = simpledialog.askstring("Nombre", "Escribe tu nombre:") or "Anónimo"
        resultado, conclusion = motor_inferencia(self.respuestas_usuario)
        guardar_resultado_usuario(nombre, resultado)

        intro = sum(1 for i, r in enumerate(self.respuestas_usuario)
                    if r == 1 and reglas_preguntas.get(preguntas[i]) == "introvertido")
        extro = sum(1 for i, r in enumerate(self.respuestas_usuario)
                    if r == 1 and reglas_preguntas.get(preguntas[i]) == "extrovertido")

        tk.Label(self.root, text=f"Tu personalidad es: {resultado.upper()}",
                 font=("Helvetica", 18), bg="#fdf6f0", fg="#2196f3").pack(pady=10)

        tk.Label(self.root, text=conclusion, font=("Helvetica", 13), bg="#fdf6f0",
                 fg="black", wraplength=340, justify="center").pack(pady=10)

        etiquetas = []
        valores = []
        colores = []

        if intro == 0 and extro == 0:
            etiquetas = [resultado]
            valores = [1]
            colores = ["#64b5f6"] if resultado == "introvertido" else ["#81c784"]
        else:
            if intro > 0:
                etiquetas.append("Introvertido")
                valores.append(intro)
                colores.append("#64b5f6")
            if extro > 0:
                etiquetas.append("Extrovertido")
                valores.append(extro)
                colores.append("#81c784")

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        wedges, texts = ax.pie(valores, labels=etiquetas, colors=colores,
                               startangle=90, wedgeprops={'edgecolor': 'black'},
                               textprops={'fontsize': 12})

        centre_circle = plt.Circle((0, 0), 0.55, fc='white')
        ax.add_artist(centre_circle)

        total = sum(valores)
        idx_max = valores.index(max(valores))
        porcentaje = round((valores[idx_max] / total) * 100)
        ax.text(0, 0, f"{etiquetas[idx_max]}\n{porcentaje}%", ha='center', va='center',
                fontsize=14, fontweight='bold')

        ax.axis('equal')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        volver_frame = tk.Frame(self.root, bg="#fdf6f0")
        volver_frame.pack(side="bottom", anchor="e", padx=10, pady=10)

        tk.Button(volver_frame, text="Inicio", command=self.reiniciar,
                  font=("Helvetica", 10), bg="#cfd8dc", fg="#333", width=10).pack()

    def reiniciar(self):
        self.pregunta_actual = 0
        self.respuestas_usuario = []
        self.mostrar_pantalla_inicio()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        fondo_label = tk.Label(self.root, image=self.fondo_tk)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroTypeApp(root)
    root.mainloop()

