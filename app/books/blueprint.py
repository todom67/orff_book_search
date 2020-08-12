from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from models import Book, LPElement
from books.forms import BookForm

books = Blueprint('books',__name__, template_folder='templates')

def get_book_or_404(id):
  return Book.query.filter(Book.id == id).first_or_404()

def get_lpes():
  return LPElement.query.all()

def add_highlight(the_string, kw):
  kw_index = the_string.lower().find(kw.lower())
  if kw_index < 0:
    return False
  first_slice = the_string[:kw_index]
  second_slice = the_string[kw_index:kw_index + len(kw)]
  third_slice = the_string[kw_index + len(kw):]
  return f"{first_slice}<mark style=\"background-color: tomato;\">{second_slice}</mark>{third_slice}"

@books.route('/')
def index():
  search = request.args.get('q')
  if search:
    the_books = Book.query.filter(
      (Book.title.contains(search)) |
      (Book.author.contains(search)))
  else:
    the_books = Book.query.order_by(Book.title.asc())

  bl = [book for book in the_books]
  
  if search:
    if len(bl) == 0:
      flash(f"Your search on '{search}' yielded no results","danger")
    else:
      flash(f"Your search on '{search}' returned {len(bl)} books!","success")
      # process keywords here
      for the_book in bl:
        if add_highlight(the_book.title, search):
          the_book.title = add_highlight(the_book.title, search)
        elif add_highlight(the_book.author, search):
          the_book.author = add_highlight(the_book.author, search)
        else:
          print("WHA??")
  
  return render_template('books/index.html', object_list=bl) 

from app import db
@books.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
  if request.method == 'POST':
    if request.form.getlist("lp_checkbox"):
      form = BookForm(request.form)
      if form.validate():
        lpelements = sum(list(map(int, request.form.getlist("lp_checkbox"))))
        book = form.save_book(Book())
        book.lpelement_id = lpelements
        db.session.add(book)
        db.session.commit()
        flash(f"Book {book.title} created successfully.", "success")
        return redirect(url_for('books.detail', id=book.id))
    else:
      flash("You must select at least one Learning Plan Element","danger")
      return redirect(url_for('books.create'))
  else:
    form = BookForm()

  return render_template('books/create.html', form=form, lpes=get_lpes())

@books.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
  book = get_book_or_404(id)
  if request.method == 'POST':
    if request.form.getlist("lp_checkbox"):
      form = BookForm(request.form, obj=book)
      if form.validate():
        lpelements = sum(list(map(int, request.form.getlist("lp_checkbox"))))
        book = form.save_book(Book())
        book.lpelement_id = lpelements
        db.session.add(book)
        db.session.commit()
        flash(f"Book {book.title} has been updated.", "success")
        return redirect(url_for('books.detail', id=book.id))
    else:
      flash("You must select at least one Learning Plan Element","danger")
      return redirect(url_for('books.edit', id=book.id))
  else:
    form = BookForm(obj=book)
  
  return render_template('books/edit.html', book=book, form=form, lpes=get_lpes())

@books.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
  book = get_book_or_404(id)
  if request.method == 'POST':
    db.session.delete(book)
    db.session.commit()
    flash(f"Book {book.title} has been deleted.", "success")
    return redirect(url_for('books.index'))

  return render_template('books/delete.html', book=book)

@books.route('/<int:id>/detail')
def detail(id):
  book = get_book_or_404(id)
  return render_template('books/detail.html', book=book, lpes=get_lpes())

@books.route('/lpsearch/', methods=['GET', 'POST'])
def lpsearch():
  return render_template('books/lpsearch.html', lpes=get_lpes())

@books.route('/lpresults/', methods=['GET', 'POST'])
def lpresults():
  if request.method == 'POST':
    if request.form.get("LPElementSearchAll"):
      if request.form.getlist("lp_checkbox"):
        search_terms = list(map(int, request.form.getlist("lp_checkbox")))
        lpelements = sum(search_terms)
        query = Book.query.filter(Book.lpelement_id.op('&')(lpelements) == lpelements)
      else:
        flash("You must select at least one Learning Plan Element","danger")
        return redirect(url_for('books.lpsearch'))

    if request.form.get("LPElementSearchAny"):
      if request.form.getlist("lp_checkbox"):
        search_terms = list(map(int, request.form.getlist("lp_checkbox")))
        lpelements = sum(search_terms)
        query = Book.query.filter(Book.lpelement_id.op('&')(lpelements) != 0)
      else:
        flash("You must select at least one Learning Plan Element","danger")
        return redirect(url_for('books.lpsearch'))
  
    bl = [book for book in query]

    if len(bl) == 0:
      flash(f"Your search yielded no results, click your browsers back button and try removing some Learning Plan Elements","danger")
    else:
      flash(f"Your search returned {len(bl)} books!","success")

  return render_template('books/lpresults.html', object_list=bl, lpes=get_lpes(), search_terms=search_terms) 
