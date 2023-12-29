# -*- coding: utf-8 -*-
from tkinter import Tk, Label, Entry, Text, Button, Toplevel, StringVar, messagebox
import random
import string
import sqlite3

class ApplicationGestionnaireMotsDePasse:
    
    def __init__(self):
        self.root = Tk()
        self.root.title("Gestionnaire de Mots de Passe")
        self.root.geometry("500x400")

        self.creer_base_de_donnees()

        self.configurer_fenetre_principale()

    
    def generer_mot_de_passe(self, longueur, mode):
        if mode == 1:
            caracteres = string.ascii_letters
        elif mode == 2:
            caracteres = string.digits
        elif mode == 3:
            caracteres = string.ascii_letters + string.digits
        else:
            caracteres = string.ascii_letters + string.digits + string.punctuation

        if caracteres:
            mot_de_passe = ''.join(random.choice(caracteres) for i in range(longueur))
            return mot_de_passe
        else:
            return "Mode invalide"

    def creer_base_de_donnees(self):
        conn = sqlite3.connect('mots_de_passe.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS mots_de_passe
                     (id INTEGER PRIMARY KEY, titre TEXT, nom_utilisateur TEXT, mot_de_passe TEXT, url TEXT, notes TEXT)''')
        conn.commit()
        conn.close()


    def vider_table_mots_de_passe(self):
        conn = sqlite3.connect('mots_de_passe.db')
        c = conn.cursor()
        c.execute("DELETE FROM mots_de_passe")
        conn.commit()
        conn.close()

    def ajouter_mot_de_passe(self, titre, nom_utilisateur, mot_de_passe, url, notes):
      conn = sqlite3.connect('mots_de_passe.db')
      c = conn.cursor()
      c.execute("INSERT INTO mots_de_passe (titre, nom_utilisateur, mot_de_passe, url, notes) VALUES (?, ?, ?, ?, ?)", (titre, nom_utilisateur, mot_de_passe, url, notes))
      conn.commit()
      conn.close()

    def supprimer_mot_de_passe(self, id):
      conn = sqlite3.connect('mots_de_passe.db')
      c = conn.cursor()
      c.execute("DELETE FROM mots_de_passe WHERE id=?", (id,))
      conn.commit()
      conn.close()


    def voir_mots_de_passe(self):
        conn = sqlite3.connect('mots_de_passe.db')
        c = conn.cursor()
        c.execute("SELECT * FROM mots_de_passe")
        lignes = c.fetchall()
        conn.close()
        return lignes



    def configurer_fenetre_principale(self):
        Label(self.root, text="Gestionnaire de Mots de Passe", font=("Helvetica", 16)).pack(pady=10)

        Button(self.root, text="Voir les Mots de Passe", command=self.afficher_mots_de_passe).pack(pady=10)

        Button(self.root, text="Nouvelle Entrée", command=self.on_creer_mot_de_passe_click).pack(pady=10)

    def on_creer_mot_de_passe_click(self):
        fenetre_entree = Toplevel(self.root)
        fenetre_entree.title("Nouvelle Entrée de Mot de Passe")

        Label(fenetre_entree, text="Titre:").pack()
        champ_titre = Entry(fenetre_entree)
        champ_titre.pack()

        Label(fenetre_entree, text="Nom d'utilisateur:").pack()
        champ_nom_utilisateur = Entry(fenetre_entree)
        champ_nom_utilisateur.pack()

        Label(fenetre_entree, text="Mot de Passe:").pack()
        champ_mot_de_passe = Entry(fenetre_entree)
        champ_mot_de_passe.pack()

        Label(fenetre_entree, text="URL:").pack()
        champ_url = Entry(fenetre_entree)
        champ_url.pack()

        Label(fenetre_entree, text="Notes:").pack()
        champ_notes = Entry(fenetre_entree)
        champ_notes.pack()

        Button(fenetre_entree, text="Générer Mot de Passe", command=self.on_generer_mot_de_passe_click).pack(pady=10)

        Button(fenetre_entree, text="Enregistrer", command=lambda: self.enregistrer_mot_de_passe(
            champ_titre.get(),
            champ_nom_utilisateur.get(),
            champ_mot_de_passe.get(),
            champ_url.get(),
            champ_notes.get(),
            fenetre_entree
        )).pack()

    def on_generer_mot_de_passe_click(self):
        fenetre_generation = Toplevel(self.root)
        fenetre_generation.title("Générer Mot de Passe")

        Label(fenetre_generation, text="Longueur du Mot de Passe:").pack()
        champ_longueur = Entry(fenetre_generation)
        champ_longueur.pack()

        Label(fenetre_generation, text="Complexité du Mot de Passe (1-4):").pack()
        champ_mode = Entry(fenetre_generation)
        champ_mode.pack()

        Button(fenetre_generation, text="Générer", command=lambda: self.inserer_mot_de_passe_genere(
            champ_longueur.get(),
            champ_mode.get(),
            fenetre_generation
        )).pack()

    def inserer_mot_de_passe_genere(self, longueur, mode, fenetre_generation):
        try:
            longueur = int(longueur)
            mode = int(mode)
            mot_de_passe_genere = self.generer_mot_de_passe(longueur, mode)
            fenetre_generation.clipboard_clear()
            fenetre_generation.clipboard_append(mot_de_passe_genere)
            fenetre_generation.update()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour la Longueur et le Mode.")


    def enregistrer_mot_de_passe(self, titre, nom_utilisateur, mot_de_passe, url, notes, fenetre_entree):
        self.ajouter_mot_de_passe(titre, nom_utilisateur, mot_de_passe, url, notes)
        messagebox.showinfo("Succès", "Mot de passe ajouté avec succès !")
        fenetre_entree.destroy()

    def afficher_mots_de_passe(self):
        mots_de_passe = self.voir_mots_de_passe()

        fenetre_affichage = Toplevel(self.root)
        fenetre_affichage.title("Mots de Passe")

        if not mots_de_passe:
            Text(fenetre_affichage, height=10, width=100).pack(pady=10)
            widget_texte = Text(fenetre_affichage, height=10, width=50, wrap='none')
            widget_texte.insert('end', "Aucun mot de passe trouvé.")
            widget_texte.config(state='disabled')
            widget_texte.pack(pady=10)
        else:
            widget_texte = Text(fenetre_affichage, height=10, width=100, wrap='none')
            widget_texte.pack(pady=10)
            for i, mot_de_passe in enumerate(mots_de_passe):
                mot_de_passe_str = f"Mot de Passe {i + 1} - Titre: {mot_de_passe[1]}, Nom d'utilisateur: {mot_de_passe[2]}, " \
                                f"Mot de Passe: {mot_de_passe[3]}, URL: {mot_de_passe[4]}, Notes: {mot_de_passe[5]}\n\n"
                widget_texte.insert('end', mot_de_passe_str)

                # Ajouter un bouton "Supprimer" pour chaque mot de passe
                Button(fenetre_affichage, text=f"Supprimer le mot de passe n° {i + 1}", command=lambda index=i: self.supprimer_mot_de_passe(mots_de_passe[index][0])).pack()

            widget_texte.config(state='disabled')

    def supprimer_mot_de_passe(self, id):
        confirmation = messagebox.askokcancel("Confirmation", "Voulez-vous vraiment supprimer ce mot de passe ?")
        if confirmation:
            self.delete_password(id)
            messagebox.showinfo("Succès", "Mot de passe supprimé avec succès !")
            # Rafraîchir la fenêtre d'affichage après la suppression
            self.afficher_mots_de_passe()

    def on_generer_mot_de_passe_click(self):
        fenetre_generation = Toplevel(self.root)
        fenetre_generation.title("Générer Mot de Passe")

        Label(fenetre_generation, text="Longueur du Mot de Passe:").pack()
        champ_longueur = Entry(fenetre_generation)
        champ_longueur.pack()

        Label(fenetre_generation, text="Complexité du Mot de Passe (1-4):").pack()
        champ_mode = Entry(fenetre_generation)
        champ_mode.pack()

        Button(fenetre_generation, text="Générer", command=lambda: self.inserer_mot_de_passe_genere(
            champ_longueur.get(),
            champ_mode.get(),
            fenetre_generation,
            champ_mot_de_passe
        )).pack()

        # Ajouter le champ de mot de passe
        champ_mot_de_passe = Entry(fenetre_generation)
        champ_mot_de_passe.pack()

        # Ajouter le bouton de copie
        Button(fenetre_generation, text="Copier", command=lambda: self.copier_mot_de_passe(champ_mot_de_passe.get())).pack()

    # ...

    def inserer_mot_de_passe_genere(self, longueur, mode, fenetre_generation, champ_mot_de_passe):
        try:
            longueur = int(longueur)
            mode = int(mode)
            mot_de_passe_genere = self.generer_mot_de_passe(longueur, mode)

            # Insérer le mot de passe généré dans le champ de mot de passe de la fenêtre
            champ_mot_de_passe.delete(0, 'end')
            champ_mot_de_passe.insert(0, mot_de_passe_genere)

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides pour la Longueur et le Mode.")

    def copier_mot_de_passe(self, mot_de_passe):
        self.root.clipboard_clear()
        self.root.clipboard_append(mot_de_passe)
        self.root.update()
        messagebox.showinfo("Copié", "Mot de passe copié dans le presse-papiers.")
    
    def executer(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ApplicationGestionnaireMotsDePasse()
    app.executer()