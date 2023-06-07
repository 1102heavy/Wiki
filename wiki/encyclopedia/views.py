from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Creat a converter that takes a title.md and converts it to html. If title doesn't exist, return error None.
def convert(title):
    # Create a Markdown object
    markdowner = Markdown()

    try:
        # Attempt to convert the entry content to HTML
        return markdowner.convert(util.get_entry(title))
    except TypeError:
        # If an exception is raised (TypeError), it means the entry doesn't exist
        return None

# Create an entry function that takes a title and renders the entry page
def entry(request, title):
    # Check if entry exists
    if convert(title):
        # Prepare the context dictionary for rendering the entry page
        context = {
            "content": convert(title),  # Convert the entry content to HTML
            "title": title,  # Pass the title of the entry
            "error": False  # Indicate that no error occurred
        }
        return render(request, "encyclopedia/entry.html", context)
    else:
        # Prepare the context dictionary for rendering the error page
        context = {
            "message": "The requested page was not found.",
            "title": "Page Error",
            "error": True  # Indicate that an error occurred
        }
        return render(request, "encyclopedia/entry.html", context)

def search(request):
    # Get the query from the search form
    query = request.POST["q"]

    # Check if entry exists
    if convert(query):
        # Redirect to the entry page
        return entry(request, query)
    else:
        # Check for partial matches (substring matches)
        results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        # Prepare the context dictionary for rendering the search page
        context = {
            "query": query,
            "results": results
        }
        return render(request, "encyclopedia/search.html", context)

def create(request):
    if request.method == "POST":
        # Get the title and content of the new entry from the form
        title = request.POST["title"]
        content = request.POST["content"]

        #Check if title is empty
        if title == "":
            context = {
                "message": "Pls enter a title!",
                "title": "Entry Error",
                "error": True  # Indicate that an error occurred
            }
            return render(request, "encyclopedia/error.html", context)
        
        #Check if content is empty
        if content == "":
            context = {
                "message": "Pls enter some content!",
                "title": "Entry Error",
                "error": True  # Indicate that an error occurred
            }
            return render(request, "encyclopedia/error.html", context)

        # Check if an entry with the same title already exists
        if util.get_entry(title):
            # Prepare the context dictionary for rendering the error page
            context = {
                "message": "An entry with the same title already exists.",
                "title": "Entry Exists",
                "error": True  # Indicate that an error occurred
            }
            return render(request, "encyclopedia/entry.html", context)
        else:
            # Save the new entry to disk
            util.save_entry(title, content)
            # Redirect to the entry page
            return entry(request, title)
    else:
        return render(request, "encyclopedia/create.html")
    


def edit(request, title):
    if request.method == "POST":
        # Get the new content of the entry from the form
        content = request.POST["content"]
        # Save the new content to disk
        util.save_entry(title, content)
        # Redirect to the entry page
        return entry(request, title)
    else:
        # Prepare the context dictionary for rendering the edit page
        context = {
            "title": title,
            "content": util.get_entry(title)
        }
        return render(request, "encyclopedia/edit.html", context)
    
def random_page(request):
    # Get a random entry index
    random_entry = random.randint(0, len(util.list_entries()) - 1)
    # Get the title of the random entry
    title = util.list_entries()[random_entry]
    # Redirect to the entry page
    return entry(request, title)
