import tkinter as tk
from tkinter import messagebox, PhotoImage
import requests

#---- NOTES ----#
'''Import tkinter is a python library. Importing a messagebox allows for pop-up messages to happen. 
PhotoImage allows for the handling of photos.'''
#---- Line 1-3 ---#


#data model
class Pokemon:
    #represents a Pokémon with name, id, types.
    def __init__(self, name, poke_id, types):
        self.name = name
        self.id = poke_id
        self.types = types

#---- NOTES ----#
'''This creates a new object acting as a blueprint for the program. it uses the constructor _init_. 
It contains the name, id, and types of the pokemon.'''
#---- Line 12-18 ----#

#api comms
class PokemonAPI:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    @classmethod
    def get_pokemon(cls, name_or_id):

        try:
            response = requests.get(cls.BASE_URL + name_or_id.lower())

            if response.status_code != 200:#If none is found, a mesage is given to alert user.
                return None
            
            data = response.json() #converts data into a python dictionary
            name = data["name"]
            poke_id = data["id"]
            types = [t["type"]["name"] for t in data["types"]]

            return Pokemon(name, poke_id, types)
    
        except requests.RequestException: 
         #If there is no internet, this will help the application not crash out and instead just returns 'None'.
            return None


#---- NOTES ----#
''' The new class ancapuslate the base url for the pokemon library used in thsi application. 
It has the class method used for finding the name or id of the pokemon when typed in by the user. 
This combined with the try function combines the information by the user and the base url making 
a complete url that will locate the specific data from the library.'''
#---- Line 25-44 ----#


#gui app
class PokemonApp:
    def __init__(self, root): #App gui. Mian Window
        self.root = root
        self.root.title("Pokédex.moe")
        self.root.configure(bg="black")  

        #bg img
        self.bg_image = tk.PhotoImage(file="pokemon_bg.png")
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #fixed window
        window_size = 400
        self.root.geometry(f"{window_size}x{window_size}")
        self.root.resizable(False, False)

        #favicon
        icon = PhotoImage(file="pokedex_icon.png")
        self.root.iconphoto(False, icon)

        #center frame
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_columnconfigure(0, weight=0)

        self.frame = tk.Frame(
            self.root,
            bg="#000000",
            relief="solid",
            highlightbackground="#3B4CCA",
            highlightcolor="#3B4CCA",
            highlightthickness=3,
        )
        self.frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)

        #search label
        tk.Label(
            self.frame,
            text="Search Pokémon by Name or ID",
            font=("Impact", 18),
            fg="#CC0000",
            bg="#000000",
        ).grid(row=0, column=0, pady=(10, 5))

        #entry
        self.entry = tk.Entry(
            self.frame,
            font=("Impact", 16),
            fg="#CC0000",
            bg="#FFCB05",
            highlightbackground="#3B4CCA",
            highlightcolor="#3B4CCA",
            highlightthickness=2,
            width=20,
        )
        self.entry.grid(row=1, column=0, pady=(0, 10), ipadx=10)

        #search button
        self.search_button = tk.Button(
            self.frame,
            text="SEARCH",
            font=("Impact", 15),
            fg="#CC0000",
            bg="#3B4CCA",
            relief="flat",
            bd=0,
            command=self.search,
        )
        self.search_button.grid(row=2, column=0, pady=(0, 10))

        #hover effect
        self.search_button.bind("<Enter>", self.on_hover)
        self.search_button.bind("<Leave>", self.off_hover)

        #info labels
        self.name_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.type_var = tk.StringVar()

        tk.Label(
            self.frame, textvariable=self.name_var, font=("Impact", 16), fg="#FFCB05", bg="#000000"
        ).grid(row=3, column=0)
        tk.Label(
            self.frame, textvariable=self.id_var, font=("Impact", 16), fg="#FFCB05", bg="#000000"
        ).grid(row=4, column=0)
        tk.Label(
            self.frame, textvariable=self.type_var, font=("Impact", 16), fg="#FFCB05", bg="#000000"
        ).grid(row=5, column=0)

    #hover functions
    def on_hover(self, event):
        self.search_button.config(bg="#B3A125")

    def off_hover(self, event):
        self.search_button.config(bg="#3B4CCA")

    #search function using pokemon object
    def search(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Error", "Enter a name or ID.")
            return

        #get pokemon object
        pokemon = PokemonAPI.get_pokemon(query)
        if not pokemon:
            messagebox.showerror("Error", "Pokémon not found.")
            return

        # update label with pokemon data
        self.name_var.set(f"Name: {pokemon.name.capitalize()}")
        self.id_var.set(f"ID: {pokemon.id}")
        self.type_var.set(f"Types: {', '.join(pokemon.types)}")


#main program
if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()
