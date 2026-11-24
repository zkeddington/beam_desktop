"""Tkinter beam analysis screening tool. Imperial units throughout."""
import json
import csv
import math
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk, messagebox

PINE, RED, GOLD, PAPER, INK = "#173d2b", "#a23d48", "#a47719", "#fffdf6", "#1d3024"


def analyze(span_ft, support, points, distributed, E_ksi, Ix_in4, S_in3):
    """Loads are downward-positive kip, kip/ft and feet; returns sampled responses."""
    L = span_ft * 12
    pts = [(p, a * 12) for p, a in points]
    dls = [(q / 12, a * 12, b * 12) for q, a, b in distributed]
    total = sum(p for p, _ in pts) + sum(q * (b-a) for q, a, b in dls)
    load_moment = sum(p*a for p, a in pts) + sum(q*(b*b-a*a)/2 for q,a,b in dls)
    rr = load_moment/L if support == "Simply supported" else 0
    rl = total-rr if support == "Simply supported" else total
    c = 0 if support == "Simply supported" else -load_moment
    def moment(x):
        val = c + rl*x
        for p,a in pts: val -= p*max(x-a, 0)
        for q,a,b in dls: val -= q*(max(x-a,0)**2-max(x-b,0)**2)/2
        return val
    def integ(x):
        val = c*x*x/2 + rl*x**3/6
        for p,a in pts: val -= p*max(x-a,0)**3/6
        for q,a,b in dls: val -= q*(max(x-a,0)**4-max(x-b,0)**4)/24
        return val
    EI=E_ksi*Ix_in4
    slope=integ(L)/(EI*L) if support == "Simply supported" else 0
    samples=[]
    for i in range(501):
        x=L*i/500
        v=rl-sum(p for p,a in pts if x>=a)-sum(q*max(0,min(x,b)-a) for q,a,b in dls)
        m=moment(x); y=-integ(x)/EI+slope*x
        samples.append((x/12,v,m,y))
    return dict(left=rl,right=rr,fixed_moment=load_moment/12,total=total,samples=samples,
                maxV=max(samples,key=lambda z:abs(z[1])),maxM=max(samples,key=lambda z:abs(z[2])),
                maxY=max(samples,key=lambda z:abs(z[3])))


class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Beam Designer · Preliminary Screening"); self.geometry("1280x900"); self.configure(bg="#f5f2e7")
        menu=tk.Menu(self); file_menu=tk.Menu(menu,tearoff=False); file_menu.add_command(label="Save",command=self.save_design); file_menu.add_command(label="Open",command=self.open_design); menu.add_cascade(label="File",menu=file_menu); self.config(menu=menu)
        style=ttk.Style(self); style.theme_use("clam"); style.configure("TFrame",background="#f5f2e7"); style.configure("TLabel",background="#f5f2e7",foreground=INK); style.configure("TLabelframe",background=PAPER); style.configure("TLabelframe.Label",background=PAPER,foreground=PINE,font=("Segoe UI",10,"bold"))
        head=tk.Label(self,text="❄  BEAM DESIGNER     |     PRELIMINARY SCREENING",bg=PINE,fg="#f0d48a",font=("Segoe UI",16,"bold"),pady=14); head.pack(fill="x")
        outer=ttk.Frame(self,padding=12); outer.pack(fill="both",expand=True)
        self.left=ttk.Frame(outer); self.left.pack(side="left",fill="y",padx=(0,12))
        self.right=ttk.Frame(outer); self.right.pack(side="left",fill="both",expand=True)
        self.vars={}
        self.field("Span (ft)","span","20"); self.combo("Support","support",["Simply supported","Cantilever"])
        self.combo("Material","material",["Steel W-shape","Lumber"])
        self.combo("W-shape","section",["W12x26","W8x10","W10x22","W14x30","W16x36","W18x40","W21x44","W24x55"])
        for label,key,value in [("Depth d (in)","d","12.22"),("Flange width bf (in)","bf","6.49"),("Web thickness tw (in)","tw","0.23"),("Flange thickness tf (in)","tf","0.38"),("Weight (lb/ft)","weight","26"),("E (ksi)","E","29000"),("Ix (in⁴)","Ix","204"),("Sx (in³)","Sx","33.4"),("Fy (ksi)","Fy","50"),("Allowable Fb (ksi, optional)","allow",""),("Property source","source","Example values—verify")]: self.field(label,key,value)
        self.field("Point loads kip downward: value@ft (comma separated)","points","")
        self.field("Uniform loads kip/ft: value@start-end ft (comma separated)","udl","1@0-20")
        self.field("Deflection limit L/n","limit","360")
        self.vars["selfwt"]=tk.BooleanVar(value=False); ttk.Checkbutton(self.left,text="Include member self-weight",variable=self.vars["selfwt"]).pack(anchor="w",pady=3)
        ttk.Button(self.left,text="Analyze beam",command=self.run).pack(fill="x",pady=5); ttk.Button(self.left,text="Load example",command=self.example).pack(fill="x")
        self.result=ttk.Label(self.right,text="",justify="left",wraplength=750); self.result.pack(fill="x",pady=6)
        ttk.Button(self.right,text="Export results to CSV",command=self.export_results).pack(anchor="e",pady=(0,5))
        self.canvas=tk.Canvas(self.right,bg=PAPER,highlightthickness=0); self.canvas.pack(fill="both",expand=True); self.canvas.bind("<Configure>",lambda e:self.run())
        self.run()

    def field(self,label,key,value):
        row=ttk.Frame(self.left); row.pack(fill="x",pady=2); ttk.Label(row,text=label,width=37).pack(side="left"); v=tk.StringVar(value=value); self.vars[key]=v; ttk.Entry(row,textvariable=v,width=18).pack(side="right")
    def combo(self,label,key,values):
        row=ttk.Frame(self.left); row.pack(fill="x",pady=3); ttk.Label(row,text=label,width=37).pack(side="left"); v=tk.StringVar(value=values[0]); self.vars[key]=v; ttk.Combobox(row,textvariable=v,values=values,state="readonly",width=16).pack(side="right")
    def example(self):
        for k,v in dict(span="20",support="Simply supported",material="Steel W-shape",section="W12x26",d="12.22",bf="6.49",tw="0.23",tf="0.38",weight="26",E="29000",Ix="204",Sx="33.4",Fy="50",allow="",source="Example values—verify",points="",udl="1@0-20",limit="360").items(): self.vars[k].set(v)
        self.run()
    def save_design(self):
        path=filedialog.asksaveasfilename(defaultextension=".beam.json",filetypes=[("Beam design","*.beam.json"),("JSON files","*.json")])
        if not path: return
        keys=("span","support","material","section","d","bf","tw","tf","weight","E","Ix","Sx","Fy","allow","source","points","udl","limit")
        data={k:self.vars[k].get() for k in keys}; data["selfwt"]=bool(self.vars["selfwt"].get())
        try:
            with open(path,"w",encoding="utf-8") as f: json.dump(data,f,indent=2)
        except OSError as exc: messagebox.showerror("Save design",str(exc),parent=self)
    def open_design(self):
        path=filedialog.askopenfilename(filetypes=[("Beam design","*.beam.json *.json"),("All files","*.*")])
        if not path: return
        try:
            with open(path,encoding="utf-8") as f: data=json.load(f)
            for k,v in data.items():
                if k in self.vars and k!="selfwt": self.vars[k].set(str(v))
            if "selfwt" in data: self.vars["selfwt"].set(bool(data["selfwt"]))
            self.run()
        except (OSError,ValueError,TypeError) as exc: messagebox.showerror("Open design",str(exc),parent=self)
    def run(self):
        try:
            span=float(self.vars['span'].get()); E=float(self.vars['E'].get()); I=float(self.vars['Ix'].get()); S=float(self.vars['Sx'].get());
            if min(span,E,I,S)<=0: raise ValueError("Span and member properties must be positive.")
            pts=[]
            for item in filter(None,self.vars['points'].get().split(',')):
                p,a= item.split('@'); pts.append((float(p),float(a)))
            dls=[]
            for item in filter(None,self.vars['udl'].get().split(',')):
                q,ends=item.split('@'); a,b=ends.split('-'); dls.append((float(q),float(a),float(b)))
            if self.vars['selfwt'].get(): dls.append((float(self.vars['weight'].get())/1000,0,span))
            if any(a<0 or a>span or b<0 or b>span or b<=a for q,a,b in dls) or any(a<0 or a>span for p,a in pts): raise ValueError("Load locations must lie within the span.")
            out=analyze(span,self.vars['support'].get(),pts,dls,E,I,S); out['points']=pts; out['distributed']=dls; stress=abs(out['maxM'][2]/S)
            self.current_results=out
            allow=self.vars['allow'].get().strip(); lim=span*12/float(self.vars['limit'].get()); dy=abs(out['maxY'][3])
            self.result.config(text=f"Reactions: {out['left']:.3f} kip left; {out['right']:.3f} kip right   |   Max |M| {abs(out['maxM'][2])/12:.3f} kip-ft @ {out['maxM'][0]:.2f} ft   |   Max |fb| {stress:.3f} ksi   |   Max |δ| {dy:.3f} in\nBending: {'NOT CHECKED' if not allow else ('PASS' if stress<=float(allow) else 'FAIL')}    Deflection: {'PASS' if dy<=lim else 'FAIL'} (L/{self.vars['limit'].get()})\nEducational screening only. No shear-strength, buckling, bracing, bearing, connection, or code load-combination checks. Source: {self.vars['source'].get()}")
            self.draw(out,span)
        except Exception as e:
            self.result.config(text=f"Input error: {e}")

    def export_results(self):
        if not hasattr(self,"current_results"):
            messagebox.showerror("Export results","Analyze a valid beam before exporting.",parent=self); return
        path=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV file","*.csv")])
        if not path: return
        try:
            with open(path,"w",newline="",encoding="utf-8-sig") as f:
                writer=csv.writer(f); writer.writerow(["x (ft)","V (kip)","M (kip-ft)","Deflection (in)"])
                writer.writerows((f"{x:.6f}",f"{v:.6f}",f"{m/12:.6f}",f"{y:.6f}") for x,v,m,y in self.current_results["samples"])
        except OSError as exc: messagebox.showerror("Export results",str(exc),parent=self)

    def draw(self,o,span):
        c=self.canvas; c.delete('all'); w=max(c.winfo_width(),500); left=75; right=w-25; scale=(right-left)/span; y=45
        c.create_text(12,10,text="❄",fill=RED); c.create_line(left,y,right,y,width=5,fill=PINE)
        if self.vars['support'].get()=="Simply supported":
            for x in (left,right): c.create_polygon(x,y+2,x-10,y+22,x+10,y+22,fill=GOLD)
        else: c.create_rectangle(left-8,y-20,left,y+22,fill=PINE)
        for i in range(11):
            x=left+(right-left)*i/10;c.create_line(x,y+30,x,y+34,fill=INK);c.create_text(x,y+44,text=f"{span*i/10:g}",font=("Segoe UI",8))
        for q,a,b in o.get('distributed',[]):
            xa=left+scale*a; xb=left+scale*b; top=y-34
            c.create_line(xa,top,xb,top,fill=RED,width=2)
            for xx in [xa+(xb-xa)*i/12 for i in range(13)]: c.create_line(xx,top+2,xx,y-5,fill=RED,arrow=tk.LAST)
            c.create_text((xa+xb)/2,top-9,text=f"{q*12:g} kip/ft",fill=RED,font=("Segoe UI",9))
        for p,a in o.get('points',[]):
            xx=left+scale*a;c.create_line(xx,y-37,xx,y-5,fill=RED,width=2,arrow=tk.LAST)
            c.create_text(xx,y-45,text=f"{p:g} kip",fill=RED)
        c.create_text((left+right)/2,y+61,text="Beam position (ft)",fill=PINE)
        for name,idx,color,unit in [("Shear (kip)",1,PINE,1),("Moment (kip-ft)",2,RED,1/12),("Deflection (in)",3,GOLD,1)]:
            vals=[s[idx]*unit for s in o['samples']]; peak=max(max(abs(v) for v in vals),.01)
            y0=145+[0,130,260][["Shear (kip)","Moment (kip-ft)","Deflection (in)"].index(name)]; baseline=y0+35
            c.create_text(left,y0,text=name,anchor="w",fill=color,font=("Segoe UI",10,"bold")); c.create_line(left,baseline,right,baseline,fill="#abb5a9",dash=(3,3))
            coords=[]
            for x,v in zip((left+(right-left)*s[0]/span for s in o['samples']),vals): coords.extend([x,baseline-v/peak*38])
            c.create_line(*coords,fill=color,width=2)
            # fixed diagram bands
            if name.startswith("Shear"): pass
        # Cross-section uses one scale for every entered dimension.
        x0=w-130; cy=c.winfo_height()-115; depth=max(float(self.vars['d'].get()),.1); width=max(float(self.vars['bf'].get()),.1); fac=90/max(depth,width)
        xl=x0-width*fac/2; xr=x0+width*fac/2; yt=cy-depth*fac/2; yb=cy+depth*fac/2
        c.create_text(x0,yt-17,text="Section (scaled)",fill=PINE)
        if self.vars['material'].get()=="Steel W-shape":
            tw=float(self.vars['tw'].get())*fac; tf=float(self.vars['tf'].get())*fac
            c.create_polygon(xl,yt,xr,yt,xr,yt+tf,x0+tw/2,yt+tf,x0+tw/2,yb-tf,xr,yb-tf,xr,yb,xl,yb,xl,yb-tf,x0-tw/2,yb-tf,x0-tw/2,yt+tf,xl,yt+tf,fill="#dce8dc",outline=RED,width=2)
        else: c.create_rectangle(xl,yt,xr,yb,fill="#dce8dc",outline=RED,width=2)
        c.create_text(xr+5,cy,text=f"d={depth:g} in",anchor="w",font=("Segoe UI",8))


if __name__ == "__main__":
    App().mainloop()
