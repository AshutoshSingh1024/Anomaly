import tkinter as tk

class TerminalView(tk.Frame):
    def __init__(self,parent,on_command):
        super().__init__(parent,bd=1,relief="sunken")
        self.on_command=on_command
        self.output=tk.Text(self,height=12,wrap="word",bg="#111111",fg="#dddddd",
                            insertbackground="#ffffff",font=("Consolas",10),state="disabled")
        self.output.pack(fill="both",expand=True,padx=6,pady=(6,3))
        bottom=tk.Frame(self); bottom.pack(fill="x",padx=6,pady=(3,6))
        tk.Label(bottom,text=">",font=("Consolas",11,"bold")).pack(side="left",padx=(0,6))
        self.entry=tk.Entry(bottom,font=("Consolas",11)); self.entry.pack(side="left",fill="x",expand=True)
        self.entry.bind("<Return>",self.submit); self.entry.focus_set()
    def submit(self,_=None):
        text=self.entry.get().strip()
        if text: self.entry.delete(0,"end"); self.on_command(text)
        return "break"
    def refresh(self,text):
        self.output.config(state="normal"); self.output.delete("1.0","end")
        self.output.insert("end",text); self.output.see("end"); self.output.config(state="disabled")
