from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter as tk
import os
import filecmp
import datetime

global is_detect_open #To avoid doing the detection task multiple times (True/False)
global filename #path to the folder to scan
global scan_type #type of scanning methods
global comp_type #type of comp methods (True=only metadata / False=everything is compared)

global take_in_consideration_size
global size
global take_in_consideration_ext
global ext_

is_detect_open = False
filename = ""

class Main_window: #Creation de la fenetre principale
    def __init__(self, master):
        global scan_type
        global comp_type
        global take_in_consideration_size
        global size
        global take_in_consideration_ext
        global ext_

        self.master = master
        self.frame = tk.Frame(self.master)

        self.Detectapp = None

        #boutton aide
        self.Aide_button = tk.Button(self.frame, text = 'Aides', width = 40, command = self.Aides)
        self.Aide_button.grid(row=0,column=0,padx=9,pady=9,columnspan=2)

        #boutton choix dossier
        self.Choose_folder_button = tk.Button(self.frame, text = 'Choisir un dossier', width = 40, command = self.Choose_folder)
        self.Choose_folder_button.grid(row=1,column=0,padx=9,pady=9,columnspan=2)

        #checkbox scan complet / dossier par dossier
        frame_scan=tk.LabelFrame(self.frame,text="type de scan")
        scan_type = tk.IntVar()
        scan_type.set(1)
        self.C1 = tk.Radiobutton(frame_scan, text="Scan complet",  variable = scan_type, value = 1)
        self.C2 = tk.Radiobutton(frame_scan, text="Scan fichier par fichier", variable = scan_type, value = 2)

        self.C1.grid(row=0,column=0)
        self.C2.grid(row=0,column=1)
        frame_scan.grid(row=2,column=0,columnspan=2)

        frame_comp=tk.LabelFrame(self.frame,text="type de comparaison")
        comp_type = tk.BooleanVar()
        comp_type.set(True)
        self.C3 = tk.Radiobutton(frame_comp, text="Scan contenu entier",  variable = comp_type, value = False)
        self.C4 = tk.Radiobutton(frame_comp, text="Scan metadonnées", variable = comp_type, value = True)

        self.C3.grid(row=0,column=0)
        self.C4.grid(row=0,column=1)
        frame_comp.grid(row=3,column=0,columnspan=2)

        #checkbox taille
        take_in_consideration_size = tk.BooleanVar()
        self.taille_check = ttk.Checkbutton(self.frame, text="Taille mini fichier [ko]:", variable=take_in_consideration_size, command=self.up)
        self.taille_check.grid(row=4,column=0)

        vcmd = (root.register(self.callback_verif),'%P')

        size=tk.StringVar()
        self.size_entry = tk.Entry(self.frame, validate='all', bg='gray',textvariable=size, validatecommand=vcmd)
        self.size_entry.grid(row=4,column=1)

        #checkbox ext
        take_in_consideration_ext = tk.BooleanVar()
        self.ext_check = ttk.Checkbutton(self.frame, text="Extension [séparé par ',']:", variable=take_in_consideration_ext, command=self.up)
        self.ext_check.grid(row=5,column=0)

        vcmd2 = (root.register(self.callback_verif_ext),'%P')

        ext_=tk.StringVar()
        self.ext_entry = tk.Entry(self.frame, validate='all', bg='gray',textvariable=ext_, validatecommand=vcmd2)
        self.ext_entry.grid(row=5,column=1)

        #boutton détection des doublon
        self.Generate_button = tk.Button(self.frame, text = 'Détection des doublons', width = 40, command = self.Detect)
        self.Generate_button.grid(row=6,column=0,padx=9,pady=9,columnspan=2)

        self.frame.pack()

    def up(self):
        global take_in_consideration_size
        global take_in_consideration_ext

        if take_in_consideration_size.get():
            self.size_entry.config(bg='white')
        else:
            self.size_entry.config(bg='gray')

        if take_in_consideration_ext.get():
            self.ext_entry.config(bg='white')
        else:
            self.ext_entry.config(bg='gray')

    def Aides(self):
        self.Aides = tk.Toplevel(self.master)
        self.app = Aides_window(self.Aides)

    def Choose_folder(self):
        global filename

        filename = filedialog.askdirectory()
        if filename!="":
            self.Choose_folder_button.config(text="Choisir un dossier\n"+filename)
        else:
            self.Choose_folder_button.config(text="Choisir un dossier")

    def Detect(self):
        global filename
        global is_detect_open

        if filename=="":
            showinfo(message='Erreur - Aucun dossier sélectionné')

        elif not is_detect_open:
            is_detect_open=True
            self.Detectapp = tk.Toplevel(self.master)
            self.app = Detect_window(self.Detectapp)


    def callback_verif(self, P):
        global take_in_consideration_size
        if (str.isdigit(P) or P == "") and take_in_consideration_size.get():
            return True
        else:
            return False

    def callback_verif_ext(self, P):
        global take_in_consideration_ext
        if take_in_consideration_ext.get():
            return True
        else:
            return False

class Aides_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        try:self.master.iconbitmap(resource_path("Anti_doublapp_ico.ico"))
        except Exception:pass
        self.master.title("Aides")

        T = tk.Text(self.frame, height = 20, width = 130)
        l = tk.Label(self.frame, text = "Section Aides",font=("Arial", 15))

        info_aide = """Voici les étapes à suivre pour détecter les doublons présents dans un ou plusieurs dossiers:\n
        1) Choisir un dossier\n
        2) Sélectionner un mode de scan :\n   -Complet = Cherche les doublons présents dans tous les fichiers présents dans tout le dossier sélectionné (peut être très long)\n   -Dossier par dossier = Cherche les doublons dans les dossiers un par un, ne detecte donc pas les doublons présents dans\ndifférents dossiers, mais est plus rapide\n
        3) Choisir type de comparaison de fichier. Comparer les métadonnées est plus rapide mais moins fiable.\n
        4) Choisir la taille minimale en ko, si le bouton n'est pas coché la taille ne sera pas prise en compte\n
        5) Choisir les possible extensions à traiter (ex : .png,.MPEG,.pdf), si le bouton n'est pas coché l'extension ne sera pas prise en compte\n
        6) Cliquer sur "Détection des doublons"\n
Ce programme n'éfface rien de lui même. Il isole juste les doublons dans un dossier à part nommé "Doublons".
        """

        l.pack(padx=5,pady=5)
        T.pack(padx=5,pady=5)
        T.insert(tk.END, info_aide)
        self.quitButton = tk.Button(self.frame, text = 'Quitter', width = 40, command = self.close_windows)
        self.quitButton.pack(padx=5,pady=5)
        self.frame.pack(padx=5,pady=5)

    def close_windows(self):
        self.master.destroy()


class Detect_window:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        try:self.master.iconbitmap(resource_path("Anti_doublapp_ico.ico"))
        except Exception:pass

        self.master.title("Scan")

        self.l = tk.Label(self.frame, text = "Détection de fichiers ...")
        self.l.grid(column=0, row=0, padx=0, pady=10)

        self.quitButton = tk.Button(self.frame, text = 'Annuler', width = 20, command = self.close_windows)
        self.quitButton.grid(column=2, row=2, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(
            self.frame,
            orient='horizontal',
            mode='determinate',
            length=500
        )
        self.progress_bar.grid(column=0, row=1, columnspan=3, padx=5, pady=10)

        self.frame.pack()
        self.master.protocol("WM_DELETE_WINDOW", self.closed)

        self.nb_doublon=0
        root.update()
        self.BEGIN_SCAN()
        self.progress(1,1)
        showinfo(message=str(self.nb_doublon)+' doublons ont été détectés et déplacés')
        self.close_windows

    def BEGIN_SCAN(self):
        global filename
        global is_detect_open
        global scan_type
        global comp_type

        global take_in_consideration_size
        global size
        global take_in_consideration_ext
        global ext_


        if size.get()!='':
            size2=size.get()
        else : size2=0

        listext=ext_.get().split(",")

        if scan_type.get()==1:#scan all files

            doublon_dir=os.path.join(filename,'Doublons')
            to_compare=[]
            for path, directories, files in os.walk(filename):

                if not(files==[]) and path!=doublon_dir:
                    for e in files:
                        if not take_in_consideration_size.get() or os.stat(os.path.join(path,e)).st_size/1024 > int(size2):
                            if not take_in_consideration_ext.get() or os.path.splitext(os.path.join(path,e))[1] in listext:
                                to_compare.append(os.path.join(path,e))#ajout de l'element à la liste à comparer

            self.l.config(text=str(len(to_compare))+" fichiers ont été détectés")
            root.update()
            first_time=True

            i=0
            while i < len(to_compare):
                k=0
                no=1
                while k < len(to_compare):

                    if (k+no)%50==0:
                        self.progress(i+1,len(to_compare))

                    if k>i and filecmp.cmp(to_compare[i], to_compare[k], shallow = comp_type.get()):
                        if first_time:
                            first_time=False
                            try:
                                os.mkdir(doublon_dir)
                            except OSError as error:pass

                        now = str(datetime.datetime.now())[:19]
                        now = now.replace(":","_")

                        target_name="doublon_n_"+str(no)+"_de_"+os.path.basename(os.path.normpath(to_compare[i]))
                        no+=1
                        move_to=os.path.join(doublon_dir,target_name)

                        os.rename(to_compare[k],move_to)

                        to_compare.pop(k)
                        self.nb_doublon+=1


                    else: k+=1
                i+=1


        if scan_type.get()==2:#scan all directories one by one
            to_compare=[filename]
            for path, directories, files in os.walk(filename):
                if not(directories==[]):
                    for e in directories:
                        if not(e.endswith('Doublons')):
                            to_compare.append(os.path.join(path,e))

            self.l.config(text=str(len(to_compare))+" dossiers ont été détectés | Scan dossier 1/"+str(len(to_compare)))
            folder_no=0
            for folder in to_compare:
                doublon_dir=os.path.join(folder,'Doublons')
                first_time=True

                to_compare_file=[]
                for file in os.listdir(folder):
                    #print(os.path.join(folder,file), os.stat(os.path.join(folder,file)).st_size/1024, int(size2))
                    if not take_in_consideration_size.get() or os.stat(os.path.join(folder,file)).st_size/1024 > int(size2):
                        if not take_in_consideration_ext.get() or os.path.splitext(os.path.join(folder,file))[1] in listext:
                            to_compare_file.append(os.path.join(folder,file))

                i=0
                while i < len(to_compare_file):
                    k=0
                    no=1
                    while k < len(to_compare_file):

                        if (k+no)%50==0:
                            self.progress(i+1,len(to_compare))

                        if k>i and filecmp.cmp(to_compare_file[i], to_compare_file[k], shallow = comp_type.get()):
                            if first_time:
                                first_time=False
                                try:
                                    os.mkdir(doublon_dir)
                                except OSError as error:pass

                            now = str(datetime.datetime.now())[:19]
                            now = now.replace(":","_")

                            target_name="doublon_n_"+str(no)+"_de_"+os.path.basename(os.path.normpath(to_compare_file[i]))
                            no+=1
                            move_to=os.path.join(doublon_dir,target_name)

                            os.rename(to_compare_file[k],move_to)

                            to_compare_file.pop(k)
                            self.nb_doublon+=1
                            self.progress(i+1,len(to_compare))

                        else: k+=1
                    i+=1
                folder_no+=1
                self.l.config(text=str(len(to_compare))+" dossiers ont été détectés | Scan dossier "+str(folder_no)+"/"+str(len(to_compare)))
                root.update()



    def close_windows(self):
        global is_detect_open
        is_detect_open = False
        self.master.destroy()

    def closed(self):
        global is_detect_open
        is_detect_open = False
        self.master.destroy()

    def progress(self,a,b):
            self.progress_bar['value'] = int(100*a/b)
            root.update()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    root = tk.Tk()
    app = Main_window(root)
    root.title("Anti doublapp")
    try:root.iconbitmap(resource_path("Anti_doublapp_ico.ico"))
    except Exception:pass


    root.mainloop()
