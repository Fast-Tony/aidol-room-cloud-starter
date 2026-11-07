import tkinter as tk
from tkinter import ttk, messagebox
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import webbrowser
from client import AidolClient

BG='#080D15'; PANEL='#101827'; EDGE='#263246'; INK='#EDF2FC'; MUTED='#91A1BB'; BRAND='#3798FF'
KINDS={'Bình luận':'comment','Vào xem':'join','Theo dõi':'follow','Chia sẻ':'share','Lượt thích':'like','Quà tặng':'gift'}
class DemoApp:
 def __init__(self,root):
  self.root=root;self.client=AidolClient();self.busy=False;self.closed=False;self.pool=ThreadPoolExecutor(max_workers=1)
  root.title('Aidol Room Cloud | AI Livestream Starter');root.geometry('1380x880');root.minsize(1080,700);root.configure(bg=BG)
  s=ttk.Style();s.theme_use('clam');s.configure('.',font=('Segoe UI',10),foreground=INK,background=PANEL)
  s.configure('TEntry',padding=11,fieldbackground='#0A111D',foreground=INK,bordercolor=EDGE,insertcolor=INK)
  s.map('TEntry',fieldbackground=[('readonly','#0A111D')],foreground=[('readonly',INK)])
  s.configure('TCombobox',padding=9,fieldbackground='#0A111D',background=EDGE,foreground=INK,arrowcolor=MUTED)
  s.map('TCombobox',fieldbackground=[('readonly','#0A111D')],foreground=[('readonly',INK)],selectbackground=[('readonly','#0A111D')],selectforeground=[('readonly',INK)])
  root.option_add('*TCombobox*Listbox.background','#101827');root.option_add('*TCombobox*Listbox.foreground',INK)
  s.configure('TButton',padding=(16,10),background='#182438',foreground=INK,borderwidth=1,bordercolor=EDGE)
  s.map('TButton',background=[('active','#263952'),('disabled','#141D2B')],foreground=[('disabled','#596A84')])
  s.configure('Primary.TButton',background=BRAND,foreground='white',bordercolor=BRAND);s.map('Primary.TButton',background=[('active','#60ACFF'),('disabled','#193B61')],foreground=[('disabled','#7993AF')])
  s.configure('Vertical.TScrollbar',background='#263246',troughcolor=BG,bordercolor=BG,arrowcolor=MUTED)
  self.code=tk.StringVar();self.link=tk.StringVar();self.name=tk.StringVar(value='Khách thử nghiệm');self.kind=tk.StringVar(value='Bình luận');self.reply=tk.BooleanVar();self.status=tk.StringVar(value='Chưa kết nối phòng');self.room=tk.StringVar(value='Chưa chọn phòng');self.badge=tk.StringVar(value='●  Chưa kết nối')
  side=tk.Frame(root,bg='#070C13',width=224,highlightthickness=1,highlightbackground='#1D2838');side.pack(side='left',fill='y');side.pack_propagate(False)
  tk.Label(side,text='◈  Aidol',font=('Segoe UI',23,'bold'),fg='#74DDFF',bg='#070C13').pack(anchor='w',padx=22,pady=(26,0))
  tk.Label(side,text='AI LIVESTREAM STARTER',font=('Segoe UI',9,'bold'),fg=MUTED,bg='#070C13').pack(anchor='w',padx=25,pady=(4,28))
  tk.Label(side,text='KHÔNG GIAN LÀM VIỆC',font=('Segoe UI',8,'bold'),fg='#617792',bg='#070C13').pack(anchor='w',padx=22,pady=12)
  tk.Label(side,text='◉   Live stream AI',font=('Segoe UI',11,'bold'),fg=INK,bg='#142438',padx=18,pady=15,anchor='w').pack(fill='x',padx=10)
  tk.Label(side,text='Kết nối phòng đã thuê, gửi sự kiện và lấy link phát cho OBS.',justify='left',font=('Segoe UI',10),fg=MUTED,bg='#070C13',wraplength=177).pack(anchor='w',padx=22,pady=20)
  footer=tk.Frame(side,bg='#070C13');footer.pack(side='bottom',fill='x',padx=22,pady=24)
  tk.Label(footer,text='ROOM CLOUD API  v1.0',font=('Segoe UI',9,'bold'),fg='#6985A6',bg='#070C13').pack(anchor='w')
  tk.Label(footer,text='Ứng dụng mẫu cho nhà phát triển',font=('Segoe UI',9),fg=MUTED,bg='#070C13',wraplength=180,justify='left').pack(anchor='w',pady=(6,0))
  main=tk.Frame(root,bg=BG);main.pack(side='left',fill='both',expand=True)
  top=tk.Frame(main,bg='#0B111C',padx=24,pady=17,highlightthickness=1,highlightbackground='#1D2838');top.pack(fill='x')
  tk.Label(top,text='Trung tâm điều khiển',font=('Segoe UI',12,'bold'),fg=INK,bg='#0B111C').pack(side='left')
  tk.Label(top,textvariable=self.badge,font=('Segoe UI',10),fg='#67D8C1',bg='#0B111C').pack(side='right')
  intro=tk.Frame(main,bg=BG);intro.pack(fill='x',padx=24,pady=(22,18))
  tk.Label(intro,text='AIDOL ROOM CLOUD / DEVELOPER',font=('Segoe UI',9,'bold'),fg='#6EB6FF',bg=BG).pack(anchor='w')
  tk.Label(intro,text='Điều khiển phiên live',font=('Segoe UI',21,'bold'),fg=INK,bg=BG).pack(anchor='w',pady=(5,4))
  tk.Label(intro,text='Kết nối một lần. Gửi tương tác và nhận link Browser Source ngay tại đây.',fg=MUTED,bg=BG).pack(anchor='w')
  outer=tk.Frame(main,bg=BG);outer.pack(fill='both',expand=True,padx=24,pady=(0,20))
  cv=tk.Canvas(outer,bg=BG,highlightthickness=0);sb=ttk.Scrollbar(outer,command=cv.yview);sb.pack(side='right',fill='y');cv.pack(side='left',fill='both',expand=True);cv.configure(yscrollcommand=sb.set)
  body=tk.Frame(cv,bg=BG);win=cv.create_window((0,0),window=body,anchor='nw');body.bind('<Configure>',lambda e:cv.configure(scrollregion=cv.bbox('all')));cv.bind('<Configure>',lambda e:cv.itemconfigure(win,width=e.width));root.bind('<MouseWheel>',lambda e:cv.yview_scroll(int(-e.delta/120),'units'))
  body.columnconfigure(0,weight=3);body.columnconfigure(1,weight=2)
  left=tk.Frame(body,bg=BG);left.grid(row=0,column=0,sticky='nsew',padx=(0,16));right=tk.Frame(body,bg=BG);right.grid(row=0,column=1,sticky='nsew')
  c=self.card(left,'01  Kết nối phòng','Nhập mã ALC từ mục kết nối Router trong phòng đã thuê.')
  self.label(c,'MÃ KẾT NỐI');ttk.Entry(c,textvariable=self.code).pack(fill='x',pady=(0,12))
  self.connect=ttk.Button(c,text='Kết nối phòng',style='Primary.TButton',command=lambda:self.work('connect'));self.connect.pack(fill='x')
  tk.Label(c,textvariable=self.room,fg=MUTED,bg=PANEL,anchor='w',wraplength=460).pack(fill='x',pady=(14,0))
  c=self.card(left,'02  Gửi sự kiện','Bật live và phản hồi bình luận trong phòng trước khi gửi.')
  row=tk.Frame(c,bg=PANEL);row.pack(fill='x',pady=(12,10));row.columnconfigure(0,weight=1);row.columnconfigure(1,weight=1)
  tk.Label(row,text='Loại sự kiện',bg=PANEL,fg=MUTED).grid(row=0,column=0,sticky='w',pady=(0,6));tk.Label(row,text='Tên người xem',bg=PANEL,fg=MUTED).grid(row=0,column=1,sticky='w',padx=(12,0),pady=(0,6))
  ttk.Combobox(row,textvariable=self.kind,values=list(KINDS),state='readonly',width=14).grid(row=1,column=0,sticky='ew');ttk.Entry(row,textvariable=self.name,width=18).grid(row=1,column=1,sticky='ew',padx=(12,0))
  self.label(c,'NỘI DUNG BÌNH LUẬN')
  self.message=tk.Text(c,height=5,wrap='word',font=('Segoe UI',11),bg='#0A111D',fg=INK,insertbackground=INK,relief='flat',padx=12,pady=12,highlightthickness=1,highlightbackground=EDGE);self.message.pack(fill='x');self.message.insert('1.0','Sản phẩm này có những màu nào vậy?')
  tk.Checkbutton(c,text='Phản hồi các sự kiện tương tác',variable=self.reply,bg=PANEL,fg=MUTED,activebackground=PANEL,activeforeground=INK,selectcolor='#0A111D',anchor='w').pack(fill='x',pady=12)
  self.send=ttk.Button(c,text='Gửi sự kiện  →',style='Primary.TButton',command=lambda:self.work('send'));self.send.pack(fill='x')
  c=self.card(right,'Đầu ra phiên live','Link Browser Source tự động đồng bộ theo phòng.')
  stage=tk.Frame(c,bg='#080F1B',highlightthickness=1,highlightbackground=EDGE);stage.pack(fill='x',pady=14)
  tk.Label(stage,text='▣',font=('Segoe UI',38),fg=BRAND,bg='#080F1B').pack(pady=(20,2));tk.Label(stage,text='BROWSER SOURCE',font=('Segoe UI',10,'bold'),fg=INK,bg='#080F1B').pack();tk.Label(stage,text='Mở link để xem trực tiếp trong trình duyệt',font=('Segoe UI',9),fg=MUTED,bg='#080F1B',wraplength=285).pack(pady=(7,22))
  ttk.Entry(c,textvariable=self.link,state='readonly').pack(fill='x',pady=(0,12))
  self.copy=ttk.Button(c,text='Sao chép link OBS',style='Primary.TButton',command=self.copy_link);self.copy.pack(fill='x',pady=(0,8))
  row=tk.Frame(c,bg=PANEL);row.pack(fill='x');self.preview=ttk.Button(row,text='Mở xem ↗',command=self.open_link);self.preview.pack(side='left',fill='x',expand=True,padx=(0,8));self.check=ttk.Button(row,text='Kiểm tra',command=lambda:self.work('status'));self.check.pack(side='left',fill='x',expand=True)
  tk.Label(c,text='OBS → Sources → + → Browser → dán URL. Giữ riêng link phát của bạn.',fg=MUTED,bg=PANEL,justify='left',wraplength=310).pack(anchor='w',pady=(14,0))
  c=self.card(right,'Trạng thái & hoạt động','Theo dõi kết quả của mỗi thao tác.')
  tk.Label(c,textvariable=self.status,bg=PANEL,fg='#69CBBB',anchor='w',wraplength=310,justify='left').pack(fill='x',pady=12);self.log=tk.Text(c,height=6,font=('Segoe UI',9),bg='#0A111D',fg=MUTED,relief='flat',padx=10,pady=10,state='disabled',wrap='word');self.log.pack(fill='x')
  tk.Label(c,text='Nhận sự kiện không đồng nghĩa AI đã phát lời phản hồi.',fg=MUTED,bg=PANEL,wraplength=310,justify='left').pack(anchor='w',pady=(12,0))
  self.code.trace_add('write',lambda *a:self.refresh());self.refresh();root.protocol('WM_DELETE_WINDOW',self.close);root.after(5000,self.auto_status)
 def label(self,parent,text):
  tk.Label(parent,text=text,font=('Segoe UI',9,'bold'),bg=PANEL,fg=MUTED).pack(anchor='w',pady=(14,6))
 def card(self,parent,title,subtitle):
  border=tk.Frame(parent,bg=EDGE,padx=1,pady=1);border.pack(fill='x',pady=(0,16));box=tk.Frame(border,bg=PANEL,padx=18,pady=18);box.pack(fill='both',expand=True);tk.Label(box,text=title,font=('Segoe UI',13,'bold'),bg=PANEL,fg=INK).pack(anchor='w');tk.Label(box,text=subtitle,bg=PANEL,fg=MUTED,wraplength=350,justify='left').pack(anchor='w',pady=(5,0));return box
 def refresh(self):
  paired=bool(self.client.key and self.client.session)
  self.badge.set('Đang xử lý…' if self.busy else '●  Đã kết nối' if paired else '●  Chưa kết nối')
  for b,enabled in [(self.connect,bool(self.code.get().strip())),(self.check,paired),(self.send,paired),(self.copy,bool(self.link.get())),(self.preview,bool(self.link.get()))]:b.configure(state='normal' if enabled and not self.busy else 'disabled')
 def note(self,text):
  self.status.set(text);self.log.configure(state='normal');self.log.insert('1.0',datetime.now().strftime('%H:%M:%S')+'  '+text+chr(10));self.log.configure(state='disabled')
 def work(self,action,quiet=False):
  if self.busy:return
  text=self.message.get('1.0','end').strip()
  if action=='send' and self.kind.get()=='Bình luận' and not text:messagebox.showinfo('Thiếu nội dung','Bạn nhập nội dung bình luận trước khi gửi.');return
  self.busy=True;self.refresh();code=self.code.get().strip();kind=KINDS[self.kind.get()];name=self.name.get().strip();reply=self.reply.get()
  if not quiet:self.status.set('Đang xử lý…')
  def run():
   if action=='connect':return self.client.connect(code)
   if action=='send':return self.client.send(kind,name,text,reply=reply)
   return self.client.request('GET','/rooms/'+self.client.session)
  future=self.pool.submit(run)
  def poll():
   if self.closed:return
   if not future.done():self.root.after(100,poll);return
   try:
    result=future.result()
    if action in ('connect','status'):
     old=self.link.get();self.link.set(result.get('browser_source_url',''));self.room.set('Phòng: '+self.client.session)
     if not quiet or old!=self.link.get():self.note('Đã kết nối • Link OBS sẵn sàng.' if self.link.get() else 'Đã kết nối • Chờ link phát. Bật live trong phòng; app sẽ tự kiểm tra lại.')
    else:self.note('Đã nhận '+str(result.get('received',0))+' sự kiện • Trùng: '+str(result.get('duplicates',0))+'. Phản hồi theo cài đặt phòng.')
   except Exception as exc:
    self.link.set('');self.note(str(exc))
    if not quiet:messagebox.showerror('Không thể hoàn tất',str(exc),parent=self.root)
   finally:self.busy=False;self.refresh()
  self.root.after(100,poll)
 def auto_status(self):
  if self.closed:return
  if self.client.key and not self.busy:self.work('status',quiet=True)
  self.root.after(15000,self.auto_status)
 def copy_link(self):
  self.root.clipboard_clear();self.root.clipboard_append(self.link.get());self.note('Đã sao chép link. Dán vào Browser Source trong OBS.')
 def open_link(self):
  if self.link.get().startswith('https://room.genaidol.com/live/'):webbrowser.open(self.link.get())
 def close(self):
  self.closed=True;self.pool.shutdown(wait=False,cancel_futures=True);self.root.destroy()
if __name__=='__main__':
 root=tk.Tk();DemoApp(root);root.mainloop()
