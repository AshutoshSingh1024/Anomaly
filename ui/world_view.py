import tkinter as tk

class WorldView(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bd=1,relief="sunken",bg="#202020")
        self.controller=controller
        self.canvas=tk.Canvas(self,bg="#202020",highlightthickness=0); self.canvas.pack(fill="both",expand=True)
        self.canvas.bind("<Configure>",self.draw)
    def refresh(self): self.draw()
    def draw(self,_=None):
        c=self.canvas; c.delete("all"); s=self.controller.state; w=s.world; p=s.player
        W=max(c.winfo_width(),400); H=max(c.winfo_height(),250)
        c.create_text(18,16,anchor="nw",text=f"ANOMALY    {s.clock.display()}",fill="#eeeeee",font=("Consolas",12,"bold"))
        cell=max(min((W-80)/w.width,(H-70)/w.height),22)
        cx,cy=W/2,H/2+15; minx,miny=-(w.width//2),-(w.height//2)
        def pos(x,y): return cx+(x-minx+0.5-w.width/2)*cell,cy+(y-miny+0.5-w.height/2)*cell
        for i in range(w.width+1):
            x=cx+(i-w.width/2)*cell
            c.create_line(x,cy-w.height*cell/2,x,cy+w.height*cell/2,fill="#303030")
        for i in range(w.height+1):
            y=cy+(i-w.height/2)*cell
            c.create_line(cx-w.width*cell/2,y,cx+w.width*cell/2,y,fill="#303030")
        ry=pos(0,0)[1]
        c.create_line(cx-w.width*cell/2,ry,cx+w.width*cell/2,ry,fill="#514b42",width=max(4,int(cell*.18)))
        for l in w.locations.values():
            x,y=pos(l.x,l.y); c.create_text(x,y-cell*.42,text=l.name,fill="#888888",font=("Consolas",8))
        symbols={"house":"H","tree":"T","well":"W","bread":"B"}
        for o in w.objects.values():
            if o.hidden: continue
            x,y=pos(o.x,o.y); r=max(6,cell*.25)
            c.create_oval(x-r,y-r,x+r,y+r,outline="#aaaaaa")
            c.create_text(x,y,text=symbols.get(o.object_id,"?"),fill="#dddddd",font=("Consolas",max(8,int(cell*.25)),"bold"))
            c.create_text(x,y+r+5,text=o.name,fill="#999999",font=("Consolas",8))
        for n in w.npcs.values():
            if not n.alive: continue
            x,y=pos(n.x,n.y); r=max(7,cell*.27)
            c.create_oval(x-r,y-r,x+r,y+r,outline="#bbbbbb",width=2)
            c.create_text(x,y,text="@",fill="#eeeeee",font=("Consolas",max(9,int(cell*.3)),"bold"))
            c.create_text(x,y+r+6,text=n.name,fill="#bbbbbb",font=("Consolas",8))
        x,y=pos(p.x,p.y); r=max(9,cell*.31)
        c.create_oval(x-r,y-r,x+r,y+r,outline="#ffffff",width=2)
        c.create_text(x,y,text="P",fill="#ffffff",font=("Consolas",max(10,int(cell*.34)),"bold"))
        inv=", ".join(p.inventory) if p.inventory else "empty"
        c.create_text(18,H-18,anchor="sw",text=f"Position: ({p.x}, {p.y})    Inventory: {inv}",fill="#aaaaaa",font=("Consolas",9))
