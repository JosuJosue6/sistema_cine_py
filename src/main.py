from tkinter import Tk
from views.movie_list_view import MovieListView

def main():
    root = Tk()
    root.title("Test")
    root.geometry("800x600")

    # Crear la vista de la lista de películas
    movie_list_view = MovieListView(root)
    # Empaquetar la vista
    movie_list_view.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()