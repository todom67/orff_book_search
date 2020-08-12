import wtforms
from wtforms.validators import DataRequired, Optional, URL
from models import Book, LPElement

class LPElementField(wtforms.StringField):
  def _value(self):
    print(self.data)
    if self.data:
      return ', '.join(str(lpe) for lpe in self.data)
    return ''

  def get_lpes_from_string(self, lpe_elist):
    lpe_tags = LPElement.query.order_by(LPElement.value.asc())
    
    lpe_names = [lpe.description for lpe in lpe_tags]
    existing_lpes = [lpe.description for lpe in lpe_tags if lpe.value in lpe_elist]

    new_lpes = set(lpe_names) - set(existing_lpes)

def get_lpe_stuff():
  lpes = LPElement.query.order_by(LPElement.value.asc())
  lpe_dict = {}

  lpe_list = [(lpe.value, lpe.description) for lpe in lpes]
  return lpe_list

class BookForm(wtforms.Form):
  title = wtforms.StringField('Title', validators=[DataRequired()])
  author = wtforms.StringField('Author', validators=[DataRequired()])
  ISBN = wtforms.StringField('ISBN', validators=[DataRequired()])
  storelink = wtforms.StringField('TPT Link', validators=[
        Optional(),
        URL()
    ])
 
  def save_book(self, book):
    self.populate_obj(book)
    print(book)
    return book
