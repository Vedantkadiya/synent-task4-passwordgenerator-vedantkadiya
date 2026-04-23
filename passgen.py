"""
Synent Technologies – Python Development Internship
Task 4: Password Generator (GUI)
Author: dev
"""

import tkinter as tk
from tkinter import messagebox
import random
import string
import re

# ── Palette ─────────────────────────────────────────────────────────────
BG       = "#0a0a0f"
PANEL    = "#10101e"
CARD     = "#13131f"
NEON_GRN = "#39ff14"
NEON_BLU = "#00d4ff"
NEON_PNK = "#ff2d78"
NEON_YLW = "#ffe600"
TEXT     = "#d0d8f0"
SUBTEXT  = "#5a6080"
# ────────────────────────────────────────────────────────────────────────


def password_strength(pwd: str) -> tuple[str, str]:
    """Returns (label, color) for strength."""
    score = 0
    if len(pwd) >= 12:  score += 1
    if len(pwd) >= 16:  score += 1
    if re.search(r"[A-Z]", pwd): score += 1
    if re.search(r"[a-z]", pwd): score += 1
    if re.search(r"\d",    pwd): score += 1
    if re.search(r"[^a-zA-Z0-9]", pwd): score += 1

    if score <= 2:  return "WEAK",   NEON_PNK
    if score <= 4:  return "FAIR",   NEON_YLW
    if score == 5:  return "STRONG", NEON_BLU
    return          "ULTRA",         NEON_GRN


def generate_password(length: int, use_upper: bool, use_lower: bool,
                      use_digits: bool, use_symbols: bool,
                      exclude_ambiguous: bool) -> str:
    pool = ""
    required = []

    if use_upper:
        chars = string.ascii_uppercase
        if exclude_ambiguous:
            chars = chars.replace("I", "").replace("O", "")
        pool += chars
        required.append(random.choice(chars))

    if use_lower:
        chars = string.ascii_lowercase
        if exclude_ambiguous:
            chars = chars.replace("l", "").replace("o", "")
        pool += chars
        required.append(random.choice(chars))

    if use_digits:
        chars = string.digits
        if exclude_ambiguous:
            chars = chars.replace("0", "").replace("1", "")
        pool += chars
        required.append(random.choice(chars))

    if use_symbols:
        chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        pool += chars
        required.append(random.choice(chars))

    if not pool:
        return ""

    remaining_len = max(0, length - len(required))
    remaining = [random.choice(pool) for _ in range(remaining_len)]
    password = required + remaining
    random.shuffle(password)
    return "".join(password)


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Synent PassGen")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        w, h = 480, 640
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────
        hdr = tk.Frame(self.root, bg=PANEL, pady=18)
        hdr.pack(fill="x")
        tk.Label(hdr, text="◈ PASSGEN", bg=PANEL, fg=NEON_GRN,
                 font=("Courier New", 22, "bold")).pack()
        tk.Label(hdr, text="Synent Technologies  •  Secure Password Generator",
                 bg=PANEL, fg=SUBTEXT,
                 font=("Courier New", 9)).pack()

        # ── Password display ──────────────────────────────────────
        disp_frame = tk.Frame(self.root, bg=CARD,
                              highlightbackground=NEON_GRN,
                              highlightthickness=1)
        disp_frame.pack(fill="x", padx=24, pady=18)

        self.pwd_var = tk.StringVar(value="Click GENERATE")
        pwd_label = tk.Label(disp_frame, textvariable=self.pwd_var,
                             bg=CARD, fg=NEON_GRN,
                             font=("Courier New", 16, "bold"),
                             wraplength=380, justify="center",
                             pady=18, padx=14)
        pwd_label.pack(fill="x")

        # Strength bar
        str_frame = tk.Frame(disp_frame, bg=CARD)
        str_frame.pack(fill="x", padx=14, pady=(0, 10))

        self.str_var  = tk.StringVar(value="")
        self.str_bar  = tk.Canvas(str_frame, bg=CARD, bd=0,
                                  highlightthickness=0,
                                  height=6, width=420)
        self.str_bar.pack()
        self.str_label = tk.Label(str_frame, textvariable=self.str_var,
                                  bg=CARD, fg=TEXT,
                                  font=("Courier New", 10))
        self.str_label.pack(pady=(4, 0))

        # Copy btn
        tk.Button(disp_frame, text="⧉ COPY",
                  bg=PANEL, fg=NEON_BLU,
                  font=("Courier New", 11, "bold"),
                  bd=0, relief="flat", padx=18, pady=6,
                  cursor="hand2",
                  command=self._copy_password).pack(pady=(0, 10))

        # ── Options ───────────────────────────────────────────────
        opt_frame = tk.Frame(self.root, bg=PANEL, padx=24, pady=16)
        opt_frame.pack(fill="x", padx=24)

        tk.Label(opt_frame, text="OPTIONS", bg=PANEL, fg=SUBTEXT,
                 font=("Courier New", 10, "bold")).pack(anchor="w")

        # Length
        len_frame = tk.Frame(opt_frame, bg=PANEL)
        len_frame.pack(fill="x", pady=(10, 6))
        tk.Label(len_frame, text="Length", bg=PANEL, fg=TEXT,
                 font=("Courier New", 12), width=14,
                 anchor="w").pack(side="left")

        self.length_var = tk.IntVar(value=16)
        len_slider = tk.Scale(
            len_frame, from_=6, to=64,
            orient="horizontal", variable=self.length_var,
            bg=PANEL, fg=NEON_GRN,
            troughcolor=CARD, highlightthickness=0,
            font=("Courier New", 10),
            length=200, showvalue=True,
            command=lambda _: self._live_generate()
        )
        len_slider.pack(side="left", padx=10)

        # Checkboxes
        self.use_upper   = tk.BooleanVar(value=True)
        self.use_lower   = tk.BooleanVar(value=True)
        self.use_digits  = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.excl_ambig  = tk.BooleanVar(value=False)

        checks = [
            ("Uppercase (A–Z)",        self.use_upper,   NEON_BLU),
            ("Lowercase (a–z)",        self.use_lower,   NEON_GRN),
            ("Digits (0–9)",           self.use_digits,  NEON_YLW),
            ("Symbols (!@#...)",       self.use_symbols, NEON_PNK),
            ("Exclude Ambiguous (0,O,l,I)", self.excl_ambig, SUBTEXT),
        ]
        for label, var, color in checks:
            cb = tk.Checkbutton(
                opt_frame, text=label, variable=var,
                bg=PANEL, fg=color,
                selectcolor=CARD, activebackground=PANEL,
                font=("Courier New", 11),
                command=self._live_generate
            )
            cb.pack(anchor="w", pady=2)

        # ── Generate Button ───────────────────────────────────────
        tk.Button(
            self.root, text="⚡ GENERATE PASSWORD",
            bg=NEON_GRN, fg=BG,
            font=("Courier New", 14, "bold"),
            bd=0, relief="flat", pady=14,
            cursor="hand2",
            command=self._generate
        ).pack(fill="x", padx=24, pady=18)

        # ── History ───────────────────────────────────────────────
        hist_lbl = tk.Label(self.root, text="Recent Passwords",
                            bg=BG, fg=SUBTEXT,
                            font=("Courier New", 10))
        hist_lbl.pack(anchor="w", padx=24)

        self.hist_frame = tk.Frame(self.root, bg=BG)
        self.hist_frame.pack(fill="x", padx=24, pady=(4, 0))
        self.history = []

        # Generate initial password
        self._generate()

    def _generate(self):
        length  = self.length_var.get()
        pwd = generate_password(
            length,
            self.use_upper.get(), self.use_lower.get(),
            self.use_digits.get(), self.use_symbols.get(),
            self.excl_ambig.get()
        )
        if not pwd:
            messagebox.showwarning("No Options",
                                   "Please select at least one character type.")
            return

        self.pwd_var.set(pwd)
        self._update_strength(pwd)
        self._add_to_history(pwd)

    def _live_generate(self):
        self._generate()

    def _update_strength(self, pwd):
        label, color = password_strength(pwd)
        self.str_var.set(f"Strength: {label}")
        self.str_label.config(fg=color)
        self.str_bar.delete("all")
        levels = {"WEAK": 0.25, "FAIR": 0.50, "STRONG": 0.75, "ULTRA": 1.0}
        ratio = levels.get(label, 0)
        self.str_bar.create_rectangle(0, 0, 420, 6, fill="#222", outline="")
        self.str_bar.create_rectangle(0, 0, int(420 * ratio), 6,
                                      fill=color, outline="")

    def _copy_password(self):
        pwd = self.pwd_var.get()
        if pwd and pwd != "Click GENERATE":
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Copied!", "Password copied to clipboard ✓")

    def _add_to_history(self, pwd):
        self.history.insert(0, pwd)
        self.history = self.history[:4]  # keep last 4

        for w in self.hist_frame.winfo_children():
            w.destroy()

        for p in self.history:
            row = tk.Frame(self.hist_frame, bg=CARD,
                           highlightbackground=SUBTEXT,
                           highlightthickness=1)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=p, bg=CARD, fg=SUBTEXT,
                     font=("Courier New", 10),
                     padx=8, pady=4).pack(side="left")
            tk.Button(
                row, text="copy", bg=CARD, fg=NEON_BLU,
                font=("Courier New", 9), bd=0, relief="flat",
                padx=6, cursor="hand2",
                command=lambda x=p: (
                    self.root.clipboard_clear(),
                    self.root.clipboard_append(x)
                )
            ).pack(side="right", padx=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
