import customtkinter as ctk
import threading
import subprocess
import sys
import os

# Appearance Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SniperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("Sniper Trading Hub v1.0")
        self.geometry("600x700")
        self.process = None  # To store the running trading process

        # --- HEADER ---
        self.label = ctk.CTkLabel(self, text="OLYMP TRADE SNIPER", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        # --- INPUTS ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        # Trade Limit Field
        ctk.CTkLabel(self.input_frame, text="Trade Limit:", font=("Roboto", 14)).grid(row=0, column=0, padx=20, pady=15)
        self.trades_entry = ctk.CTkEntry(self.input_frame, width=100)
        self.trades_entry.insert(0, "10")
        self.trades_entry.grid(row=0, column=1, padx=20)

        # Stop Loss Field
        ctk.CTkLabel(self.input_frame, text="Stop Loss (Max Losses):", font=("Roboto", 14)).grid(row=1, column=0, padx=20, pady=15)
        self.sl_entry = ctk.CTkEntry(self.input_frame, width=100)
        self.sl_entry.insert(0, "3")
        self.sl_entry.grid(row=1, column=1, padx=20)

        # --- ACTION BUTTONS ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(self.button_frame, text="START ENGINE", height=40, width=140,
                                       font=("Roboto", 15, "bold"), fg_color="#1f538d", command=self.launch_bot)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = ctk.CTkButton(self.button_frame, text="STOP ENGINE", height=40, width=140,
                                      font=("Roboto", 15, "bold"), fg_color="#942727", state="disabled", command=self.stop_bot)
        self.stop_btn.grid(row=0, column=1, padx=10)

        # --- ACTIVITY LOG ---
        self.console_label = ctk.CTkLabel(self, text="Activity Log:", font=("Roboto", 12))
        self.console_label.pack(anchor="w", padx=25)

        self.console = ctk.CTkTextbox(self, height=300, fg_color="#121212", text_color="#00FF41", font=("Consolas", 12))
        self.console.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    def log(self, text):
        """Adds text to the app's console"""
        self.console.insert("end", text)
        self.console.see("end")

    def stop_bot(self):
        """Terminates the running trading process and all child processes (Browser)"""
        if self.process:
            try:
                # /F = Force | /T = Terminate child processes (Chrome)
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(self.process.pid)],
                               capture_output=True, creationflags=0x08000000)
                self.log("\n[SYSTEM] Stopping Engine... Cleaning up resources.\n")
            except Exception as e:
                self.log(f"\n[ERROR] Could not stop process: {e}\n")

    def launch_bot(self):
        """Starts the bot in a separate thread to keep the UI responsive"""
        self.start_btn.configure(state="disabled", text="RUNNING...")
        self.stop_btn.configure(state="normal")
        self.console.delete("1.0", "end")
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        trades = self.trades_entry.get()
        sl = self.sl_entry.get()
        create_no_window = 0x08000000

        # Environment detection
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
            main_path = os.path.join(base_path, "main.py")
            command = ["python", main_path, trades, sl]
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(current_dir, "main.py")
            command = [sys.executable, main_path, trades, sl]

        self.log(f"--- Launching Engine (Limits: {trades}T, {sl}SL) ---\n")

        try:
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding="utf-8",
                shell=False,
                creationflags=create_no_window
            )

            if self.process.stdout:
                for line in self.process.stdout:
                    self.log(line)

            self.process.wait()
        except Exception as e:
            self.log(f"\n[SYSTEM ERROR]: {str(e)}\n")

        self.log("\n--- Process Finished ---\n")
        self.start_btn.configure(state="normal", text="START ENGINE")
        self.stop_btn.configure(state="disabled")
        self.process = None

if __name__ == "__main__":
    app = SniperApp()
    app.mainloop()