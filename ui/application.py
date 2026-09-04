import tkinter as tk
from tkinter import messagebox
from game.controller import GameController
from ui.world_view import WorldView
from ui.terminal_view import TerminalView

class AnomalyApp:
    def __init__(self):
        self.controller=GameController()
        self.root=tk.Tk()
        self.root.title("Anomaly")
        self.root.geometry("1100x700")
        self.root.minsize(850,550)
        main=tk.Frame(self.root); main.pack(fill="both",expand=True)
        self.world=WorldView(main,self.controller); self.world.pack(fill="both",expand=True,padx=8,pady=(8,4))
        self.terminal=TerminalView(main,self.command); self.terminal.pack(fill="both",expand=True,padx=8,pady=(4,8))
        self.refresh()
        self.root.protocol("WM_DELETE_WINDOW",self.close)
    def command(self,text):
        result=self.controller.execute(text)
        self.terminal.refresh(self.controller.transcript()); self.world.refresh()
        if result.quit_requested: self.root.after(50,self.root.destroy)
    def refresh(self):
        self.terminal.refresh(self.controller.transcript()); self.world.refresh()
    def close(self):
        if messagebox.askyesno("Anomaly","Exit the game?"): self.root.destroy()
    def run(self): self.root.mainloop()
