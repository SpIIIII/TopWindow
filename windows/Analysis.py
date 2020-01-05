import matplotlib.animation as animation
import datetime as dt
import tkinter as tk
from tkinter import ttk
from random import randrange
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Analysis(tk.Toplevel):
    def __init__(self,root,punkts,plot):
        super().__init__(root)
        self.title("Анализ")
        self.geometry("640x530")
        self.minsize(600,350)
        self.bind('<Escape>', lambda e: self.exit())
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.plot = plot
        self.punkts = punkts
        
        self.curent_date = dt.datetime.now()
        
        self.init_analysis()
        

    def exit(self):
        self.plot.destroy()
        self.destroy()
    

    def init_analysis(self):
        
        
        def update_plot(event):
            # inject data that need to be plotted
            self.plot.set_data(combox_punkts.get(), combox_month.get())
            # update plot
            self.plot.update_plot()
      
            
        ## add frames
        top_frame = ttk.Frame(self,height=50)
        top_frame.pack(side=tk.TOP,fill=tk.BOTH, expand=True)

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)

        ## Draw MenuBar
        menubar = tk.Menu()
        filemenu = tk.Menu(menubar, tearoff=0)
          
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.destroy)
        
        menubar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menubar)

        ## fill top_frame
        #create label
        label = ttk.Label(top_frame, text = 'Выбранный пункт будет отмечен \nкрасным на графике')
        label.place(x=150, y=10)

        # create combox_month
        combox_month = ttk.Combobox(top_frame,values=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август',
                                                         'Сентябрь','Октябрь','Ноябрь','Декабрь'],justify='center')
        combox_month.current(self.curent_date.month-1)
        combox_month.bind("<<ComboboxSelected>>", update_plot)
        combox_month.place(x=470,y=10)

        # create combox_punkts
        combox_punkts = ttk.Combobox(top_frame, justify='center',width = 15)
        combox_punkts.bind("<<ComboboxSelected>>", lambda x: update_plot(None))
        combox_punkts.place(x=340,y=30)
        def create_combox_punkts(period):
            if period == ' Все':
                punkts_to_fill = [i.name for i in self.punkts]
                combox_punkts.config(values=punkts_to_fill)
                combox_punkts.current(randrange(0,len(punkts_to_fill)))
            else:
                punkts_to_fill = [i.name for i in self.punkts if i.period == period]
                combox_punkts.config(values=punkts_to_fill)
                combox_punkts.current(randrange(0,len(punkts_to_fill)))
        create_combox_punkts(' Все')
            
        # create period_combobox
        periods = sorted([i for i in set(i.period for i in self.punkts)])
        periods.append(' Все')
        combox_periods = ttk.Combobox(top_frame,values=periods,justify='center')
        combox_periods.current(len(periods)-1)
        combox_periods.place(x=470,y=30)
        combox_periods.bind("<<ComboboxSelected>>", lambda x: (create_combox_punkts(combox_periods.get()),update_plot(None)))

        # set data and plot it initialy
        self.plot.set_data(combox_punkts.get(), combox_month.get())
        self.plot.draw_plot_for_month(bottom_frame)

        self.grab_set()
        self.focus_set()