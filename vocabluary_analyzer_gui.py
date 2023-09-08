from customtkinter import CTk, CTkOptionMenu, CTkFrame, CTkImage, CTkLabel, CTkButton, CTkEntry, \
    set_appearance_mode, set_default_color_theme
from json import load
from tkinter import Menu
from webbrowser import open as webopen
from tkinter.ttk import Progressbar
from classes_classifier_extractor import *
from threading import Thread, ThreadError


# starting gui with creating a class
class EnglishFilterProgram(CTk):

    # override
    def __init__(self):
        super().__init__()

        # window configurations
        self.title("CODE-DEM FILTER")

        self.geometry("900x600+420+170")

        self.resizable(False, False)

        set_appearance_mode("dark")

        set_default_color_theme("dark-blue")

        # setting variables for gui

        # read json and set dictionary variable
        with open("gui_options/dictionary.json", "r", encoding="utf-8") as file:
            self.option_menu_dictionary = load(file)

        # option menu values
        self.option_menu_values = list(self.option_menu_dictionary.keys())

        # menu section
        menubar = Menu(self)
        file = Menu(menubar, tearoff=0)

        # settings section
        menubar.add_cascade(label="Ayarlar", menu=file)
        file.add_command(label="Aydınlık Mod", command=self.appearance_mode_changer)

        file.add_separator()
        file.add_command(label="Karanlık Mod", command=self.appearance_mode_changer2)

        file.add_separator()
        file.add_command(label="X-Y CONFIG FOR NEW TEMPLATE", command=lambda: None)

        file.add_separator()
        file.add_command(label="Web Sitesini Ziyaret Et", command=self.visit_website)

        # exit section
        menubar.add_command(label="Çıkış Yap", command=self.exiting)

        self.configure(menu=menubar)

        "---------------------------------------------------------------" \
        "FRAME 1--------------------------------------------------------" \
        "---------------------------------------------------------------"

        # frame configs
        self.main_frame = CTkFrame(master=self, fg_color="gray75")

        self.main_frame.pack(fill="both", padx=20, pady=10, expand=True)

        # main label

        self.main_label = CTkLabel(master=self.main_frame, text="KELİME FİLTRELEME\nVE\nPOST ÜRETME ARACI",
                                   text_color="brown4").pack()

        # options menu and label
        # label
        self.option_menu_label = CTkLabel(master=self.main_frame, text="KELİME CİNSİNİ SEÇİNİZ :",
                                          text_color="black").pack(anchor="w", padx=10, pady=10)
        # options
        self.option_menu = CTkOptionMenu(master=self.main_frame, fg_color="green", button_hover_color="green3",
                                         values=self.option_menu_values,
                                         button_color="green2")

        self.option_menu.pack(fill="x", anchor="w", padx=10)

        # file name entry
        self.file_name_entry = CTkEntry(master=self.main_frame, placeholder_text="OLUŞTURULACAK DOSYA ADINI SEÇİNİZ")

        self.file_name_entry.pack(anchor="w", fill="x", pady=20, padx=10)

        # extract text and render text button
        self.run_button = CTkButton(master=self.main_frame, text="PROGRAMI BAŞLAT", text_color="black",
                                    hover_color="brown2", fg_color="brown4",
                                    command=self.analyze_function).pack(anchor="w", fill="x", padx=10, pady=20)

        # prgressbar
        self.progress_bar = Progressbar(master=self.main_frame, mode="determinate")

        self.progress_bar.pack(anchor="w", padx=10, pady=20, fill="x")

        self.progress_bar['value'] = 0

        # progresbar label
        self.progressbar_percent = CTkLabel(master=self.main_frame, text=f"TAMAMLANMA YÜZDESİ % 0 :",
                                            text_color="black")
        self.progressbar_percent.pack(anchor="w", padx=10, pady=10)

        # run button

    # button functions
    @staticmethod
    def appearance_mode_changer():
        # change appearance mode
        set_appearance_mode("system")

    @staticmethod
    def appearance_mode_changer2():
        # change appearance mode
        set_appearance_mode("dark")

    @staticmethod
    def visit_website():
        # get our web site
        webopen("https://www.code-dem.com")

    # exit function
    @staticmethod
    def exiting():
        exit()

    # analyze function
    def analyze_function(self):
        # reset progressbar value
        self.progress_bar['value'] = 0

        # get option value and convert
        option_value = self.option_menu.get()

        option_value = self.option_menu_dictionary[option_value]

        # get entry values
        post_dir_name = self.file_name_entry.get()

        try:
            # run funct
            analyzer_function(option_value, post_dir_name, self.progress_bar, self.main_frame)

        except:
            raise


c = EnglishFilterProgram()


# progressbar thread
def percent():
    while True:
        # thread operation
        # catch errors with try except blocks
        try:
            val = c.progress_bar['value']
            c.progressbar_percent.configure(text=f"TAMAMLANMA YÜZDESİ %{val:.1f}")
        except RuntimeError:
            exit()


Thread(target=percent).start()

c.mainloop()
