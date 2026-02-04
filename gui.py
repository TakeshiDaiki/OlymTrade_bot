import customtkinter as ctk
import threading
import subprocess
import sys
import os
import multiprocessing

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SniperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OLYMP TRADE SNIPER")
        self.geometry("600x600")  # Un poco más grande
        self.resizable(False, False)
        self.process = None

        # --- HEADER ---
        self.label = ctk.CTkLabel(self, text="SNIPER ENGINE v1.0", font=("Roboto", 24, "bold"))
        self.label.pack(pady=(20, 10))

        # --- CENTERED INPUTS ---
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=10)

        ctk.CTkLabel(self.input_frame, text="Trades:", font=("Roboto", 14)).grid(row=0, column=0, padx=10, pady=5)
        self.trades_entry = ctk.CTkEntry(self.input_frame, width=80, height=35, font=("Roboto", 14), justify="center")
        self.trades_entry.insert(0, "10")
        self.trades_entry.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(self.input_frame, text="SL:", font=("Roboto", 14)).grid(row=0, column=2, padx=10, pady=5)
        self.sl_entry = ctk.CTkEntry(self.input_frame, width=80, height=35, font=("Roboto", 14), justify="center")
        self.sl_entry.insert(0, "3")
        self.sl_entry.grid(row=0, column=3, padx=10)

        # --- BUTTONS ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="START ENGINE", width=160, height=40,
                                       font=("Roboto", 14, "bold"), command=self.launch_bot)
        self.start_btn.grid(row=0, column=0, padx=15)

        self.stop_btn = ctk.CTkButton(self.btn_frame, text="STOP ENGINE", width=160, height=40,
                                      font=("Roboto", 14, "bold"), command=self.stop_bot,
                                      fg_color="#942727", state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=15)

        # --- CONSOLE ---
        self.console = ctk.CTkTextbox(self, height=300, fg_color="#000000", text_color="#00FF41",
                                      font=("Consolas", 12), border_width=1, wrap="none")
        self.console.pack(padx=20, pady=10, fill="both", expand=True)
        self.console.configure(state="disabled")

    def log(self, text):
        """Advanced logging with overwrite support"""
        self.console.configure(state="normal")

        # If line starts with @@, we delete the previous line before printing
        if text.startswith('@@'):
            self.console.delete("end-2c linestart", "end-1c")
            text = text.replace('@@', '')

        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")

    def stop_bot(self):
        if self.process:
            try:
                # Cleaner kill
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.process.pid)],
                               capture_output=True, creationflags=0x08000000)
                self.log("\n[SYSTEM] Engine Stopped.")
            except Exception as err:
                self.log(f"\n[INFO] Shutdown info: {err}")

            self.start_btn.configure(state="normal", text="START ENGINE")
            self.stop_btn.configure(state="disabled")

    def launch_bot(self):
        self.start_btn.configure(state="disabled", text="RUNNING...")
        self.stop_btn.configure(state="normal")
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        trades, sl = self.trades_entry.get(), self.sl_entry.get()
        main_path = os.path.join(os.path.dirname(__file__), "main.py")

        if getattr(sys, 'frozen', False):
            cmd = [sys.executable, trades, sl]
        else:
            cmd = [sys.executable, "-u", main_path, trades, sl]

        try:
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            text=True, bufsize=1, universal_newlines=True,
                                            creationflags=0x08000000)
            while True:
                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break
                if line:
                    self.log(line)
        except Exception as err:
            self.log(f"Critical Error: {err}")

        self.start_btn.configure(state="normal", text="START ENGINE")
        self.stop_btn.configure(state="disabled")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    if len(sys.argv) > 1:
        from main import main as start_trading

        start_trading(max_trades=int(sys.argv[1]), max_losses=int(sys.argv[2]))
        sys.exit(0)
    app = SniperApp()
    app.mainloop()