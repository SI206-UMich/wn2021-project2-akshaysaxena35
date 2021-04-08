from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website)
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    # url = "search_results.htm"
    # r = requests.get(url)
    root_path = os.path.dirname(os.path.abspath(__file__))
    fullfilename = os.path.join(root_path, filename)
    soup = BeautifulSoup(open(fullfilename), 'html.parser')

    title_list = soup.find_all('span', {'itemprop':'name'}, role = True)
    author_list = soup.find_all('span', {'itemprop':'author'})

    soup.decompose()

    final_list = []

    for x in range(len(author_list)):
        title = str.strip(title_list[x].text)
        author = str.strip(author_list[x].text)
        author = author.replace("\n", "")
        final_list.append((title, author))

    # print("final list:", final_list)
    # print("authorlist size:", len(author_list))
    # print("titlelist size:", len(title_list))
    return final_list


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to
    your list, and , and be sure to append the full path to the URL so that the url is in the format
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    url_list = soup.find_all('a', {'class':'bookTitle'})
    final_list = []

    for link in url_list:
        final_list.append('https://www.goodreads.com' + link['href'])

    return final_list[0:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.find('h1', {'id':'bookTitle'})
    author = soup.find('span', {'itemprop':'name'})
    numpages = soup.find('span', {'itemprop':'numberOfPages'})

    # print("numpages:", numpages)
    # print("numpages text:", numpages.text)
    splitpages = numpages.text.split()
    pages = int(splitpages[0])


    book_tuple = (str.strip(title.text), author.text, pages)
    return book_tuple


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a
    filepath and return a list of (category, book title, URL) tuples.

    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
    to your list of tuples.
    """
    root_path = os.path.dirname(os.path.abspath(__file__))
    fullfilename = os.path.join(root_path, filepath)
    soup = BeautifulSoup(open(fullfilename), 'html.parser')

    genre_list = soup.find('div', {'class':'categoryContainer'}).find_all('h4', {'class':'category__copy'})
    title_list = soup.find('div', {'class':'categoryContainer'}).find_all('img', {'class':'category__winnerImage'}, alt=True)
    url_list = soup.find('div', {'class':'categoryContainer'}).find_all('a', href=True)

    final_url_list = []
    for link in url_list:
        if link['href'].endswith("0"):
            final_url_list.append(link['href'])

    final_list = []
    for x in range(len(genre_list)):
        final_genre = str.strip(genre_list[x].text)
        final_title = title_list[x]['alt']
        final_url = final_url_list[x]
        final_list.append((final_genre, final_title, final_url))

    return final_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Book title", "Author Name"])
        for dataitem in data:
            # print("dataitem:", dataitem)
            writer.writerow([dataitem[0], dataitem[1]])


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles_list = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles_list), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(titles_list), type([]))
        # check that each item in the list is a tuple
        self.assertEqual(type(titles_list[0]), type((1, 2)))
        # check that the first book and author tuple is correct (open search_results.htm and find it)

        # check that the last title is correct (open search_results.htm and find it)

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(self.search_urls), type([]))
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        self.assertEqual(type(self.search_urls[0]), type(""))
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in self.search_urls:
            self.assertTrue(url.startswith("https://www.goodreads.com/book/show/"))

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in self.search_urls:
            summaries.append(get_book_summary(url))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        self.assertEqual(type(summaries[0]), type((1,2)))
            # check that each tuple has 3 elements
        self.assertEqual(len(summaries[0]), 3)
            # check that the first two elements in the tuple are string
        self.assertEqual(type(summaries[0][0]), type(""))
        self.assertEqual(type(summaries[0][1]), type(""))
            # check that the third element in the tuple, i.e. pages is an int
        self.assertEqual(type(summaries[0][2]), type(1))
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)
            # assert each item in the list of best books is a tuple
        self.assertEqual(type(best_books[0]), type((1,2)))
            # check that each tuple has a length of 3
        self.assertEqual(len(best_books[0]), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0][0], "Fiction")
        self.assertEqual(best_books[0][1], "The Midnight Library")
        self.assertEqual(best_books[0][2], "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[-1][0], "Picture Books")
        self.assertEqual(best_books[-1][1], "Antiracist Baby")
        self.assertEqual(best_books[-1][2], "https://www.goodreads.com/choiceawards/best-picture-books-2020")

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        datalist = get_titles_from_search_results("search_results.htm")
        # print(datalist)
        # call write csv on the variable you saved and 'test.csv'
        write_csv(datalist, "test.csv")
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        f = open('test.csv', 'r')
        csv_lines = f.readlines()
        f.close()
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(str.strip(csv_lines[0]), "Book title,Author Name")
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(str.strip(csv_lines[1]), "\"Harry Potter and the Deathly Hallows (Harry Potter, #7)\",J.K. Rowling")
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(str.strip(csv_lines[-1]), "\"Harry Potter: The Prequel (Harry Potter, #0.5)\",J.K. Rowling")

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)
