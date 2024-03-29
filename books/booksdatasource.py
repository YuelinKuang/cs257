#!/usr/bin/env python3
'''
    Revised by Yuelin Kuang
    4 October 2022
    
    Implemented by Lucie Wolf and Yuelin Kuang

    booksdatasource.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None, books=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.books = books

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        self.all_books = []
        self.all_authors = []

        with open(books_csv_file_name) as books_csv:
            books_csv = csv.reader(books_csv, delimiter=',')

            for row in books_csv:
                title = row[0]
                year = int(row[1])
                book = Book(title=title, publication_year=year, authors=[])

                #if the book has two authors, splitting the string with the authors' 
                #information by 'and' can separate the two authors.
                authors_in_book = row[2].split(' and ')

                for author in authors_in_book:
                    #after the following line, author will be a list like this: 
                    #[first_name, middle_name, last_name, (birth_year-death_year)] or
                    #[first_name, last_name, (birth_year-death_year)]
                    author = author.split(' ')

                    #getting the second to last element of author for surname
                    #allows multiple first or middle names
                    surname = author[-2]
                    list_of_given_names = [name for name in author[:-2]]
                    given_name = ' '.join(list_of_given_names)

                    #checks if this author is already in this list
                    already_in_list = False
                    for other_author in self.all_authors:
                        if Author(surname = surname, given_name = given_name) == other_author:
                            already_in_list = True

                            other_author.books.append(book)
                            book.authors.append(other_author)

                    #if it's not, add the rest of the information and add it
                    if not already_in_list:
                        years = author[-1][1:-1].split('-')
                        if years[0] == '':
                            birth_year = None
                        else:
                            birth_year = int(years[0])
                        if years[1] == '':
                            death_year = None
                        else:
                            death_year = int(years[1])

                        author_object = Author(surname=surname, given_name=given_name, birth_year=birth_year, \
                                               death_year=death_year, books=[book])
                        self.all_authors.append(author_object)
                        book.authors.append(author_object)
            
                self.all_books.append(book)
                
                


    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        authors_with_search_text = []

        if search_text:
            search_text = search_text.upper()

            for author in self.all_authors:
                given_name_and_surname = ' '.join([author.given_name.upper(), author.surname.upper()])
                if search_text in given_name_and_surname: 
                    authors_with_search_text.append(author)
        else:
            authors_with_search_text = self.all_authors

        return sorted(authors_with_search_text, key = lambda author: (author.surname, author.given_name))

        
        

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        if search_text:
            search_text = search_text.upper()
            books_with_search_text = [book for book in self.all_books if search_text in book.title.upper()]
        else:
            books_with_search_text = self.all_books

        if sort_by == 'year':
            return sorted(books_with_search_text, key = lambda book: (book.publication_year, book.title))
        else:
            return sorted(books_with_search_text, key = lambda book: (book.title))

            


    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        #Raise an exception if the input is not valid (not an integer)
        if (type(start_year) is not int and start_year is not None) or \
           (type(end_year) is not int and end_year is not None):
            raise TypeError('Year should be an integer.')

        books = self.all_books

        books_filtered_by_start_year = []
        books_filtered_by_end_year = []
        
        if start_year is None:
            books_filtered_by_start_year = books
        else:
            for book in books:
                if book.publication_year >= start_year:
                    books_filtered_by_start_year.append(book)

        if end_year is not None:
            for book in books_filtered_by_start_year:
                if book.publication_year <= end_year:
                    books_filtered_by_end_year.append(book)
        else:
            books_filtered_by_end_year = books_filtered_by_start_year

        sorted_books = sorted(books_filtered_by_end_year, key = lambda book: (book.publication_year, book.title))

        return sorted_books