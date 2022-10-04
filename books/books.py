#!/usr/bin/env python3

#Written by Yuelin Kuang & Lucie Wolf

import booksdatasource as bds
import sys

def run_command(args, source):
    if len(args) >= 2:
        if args[1] == 'author':
            return run_author_command(args[2:], source)
        
        if args[1] == 'title':
            return run_title_command(args[2:], source)
            
        if args[1] == 'range':
            return run_range_command(args[2:], source)

    return 'Help' #else, return help


def run_author_command(short_args, source): 
    #short_args is only the relevant arguments (excluding "books.py author")
    #runs the author command using the arguments given by finding out the specific structure of the input

    if len(short_args) == 0 or (len(short_args) == 1 and short_args[0][0] == '_'):
        return source.authors()
    
    if len(short_args) == 1:
        return source.authors(short_args[0])
    
    return 'Help'


def run_title_command(short_args, source): 
    #short_args is only the relevant arguments (excluding "books.py title")
    #runs the title command using the arguments given by finding out the specific structure of the input

    if len(short_args) == 0:
        return source.books()

    if len(short_args) == 1:
        if short_args[0] == '_':
            return source.books()
        if short_args[0][0] == '-':
            if short_args[0] == '-y' or short_args[0] == '--year':
                return source.books(sort_by = 'year')
            return source.books()
        return source.books(short_args[0])
    
    if len(short_args) == 2:
        if short_args[0] == '_':
            if short_args[1] == '-y' or short_args[1] == '--year':
                return source.books(sort_by = 'year')
            return source.books()
        if short_args[1][0] == '-':
            if short_args[1] == '-y' or short_args[1] == '--year':
                return source.books(short_args[0], sort_by = 'year')
            return source.books(short_args[0])
    
    return 'Help'


def run_range_command(short_args, source): 
    #short_args is only the relevant arguments (excluding "books.py range")
    #runs the range_between_years command using the arguments given by finding out the specific structure of the input

    if len(short_args) == 0:
        return source.books_between_years()

    if len(short_args) == 1:
        if short_args[0] == '_':
            return source.books_between_years()
        try: 
            return source.books_between_years(start_year = int(short_args[0]))
        except:
            return 'Help'

    if len(short_args) == 2:
        if short_args[0] == '_':
            if short_args[1] == '_':
                return source.books_between_years()
            try:
                return source.books_between_years(end_year = int(short_args[1]))
            except:
                return 'Help'
        if short_args[1] == '_':
            try:
                return source.books_between_years(start_year = int(short_args[0]))
            except:
                return 'Help'
        else:
            try:
                return source.books_between_years(start_year = int(short_args[0]), end_year = int(short_args[1]))
            except:
                return 'Help'
    return 'Help'

                
def print_output(output):
    '''
    This function takes in the output from run_author_command, run_title_command or 
    run_range_command and prints out the list of books or authors in an organized 
    format. If the input is a string 'Help', it will print out the usage statement instead. 
    '''

    print('\n\n')

    if output == 'Help':
        usage = open('usage.txt', 'r')
        print(usage.read())
        usage.close()

    elif output == []:
        print('Nothing found.')
    
    # Check whether output is a list of Author objects or Book objects. 
    elif isinstance(output[0], bds.Author):
        # If output is a list of authors: 
        # Print out every author's name, birth year, and death year, followed by the list of their books 
        for author in output:
            print(f'{author.given_name} {author.surname} ({author.birth_year}-{author.death_year})')
            for book in author.books:
                print(f'   {book.title}, published in {book.publication_year}.')
    
    else:
        # If output is a list of books: 
        # Print out every book's title, publication year, and author(s). 
        for book in output:
            author_string = ''
            for author in book.authors:
                author_string += f'{author.given_name} {author.surname} and '

            print(f'{book.title}, published in {book.publication_year}, written by {author_string[:-5]}.')
   
    print('\n\n')


def main(args):
    source = bds.BooksDataSource('books1.csv')
    output = run_command(args, source)
    print_output(output)
    

if __name__ == '__main__':
    main(sys.argv)