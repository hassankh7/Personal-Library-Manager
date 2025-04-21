
# Bismillah Rahman Rahim

import streamlit as st
import json
import os

st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

# Initialize Library
if "library" not in st.session_state:
    st.session_state.library = []

# Optional file path
LIBRARY_FILE = "library_data.json"

# Load from file (optional)
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as f:
            st.session_state.library = json.load(f)

# Save to file (optional)
def save_library():
    with open(LIBRARY_FILE, "w") as f:
        json.dump(st.session_state.library, f, indent=4)

# Add book
def add_book(title, author, year, genre, read):
    new_book = {
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read
    }
    st.session_state.library.append(new_book)
    save_library()

# Remove book
def remove_book(title):
    st.session_state.library = [book for book in st.session_state.library if book["Title"].lower() != title.lower()]
    save_library()

# Search books
def search_books(query):
    return [
        book for book in st.session_state.library
        if query.lower() in book["Title"].lower() or query.lower() in book["Author"].lower()
    ]

# Display books
def display_books(books):
    for book in books:
        st.markdown(f"**📘 {book['Title']}** by *{book['Author']}* ({book['Year']})")
        st.markdown(f"- Genre: `{book['Genre']}` | Read: {'✅ Yes' if book['Read'] else '❌ No'}")
        st.markdown("---")

# Stats
def show_statistics():
    total = len(st.session_state.library)
    read = len([b for b in st.session_state.library if b["Read"]])
    percent = (read / total * 100) if total > 0 else 0
    st.metric("📚 Total Books", total)
    st.metric("✅ Books Read", f"{percent:.1f}%")

# Load library if not loaded
load_library()

# Sidebar Menu
st.sidebar.title("📚 Menu")
menu = st.sidebar.radio("Choose an action", [
    "Add a Book", "Remove a Book", "Search Books", "View All Books", "View Statistics"
])

# Main Logic
st.title("📖 Personal Library Manager")

if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        if title and author and genre:
            add_book(title, author, int(year), genre, read)
            st.success("Book added successfully!")
        else:
            st.error("Please fill all the required fields.")

elif menu == "Remove a Book":
    st.subheader("❌ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove"):
        remove_book(title)
        st.success("Book removed (if it existed).")

elif menu == "Search Books":
    st.subheader("🔍 Search for a Book")
    query = st.text_input("Enter title or author name to search")
    if query:
        results = search_books(query)
        if results:
            display_books(results)
        else:
            st.warning("No matching books found.")

elif menu == "View All Books":
    st.subheader("📚 All Books in Your Library")
    if st.session_state.library:
        display_books(st.session_state.library)
    else:
        st.info("No books in your library yet.")

elif menu == "View Statistics":
    st.subheader("📊 Library Statistics")
    show_statistics()