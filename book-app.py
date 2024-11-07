from tkinter import *
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from appDB import addBook as addBookToDB, updateStatus as updateBookStatus, addRating, getBooks, getBookDetails

# ---- Initialize ttkbootstrap Style ----
style = Style("superhero")  # Use 'superhero' theme for a dark look, or try 'cosmo' for light
window = style.master
window.title("Book List App")

# ---- Creating the Tabs ----
tabs = ttk.Notebook(window)

tab1 = Frame(tabs)
tab2 = Frame(tabs)
tab3 = Frame(tabs)
tab4 = Frame(tabs)

tabs.add(tab1, text = "Add a Book")
tabs.add(tab2, text = "Select Category")
tabs.add(tab3, text = "Rate Books")
tabs.add(tab4, text = "View Books")

tabs.pack(fill = BOTH, expand = True)

# ---- Function to Add Book ----
def addBook():
    title = titleEntry.get()
    author = authorEntry.get()
    category = categoryVar.get()

    if title and author and category:
        try:
            addBookToDB(title, author, category)
            titleEntry.delete(0, END)
            authorEntry.delete(0, END)
            updateBookList()
            messagebox.showinfo("Success", "Book added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# ---- Function to Update Book List in Dropdown and All Tabs ----
def updateBookList():
    books = getBooks()
    bookTitles = [book['title'] for book in books]
    
    # -- Update book dropdown in Select Category tab
    bookDropdown['menu'].delete(0, 'end')
    for book in bookTitles:
        bookDropdown['menu'].add_command(label = book, command = lambda value = book: selectedBook.set(value))

    # -- Update listboxes in all relevant tabs
    updateListboxes(books)
    updateViewListbox(books)
    updateRateListbox(books)
    updateAddTabListbox(books)

# ---- Function to Update the Book List in the Add Book Tab ----
def updateAddTabListbox(books):
    bookList.delete(0, END)

    for book in books:
        # -- Format: "Title - Author (Category)"
        entry = f"{book['title']} - {book['author']} ({book['category']})"
        bookList.insert(END, entry)

# ---- Function to Update Listboxes for Select Category Tab ----
def updateListboxes(books):
    wantToReadListbox.delete(0, END)
    currentlyReadListbox.delete(0, END)
    readListbox.delete(0, END)

    for book in books:
        if book['status'] == "Want to Read":
            wantToReadListbox.insert(END, book['title'])
        elif book['status'] == "Currently Reading":
            currentlyReadListbox.insert(END, book['title'])
        elif book['status'] == "Read":
            readListbox.insert(END, book['title'])

# ---- Function to Update the View Books Tab ----
def updateViewListbox(books):
    viewBookListbox.delete(0, END)
    for book in books:
        viewBookListbox.insert(END, book['title'])

# ---- Function to Update the Rate Books Tab ----
def updateRateListbox(books):
    rateBookListbox.delete(0, END)
    for book in books:
        rateBookListbox.insert(END, book['title'])

# ---- Function to Update Book Status ----
def updateStatus(newStatus):
    title = selectedBook.get()
    book = next((b for b in getBooks() if b['title'] == title), None)

    if book:
        try:
            updateBookStatus(book['id'], newStatus)
            updateListboxes(getBooks())
            messagebox.showinfo("Success", f"Status updated to '{newStatus}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")
    else:
        messagebox.showwarning("Warning", "Please select a valid book.")

# ---- Function to Rate a Book ----
def rateBook():
    selection = rateBookListbox.curselection()

    if selection:
        selectedTitle = rateBookListbox.get(selection[0])
        rating = ratingVar.get()

        if rating.isdigit() and 1 <= int(rating) <= 5:
            book = next((b for b in getBooks() if b['title'] == selectedTitle), None)
            if book:
                try:
                    addRating(book['id'], int(rating))
                    messagebox.showinfo("Success", "Rating added successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add rating: {e}")
            else:
                messagebox.showerror("Error", "Book not found.")
        else:
            messagebox.showwarning("Warning", "Please select a valid rating (1-5).")
    else:
        messagebox.showwarning("Warning", "Please select a book to rate.")

# ---- Function to Display Selected Book Details ----
def displayBookDetails(event):
    selection = viewBookListbox.curselection()

    if selection:
        selectedTitle = viewBookListbox.get(selection[0])
        book = next((b for b in getBooks() if b['title'] == selectedTitle), None)
        
        if book:
            viewTitleLabelValue.config(text = book['title'])
            viewAuthorLabelValue.config(text = book['author'])
            viewCategoryLabelValue.config(text = book['category'])
            viewRatingLabelValue.config(text = book['rating'] if book['rating'] else "No Rating")

# ---- Creating the Widgets for the Add Book Tab ----
categoryVar = StringVar()
defaultCategories = [
    "Classics",
    "Romance",
    "Dystopian", 
    "Fiction", 
    "Non-Fiction", 
    "Sci-Fi", 
    "Mystery", 
    "Young-Adult", 
    "Poems", 
    "Horror", 
    "Novels"
]

# -- Add Book Tab Layout
Label(tab1, text = "Title").grid(row = 1, column = 0, padx = 10, pady = 5)
titleEntry = ttk.Entry(tab1)
titleEntry.grid(row = 1, column = 1, padx = 10, pady = 5)

Label(tab1, text = "Author").grid(row = 2, column = 0, padx = 10, pady = 5)
authorEntry = ttk.Entry(tab1)
authorEntry.grid(row = 2, column = 1, padx = 10, pady = 5)

Label(tab1, text = "Select a Category:").grid(row = 3, column = 0, padx = 10, pady = 5)
categoryList = ttk.OptionMenu(tab1, categoryVar, *defaultCategories)
categoryList.grid(row = 3, column = 1, padx = 10, pady = 5)

ttk.Button(tab1, text = "Add Book", command = addBook).grid(row = 5, column = 1, padx = 10, pady = 10)

# -- Book list in Add Book Tab
bookListFrame = Frame(tab1)
bookListFrame.grid(row = 6, column = 0, columnspan = 2)
bookList = Listbox(bookListFrame, width = 50, height = 10)
bookList.pack(side = LEFT)

# ---- Creating the Layout for the Select Categories Tab ----
Label(tab2, text = "Select a Book:").grid(row = 0, column = 0, columnspan = 3, pady = 10)
selectedBook = StringVar()
bookDropdown = ttk.OptionMenu(tab2, selectedBook, "Select a Book")
bookDropdown.grid(row = 1, column = 0, columnspan = 3, pady = 10, padx = 10)

# ---- Want to Read Section ----
Label(tab2, text = "Want to Read").grid(row = 2, column = 0, padx = 10, pady = 5)
wantToReadListbox = Listbox(tab2, width = 20, height = 10)
wantToReadListbox.grid(row = 3, column = 0, padx = 10, pady = 5)
ttk.Button(tab2, text = "Add to Want to Read", command = lambda: updateStatus("Want to Read")).grid(row = 4, column = 0, pady = 5)

# ---- Currently Reading Section ----
Label(tab2, text = "Currently Reading").grid(row = 2, column = 1, padx = 10, pady = 5)
currentlyReadListbox = Listbox(tab2, width = 20, height = 10)
currentlyReadListbox.grid(row = 3, column = 1, padx = 10, pady = 5)
ttk.Button(tab2, text = "Add to Currently Reading", command = lambda: updateStatus("Currently Reading")).grid(row = 4, column = 1, pady = 5)

# ---- Read Section ----
Label(tab2, text = "Read").grid(row = 2, column = 2, padx = 10, pady = 5)
readListbox = Listbox(tab2, width = 20, height = 10)
readListbox.grid(row = 3, column = 2, padx = 10, pady = 5)
ttk.Button(tab2, text = "Add to Read", command = lambda: updateStatus("Read")).grid(row = 4, column = 2, pady = 5)

# ---- Rate Books Tab Layout ----
rateBookListbox = Listbox(tab3, width = 30, height = 15)
rateBookListbox.grid(row = 0, column = 0, padx = 10, pady = 10, rowspan = 5)

Label(tab3, text = "Overall Rating").grid(row = 2, column = 1, sticky = 'w', pady = (20, 5))
ratingVar = StringVar(value = "Select")
ratingDropdown = ttk.OptionMenu(tab3, ratingVar, *[1, 2, 3, 4, 5])
ratingDropdown.grid(row = 2, column = 2, sticky = 'w')
ttk.Button(tab3, text = "Add Rating", command = rateBook).grid(row = 3, column = 2, pady = 10, sticky = 'w')

# ---- View Books Tab Layout ----
viewBookListbox = Listbox(tab4, width = 30, height = 15)
viewBookListbox.grid(row = 0, column = 0, padx = 10, pady = 10, rowspan = 5)
viewBookListbox.bind("<<ListboxSelect>>", displayBookDetails)

Label(tab4, text = "Title:").grid(row = 0, column = 1, sticky = 'w')
viewTitleLabelValue = Label(tab4, text = "")
viewTitleLabelValue.grid(row = 0, column = 2, sticky = 'w')

Label(tab4, text = "Author:").grid(row = 1, column = 1, sticky = 'w')
viewAuthorLabelValue = Label(tab4, text = "")
viewAuthorLabelValue.grid(row = 1, column = 2, sticky = 'w')

Label(tab4, text = "Category:").grid(row = 2, column = 1, sticky = 'w')
viewCategoryLabelValue = Label(tab4, text = "")
viewCategoryLabelValue.grid(row = 2, column = 2, sticky = 'w')

Label(tab4, text = "Rating:").grid(row = 3, column = 1, sticky = 'w')
viewRatingLabelValue = Label(tab4, text = "")
viewRatingLabelValue.grid(row = 3, column = 2, sticky = 'w')

# ---- Initializing Book List ----
updateBookList()
window.mainloop()