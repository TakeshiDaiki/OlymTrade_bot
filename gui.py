import customtkinter as ctk
import threading
import subprocess
import sys
import os

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SniperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la Ventana
        self.title("Sniper Trading Hub v1.0")
        self.geometry("600x650")

        # --- HEADER ---
        self.label = ctk.CTkLabel(self, text="OLYMP TRADE SNIPER", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        # --- INPUTS ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        # Campo para Trades
        ctk.CTkLabel(self.input_frame, text="Límite de Operaciones:", font=("Roboto", 14)).grid(row=0, column=0,
                                                                                                padx=20, pady=15)
        self.trades_entry = ctk.CTkEntry(self.input_frame, width=100)
        self.trades_entry.insert(0, "10")
        self.trades_entry.grid(row=0, column=1, padx=20)

        # Campo para Stop Loss
        ctk.CTkLabel(self.input_frame, text="Stop Loss (Máx. Pérdidas):", font=("Roboto", 14)).grid(row=1, column=0,
                                                                                                    padx=20, pady=15)
        self.sl_entry = ctk.CTkEntry(self.input_frame, width=100)
        self.sl_entry.insert(0, "3")
        self.sl_entry.grid(row=1, column=1, padx=20)

        # --- BOTÓN DE ACCIÓN ---
        self.start_btn = ctk.CTkButton(self, text="START ENGINE", height=40, font=("Roboto", 16, "bold"),
                                       command=self.launch_bot)
        self.start_btn.pack(pady=20)

        # --- CONSOLA DE LOGS ---
        self.console_label = ctk.CTkLabel(self, text="Activity Log:", font=("Roboto", 12))
        self.console_label.pack(anchor="w", padx=25)

        self.console = ctk.CTkTextbox(self, height=300, fg_color="#121212", text_color="#00FF41", font=("Consolas", 12))
        self.console.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    def log(self, text):
        """Añade texto a la consola de la app"""
        self.console.insert("end", text)
        self.console.see("end")

    def launch_bot(self):
        """Inicia el bot en un hilo separado para no congelar la ventana"""
        self.start_btn.configure(state="disabled", text="SNIPER RUNNING...")
        self.console.delete("1.0", "end")
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        trades = self.trades_entry.get()
        sl = self.sl_entry.get()

        # Obtener ruta absoluta de main.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(current_dir, "main.py")

        self.log(f"--- Launching Engine (Limits: {trades}T, {sl}SL) ---\n")

        try:
            # Ejecutar con UTF-8 para evitar errores de emojis en Windows
            process = subprocess.Popen(
                [sys.executable, main_path, trades, sl],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding="utf-8"  # <--- Vital para los emojis
            )

            # Leer salida en tiempo real
            if process.stdout:
                for line in process.stdout:
                    self.log(line)

            process.wait()
        except Exception as e:
            self.log(f"\n[SYSTEM ERROR]: {str(e)}\n")

        self.log("\n--- Process Finished ---\n")
        self.start_btn.configure(state="normal", text="START ENGINE")


if __name__ == "__main__":
    app = SniperApp()
    app.mainloop()