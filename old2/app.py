
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
import json
import time
import threading
from decimal import Decimal, ROUND_DOWN
from collections import OrderedDict
from datetime import datetime

from logutil import Log
from client import StoryTimeClient

THREADS_FILE = "data/threads.json"
BALANCE_FILE = "data/balance.json"

class StoryTimeApp:
    def __init__(self, root, log):
        self.root = root
        self.log = log
        self.root.title("StoryTime")
        self.root.geometry("700x550")

        self.thread_var = tk.StringVar()
        self.assistant_var = tk.StringVar()
        self.balance_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self.client = StoryTimeClient(self.log, self)

        self.current_balance = Decimal("0.0")
        self.threads = {}
        self.active_thread_name = None
        self.assistant_id = None
        self.assistants_list = []

        self.build_top_bar()
        self.build_chat_area()
        self.build_input_section()

        self.load_balance()
        self.update_balance_display()
        self.load_threads()
        self.update_thread_menu()
        self.fetch_assistants()

        if not self.client.is_ready():
            self.status_var.set("Error: No API key found.")

        self.root.protocol("WM_DELETE_WINDOW", lambda: (self.save_balance_final(), self.root.destroy()))

    def set_status(self, message):
        self.status_var.set(message)

    def set_balance(self):
        result = simpledialog.askstring("Set Balance", "Enter current balance (e.g., 10.00):")
        if result:
            try:
                self.current_balance = Decimal(result)
                self.save_balance_final()
                self.update_balance_display()
                self.status_var.set(f"Balance set to ${self.current_balance:.2f}")
            except:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def build_top_bar(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X)

        self.assistant_var.set("Select Assistant")
        self.assistant_menu = tk.OptionMenu(top_frame, self.assistant_var, ())
        self.assistant_menu.pack(side=tk.LEFT)

        self.thread_var.set("Select Thread")
        self.thread_menu = tk.OptionMenu(top_frame, self.thread_var, ())
        self.thread_menu.pack(side=tk.LEFT)

        tk.Button(top_frame, text="New Thread", command=self.new_thread_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Rename", command=self.rename_thread).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Set Balance", command=self.set_balance).pack(side=tk.LEFT, padx=5)

        self.balance_label = tk.Label(top_frame, textvariable=self.balance_var, anchor="e", font=("TkDefaultFont", 10, "bold"))
        self.balance_label.pack(side=tk.RIGHT, padx=10)

    def build_chat_area(self):
        self.chat_display = tk.Text(self.root, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(expand=True, fill=tk.BOTH)
        self.chat_display.tag_config("meta", foreground="blue", font=("TkDefaultFont", 10, "italic"))
        self.chat_display.tag_config("normal", foreground="black")

    def build_input_section(self):
        self.entry = tk.Text(self.root, height=4)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Control-Return>", self.send_input)
        tk.Button(self.root, text="Send", command=self.send_input).pack()

        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def load_balance(self):
        self.current_balance = Decimal("0.0")
        if not os.path.exists(BALANCE_FILE):
            return
        try:
            with open(BALANCE_FILE, "r") as f:
                for line in f:
                    obj = json.loads(line.strip().replace(";", ","))
                    if obj.get("action") == "set balance":
                        self.current_balance = Decimal(obj["value"])
                    elif obj.get("action") == "spent":
                        self.current_balance -= Decimal(obj["value"])
        except Exception as e:
            print(f"Failed to load balance file: {e}")

    def save_balance_final(self):
        try:
            with open(BALANCE_FILE, "w") as f:
                entry = OrderedDict([("action", "set balance"), ("value", f"{self.current_balance:.5f}")])
                json.dump(entry, f)
                f.write("\n")
        except Exception as e:
            print(f"Failed to write balance file: {e}")

    def update_balance_display(self):
        rounded = self.current_balance.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        self.balance_var.set(f"Virtual Balance: ${rounded}")
        self.balance_label.config(fg="red" if self.current_balance < 1 else "black")

    def new_thread_dialog(self):
        base = "Story "
        n = 1
        while f"{base}{n}" in self.threads:
            n += 1
        default_name = f"{base}{n}"
        name = simpledialog.askstring("New Thread", "Enter thread name:", initialvalue=default_name)
        if not name or name in self.threads:
            return
        seed_path = filedialog.askopenfilename(title="Optional seed file", filetypes=[("JSON Lines", "*.seed")])
        thread = self.client.create_thread()
        self.threads[name] = {"thread_id": thread.id, "created": datetime.utcnow().isoformat(), "seed_file": seed_path or None}
        self.save_threads()
        self.select_thread(name)
        self.update_thread_menu()
        if seed_path:
            self.upload_seed_background(thread.id, seed_path)

    def rename_thread(self):
        if not self.active_thread_name:
            return
        new_name = simpledialog.askstring("Rename Thread", "Enter new name:", initialvalue=self.active_thread_name)
        if not new_name or new_name in self.threads:
            return
        self.threads[new_name] = self.threads.pop(self.active_thread_name)
        self.save_threads()
        self.select_thread(new_name)
        self.update_thread_menu()

    def fetch_assistants(self):
        try:
            assistants = self.client.list_assistants()
            self.assistants_list = assistants.data
            self.assistant_menu['menu'].delete(0, 'end')
            for a in self.assistants_list:
                self.assistant_menu['menu'].add_command(
                    label=f"{a.name} ({a.id[:8]})",
                    command=lambda name=a.name, aid=a.id: self.select_assistant(name, aid)
                )
            self.assistant_var.set("Select Assistant")
        except Exception:
            pass

    def select_assistant(self, name, aid):
        self.assistant_id = aid
        self.assistant_var.set(name)
        self.status_var.set(f"Assistant selected: {name} ({aid[:8]})")

    def load_threads(self):
        if os.path.exists(THREADS_FILE):
            with open(THREADS_FILE, "r") as f:
                self.threads = json.load(f)

    def save_threads(self):
        with open(THREADS_FILE, "w") as f:
            json.dump(self.threads, f, indent=2)

    def update_thread_menu(self):
        self.thread_menu['menu'].delete(0, 'end')
        for name in self.threads:
            self.thread_menu['menu'].add_command(label=name, command=lambda n=name: self.select_thread(n))
        self.thread_var.set(self.active_thread_name or "Select Thread")

    def select_thread(self, name):
        self.active_thread_name = name
        self.thread_var.set(name)
        self.status_var.set(f"Active Thread: {name}")

    def upload_seed_background(self, thread_id, seed_path):
        def upload():
            try:
                with open(seed_path, "r") as f:
                    lines = f.readlines()
                total = len(lines)
                for i, line in enumerate(lines):
                    msg = json.loads(line.strip())
                    self.client.create_message(thread_id, msg['role'], msg['content'])
                    if i % 10 == 0:
                        percent = int((i / total) * 100)
                        self.status_var.set(f"Seeding: {percent}%")
                self.status_var.set("Seed upload complete.")
            except Exception as e:
                self.status_var.set(f"Seed error: {e}")
        threading.Thread(target=upload, daemon=True).start()

    def send_input(self, event=None):
        user_input = self.entry.get("1.0", tk.END).strip()
        if not user_input or not self.active_thread_name or not self.assistant_id:
            self.status_var.set("Input empty, no thread, or assistant not selected.")
            return
        self.entry.delete("1.0", tk.END)
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You: {user_input}\n", "normal")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        thread_id = self.threads[self.active_thread_name]['thread_id']
        self.client.create_message(thread_id, "user", user_input)
        run = self.client.run_thread(thread_id, self.assistant_id)

        while True:
            time.sleep(1)
            run = self.client.get_run_status(thread_id, run.id)
            if run.status in ["completed", "failed", "cancelled"]:
                break

        if run.status != "completed":
            self.status_var.set(f"Error: Run {run.status}")
            return

        messages = self.client.get_messages(thread_id)
        reply = messages.data[0].content[0].text.value.strip()
        self.chat_display.config(state=tk.NORMAL)
        if reply.startswith("meta-reply:"):
            self.chat_display.insert(tk.END, reply + "\n\n", "meta")
        else:
            self.chat_display.insert(tk.END, "Narrator: " + reply + "\n\n", "normal")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        self.status_var.set("Response received.")
