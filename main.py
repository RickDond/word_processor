from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox

class Find_dialog(Toplevel):
    def __init__(self, parent, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.geometry("450x200+200+200")
        self.title("Find and Replace")

        self.find_lbl = Label(self, text='Find:')
        self.find_entry = Entry(self, width=40)

        self.replace_lbl = Label(self, text='Replace')
        self.replace_entry = Entry(self, width=40)

        self.find_btn = Button(self, text="Find", command=self.parent.find)
        self.replace_btn = Button(self, text='Replace', command=self.parent.replace)

        self.find_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.find_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        self.replace_lbl.grid(row=1, column=0, padx=10, pady=10)
        self.replace_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        self.find_btn.grid(row=2,column=1, padx=10, pady=10)
        self.replace_btn.grid(row=2, column=2, padx=10, pady=10)

class MainMenu(Menu):
    # Main Menu
    def __init__(self, parent, *args, **kwargs):
        Menu.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # ******** File Menu ********
        self.file = Menu(self, tearoff=0)
        self.add_cascade(label='File', menu=self.file)

        # ****** New File ***********
        self.new_icon = PhotoImage(file='icons/new.png')
        self.file.add_command(label='New', image=self.new_icon, compound=LEFT, accelerator="Ctrl+N",
                              command=self.parent.new_file)

        # ****** Open ***************
        self.open_icon = PhotoImage(file='icons/open.png')
        self.file.add_command(label='Open', image=self.open_icon, compound=LEFT, accelerator="Ctrl+O",
                              command=self.parent.open_file)

        # ****** Save ***************
        self.save_icon = PhotoImage(file='icons/save_icon.png')
        self.file.add_command(label='Save', image=self.save_icon, compound=LEFT, accelerator="Ctrl+S",
                              command=self.parent.save_file)

        # ****** Save As ***************
        self.file.add_command(label='Save As', accelerator="Ctrl+Alt+S",
                              command=self.parent.save_as_file)

        # ****** Exit *****************
        self.exit_icon = PhotoImage(file='icons/exit.png')
        self.file.add_command(label='Exit', image=self.exit_icon, compound=LEFT,
                              command=self.parent.exit)

        # ****** Edit Menu ***********
        self.edit = Menu(self, tearoff=0)
        self.add_cascade(label='Edit', menu=self.edit)

        # ****** Edit Commands *******
        self.edit.add_command(label='Copy', accelerator="Ctrl+C",
                              command=lambda: self.parent.text_editor.event_generate('<Control C>'))
        self.edit.add_command(label='Paste', accelerator="Ctrl+V",
                              command=lambda: self.parent.text_editor.event_generate('<Control V>'))
        self.edit.add_command(label='Cut', accelerator="Ctrl+X",
                              command=lambda: self.parent.text_editor.event_generate('<Control X>'))
        self.edit.add_command(label='Clear All', accelerator="Ctrl+Alt+C",
                              command=lambda: self.parent.text_editor.delete("1.0", "end"))
        self.edit.add_command(label='Find', accelerator="Ctrl+F", command=self.parent.find_replace)

        # ****** View Menu ***********
        self.view = Menu(self, tearoff=0)
        self.add_cascade(label='View', menu=self.view)

        # ****** View Commands *******
        global show_tool_var
        global show_status_var

        self.view.add_checkbutton(label='Tool bar', onvalue=True, offvalue=False, variable=show_tool_var,
                                  command=self.parent.hide_tool_bar)
        self.view.add_checkbutton(label='Status bar', onvalue=True, offvalue=False, variable=show_status_var,
                                  command=self.parent.hide_status_bar)

        # ****** Theme Menu **********
        self.themes = Menu(self, tearoff=0)
        self.add_cascade(label="Templates", menu=self.themes)

        self.color_dict = {
            'Default': '#000000.#FFFFFF',  # First one is Font Color and second one is Background Color
            'Tomatoe': '#ffff00.#ff6347',
            'LimeGreen': '#fffff0.#32cd32',
            'Magenta': '#fffafa.#ff00ff',
            'RoyalBlue': '#ffffbb.#4169e1',
            'MediumBlue': '#d1e7e0.#0000cd',
            'Dracula': '#ffffff.#000000',
        }
        # Ver que es mejor si variables globales o pertenecientes a objeto
        self.theme_choice = StringVar()
        self.theme_choice.set('Default')

        for i in sorted(self.color_dict):
            self.themes.add_radiobutton(label=i, variable=self.theme_choice, command=self.parent.set_theme)

        # About
        self.about_menu = Menu(self, tearoff=0)
        self.add_cascade(label="About", command=self.parent.about_message)
        #self.add_command(label="About", command=self.parent.about_message)


class TextEditor(Text):
    # Text Editor
    def __init__(self, parent, *args, **kwargs):
        Text.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(wrap='word', font='arial 12')
        self.pack(side=TOP, expand=YES, fill=BOTH)
        xscrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.xview)
        xscrollbar.pack(side=BOTTOM, fill=X)
        yscrollbar = Scrollbar(self, orient=VERTICAL, command=self.yview)
        yscrollbar.pack(side=RIGHT, fill=Y)
        self.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        # Quiero tratar de usar GRID
        # self.grid(row=0, column=0, sticky=NSEW)
        # xscrollbar.grid(row=1, column=0, columnspan=2, sticky=EW)
        # yscrollbar.grid(row=0, column=1, sticky=NS)


# Status Bar
class StatusBar(Label):
    def __init__(self, parent, *args, **kwargs):
        Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=BOTTOM, fill=X)  # expand=YES
        self.config(text='Status Bar')


class ToolBar(Label):
    # Tool Bar
    def __init__(self, parent, *args, **kwargs):
        Label.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack(side=TOP, fill=X)

        # Combo box
        self.font_cb = ttk.Combobox(self)
        self.font_cb.pack(side=LEFT, padx=(10, 0))

        fonts = font.families()
        self.fonts_list = []
        for f in fonts:
            if not(" " in f):
                self.fonts_list.append(f)

        global font_te

        self.font_cb.config(values=self.fonts_list, textvariable=font_te)

        self.font_size_cb = ttk.Combobox(self)
        self.font_size_cb.pack(side=LEFT, padx=(10, 0))

        self.font_size_list = []

        global font_size
        for i in range(8, 80):
            self.font_size_list.append(str(i))

        self.font_size_cb.config(values=self.font_size_list, textvariable=font_size)

        self.font_cb.bind('<<ComboboxSelected>>', self.parent.set_font)
        self.font_size_cb.bind('<<ComboboxSelected>>', self.parent.set_font)

        # Icons
        self.bold_icon = PhotoImage(file='icons/bold.png')
        self.bold_icon_btn = Button(self, image=self.bold_icon, command=self.parent.set_bold)
        self.bold_icon_btn.pack(side=LEFT, padx=(10, 0))

        self.italic_icon = PhotoImage(file='icons/italic.png')
        self.italic_icon_btn = Button(self, image=self.italic_icon, command=parent.set_italic)
        self.italic_icon_btn.pack(side=LEFT, padx=(10, 0))

        self.underline_icon = PhotoImage(file='icons/under_line.png')
        self.underline_icon_byn = Button(self, image=self.underline_icon, command=parent.set_underline)
        self.underline_icon_byn.pack(side=LEFT, padx=(10, 0))

        self.color_icon = PhotoImage(file='icons/color.png')
        self.color_icon_btn = Button(self, image=self.color_icon, command=parent.set_color)
        self.color_icon_btn.pack(side=LEFT, padx=(10, 0))

        self.align_left_icon = PhotoImage(file='icons/alignleft.png')
        self.align_left_icon_btn = Button(self, image=self.align_left_icon, command=parent.set_align_left)
        self.align_left_icon_btn.pack(side=LEFT, padx=(10, 0))

        self.align_center_icon = PhotoImage(file='icons/aligncenter.png')
        self.align_center_icon_btn = Button(self, image=self.align_center_icon, command=parent.set_align_center)
        self.align_center_icon_btn.pack(side=LEFT, padx=(10, 0))

        self.align_right_icon = PhotoImage(file='icons/alignright.png')
        self.align_right_icon_btn = Button(self, image=self.align_right_icon, command=parent.set_align_right)
        self.align_right_icon_btn.pack(side=LEFT, padx=(10, 0))


# Main Application
class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        # Ver para que sirve?
        self.pack(side=TOP, fill=BOTH, expand=True)
        # Creating widgets
        self.main_menu = MainMenu(self)
        self.tool_bar = ToolBar(self)
        self.text_editor = TextEditor(self)
        self.text_editor.focus_set()
        self.status_bar = StatusBar(self)

        self.text_editor.bind('<<Modified>>', self.text_editor_changed)

        # Class variables
        self.url = None
        self.saved = True
        self.parent = parent

        # Parent Menu Configuration
        self.parent.config(menu=self.main_menu)

    def new_text_editor(self, *args):
        self.text_editor.destroy()
        self.text_editor = TextEditor(self)
        self.text_editor.focus_set()
        self.text_editor.bind('<<Modified>>', self.text_editor_changed)

    def set_font(self, *args):
        f = self.tool_bar.font_cb.get()
        fs = self.tool_bar.font_size_cb.get()
        self.text_editor.config(font=(f, fs))

    def set_bold(self, *args):
        text_pro = font.Font(font=self.text_editor['font'])
        f = self.tool_bar.font_cb.get()
        fs = self.tool_bar.font_size_cb.get()

        # {'family': 'Arial', 'size': 15, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
        weight = text_pro.actual('weight')
        slant = text_pro.actual('slant')
        underline = 'underline' if text_pro.actual('underline') == 1 else ''
        new_weight = 'bold' if weight == 'normal' else 'normal'
        options = " ".join([f, fs, new_weight, slant, underline])
        self.text_editor.configure(font=options)

    def set_italic(self, *args):
        text_pro = font.Font(font=self.text_editor['font'])
        f = self.tool_bar.font_cb.get()
        fs = self.tool_bar.font_size_cb.get()
        weight = text_pro.actual('weight')
        slant = text_pro.actual('slant')
        underline = 'underline' if text_pro.actual('underline') == 1 else ''
        new_slant = 'roman' if slant == 'italic' else 'italic'
        options = " ".join([f, fs, weight, new_slant, underline])
        self.text_editor.configure(font=options)

    def set_underline(self, *args):
        text_pro = font.Font(font=self.text_editor['font'])
        f = self.tool_bar.font_cb.get()
        fs = self.tool_bar.font_size_cb.get()
        weight = text_pro.actual('weight')
        slant = text_pro.actual('slant')
        # {'family': 'Arial', 'size': 15, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
        underline = 'underline' if text_pro.actual('underline') == 1 else ''
        new_underline = "" if underline == 'underline' else 'underline'
        options = " ".join([f, fs, weight, slant, new_underline])
        self.text_editor.configure(font=options)

    def set_color(self, *args):
        color = colorchooser.askcolor()
        self.text_editor.configure(fg=color[1])

    def set_align_left(self, *args):
        content = self.text_editor.get("1.0", "end-1c")
        self.text_editor.delete("1.0", "end")
        self.text_editor.tag_config("left", justify=LEFT)
        self.text_editor.insert("1.0", content, "left")

    def set_align_center(self, *args):
        content = self.text_editor.get("1.0", "end-1c")
        self.text_editor.delete("1.0", "end")
        self.text_editor.tag_config("center", justify=CENTER)
        self.text_editor.insert("1.0", content, "center")

    def set_align_right(self, *args):
        content = self.text_editor.get("1.0", "end-1c")
        self.text_editor.delete("1.0", "end")
        self.text_editor.tag_config("right", justify=RIGHT)
        self.text_editor.insert("1.0", content, "right")

    def text_editor_changed(self, *args):
        def elimina_vacio(wl):
            for index in range(len(wl)-1, -1, -1):
                if wl[index] == '':
                    del(wl[index])
            return wl

        flag = self.text_editor.edit_modified()
        if flag:
            word_count = 0
            lineas = self.text_editor.get("1.0", "end-1c").split('\n')

            for linea in lineas:
                words = linea.split(' ')
                words_sin_espacio = elimina_vacio(words)
                word_count += len(words_sin_espacio)

            letters = len(self.text_editor.get("1.0", "end-1c"))
            self.status_bar.config(text="Characters: " + str(letters) + ", Words: " + str(word_count))

        self.text_editor.edit_modified(False)
        self.saved = False
        if self.url is None:
            self.parent.title("Untitled*")
        else:
            self.parent.title(self.url[0:-4]+'*'+self.url[-4:])

    def new_file(self, *args):
        if self.saved:
            self.text_editor.destroy()
            self.new_text_editor()
            self.text_editor.edit_modified(True)
        else:
            if self.url is None:
                urltext = "Untitled.txt"
            else:
                urltext = self.url
            exitwithoutsaved = messagebox.askyesnocancel(title="Exit without save",
                                                         message="Do you want to save changes to " + urltext)
            if exitwithoutsaved == YES:
                self.save_as_file()
            elif exitwithoutsaved == NO:
                self.text_editor.destroy()
                self.new_text_editor()
                self.text_editor.edit_modified(True)
            else:
                return

    def open_file(self, *args):

        url = filedialog.askopenfilename(title="Open File", initialdir='/',
                                         filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        self.url = url
        try:
            self.text_editor.delete(1.0, END)
            with open(url, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    self.text_editor.insert(END, line)
        except Exception:
            return
        else:
            self.parent.title(url.split("/")[-1])
        finally:
            pass
        self.saved = True

    def save_file(self, *args):
        if self.url is not None:
            text = self.text_editor.get(1.0, END)
            try:
                with open(self.url, "w", encoding='utf-8') as file:
                    file.write(text)
            except Exception:
                return
        else:
            self.save_as_file()
        self.saved = True

    def save_as_file(self, *args):

        url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',
        title="Save File", initialdir='/', filetypes=(("Text Files", "*.txt"),))

        text = self.text_editor.get(1.0, END)
        try:
            url.write(text)
        except Exception:
            return
        url.close()
        self.parent.title(url.name.split("/")[-1])
        self.saved = True

    def exit(self, *args):
        if self.saved:
            self.parent.destroy()
        else:
            if self.url is None:
                urltext = "Untitled.txt"
            else:
                urltext = self.url
            exitwithoutsaved = messagebox.askyesnocancel(title="Exit without save",
                                                         message="Do you want to save changes to " + urltext)
            if exitwithoutsaved == YES:
                self.save_as_file()
            elif exitwithoutsaved == NO:
                self.parent.destroy()
            else:
                return

    def set_theme(self, *args):
        choice = self.main_menu.theme_choice.get()
        colors_list = self.main_menu.color_dict[choice].split(".")
        color_background = colors_list[1]
        color_foreground = colors_list[0]
        self.text_editor.configure(bg=color_background, fg=color_foreground)

    def about_message(self, *args):
        messagebox.showinfo("About", "This Text Editor is created for Educational Purposes")

    def find_replace(self, *args):
        self.find_replace = Find_dialog(self)

    def find(self, *args):
        findtxt = self.find_replace.find_entry.get()
        self.text_editor.tag_remove('match', 1.0, END)
        matches = 0
        if findtxt:
            start_pos = 1.0
            while True:
                start_pos = self.text_editor.search(findtxt, start_pos, stopindex=END)
                if not start_pos:
                    break
                end_pos = '{}+{}c'.format(start_pos, len(findtxt))
                self.text_editor.tag_add('match', start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                self.text_editor.tag_config('match', foreground='red', background='yellow')

    def replace(self, *args):
        findtxt = self.find_replace.find_entry.get()
        replacetxt = self.find_replace.replace_entry.get()
        text_to_replace = self.text_editor.get(1.0, END)
        replaced_text = text_to_replace.replace(findtxt, replacetxt)
        self.text_editor.delete(1.0, END)
        self.text_editor.insert(1.0, replaced_text)
        self.find_replace.destroy()

    def hide_status_bar(self, *args):
        global show_status_var

        if show_status_var:
            self.status_bar.pack_forget()

            show_status_var = False
        else:
            self.text_editor.pack_forget()
            self.tool_bar.pack_forget()
            self.tool_bar.pack(side=TOP, fill=X)
            self.text_editor.pack(side=TOP, expand=YES, fill=BOTH)
            self.status_bar.pack(side=BOTTOM, fill=X)
            show_status_var = True

    def hide_tool_bar(self, *args):
        global show_tool_var
        if show_tool_var:
            self.tool_bar.pack_forget()
            show_tool_var = False
        else:
            self.text_editor.pack_forget()
            self.status_bar.pack_forget()
            self.tool_bar.pack(side=TOP, fill=X)
            self.text_editor.pack(side=TOP, expand=YES, fill=BOTH)
            self.status_bar.pack(side=BOTTOM, fill=X)
            show_tool_var = True


if __name__ == '__main__':
    root = Tk()
    root.title("Untitled")
    root.geometry("1250x650")
    root.iconbitmap('icons/icon.ico')

    # Global Variables
    show_tool_var = BooleanVar()
    show_tool_var.set(True)
    show_status_var = BooleanVar()
    show_status_var.set(True)
    font_te = StringVar()
    font_te.set('Arial')
    font_size = StringVar()
    font_size.set('12')
    url = ""
    app = MainApplication(root).pack(side=TOP, fill=BOTH, expand=True)
    root.mainloop()
