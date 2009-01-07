"""

<cocooncrash> encoding='utf-8' - the encoding to use for all Unicode translations, both by engine-wide unicode conversion as well as the Unicode type object.
[Tue Jan 6 2009] [21:06:02] <cocooncrash> convert_unicode=False - if set to True, all String/character based types will convert Unicode values to raw byte values going into the database, and all raw byte values to Python Unicode coming out in result sets. This is an engine-wide method to provide unicode conversion across the board. For unicode conversion on a column-by-column level, use the Unicode column type instead, described in The
[Tue Jan 6 2009] [21:06:09] <cocooncrash> Types System.
[Tue Jan 6 2009] [21:06:14] <cocooncrash> assert_unicode=False - When set to True alongside convert_unicode=True, asserts that incoming string bind parameters are instances of unicode, otherwise raises an error. Only takes effect when convert_unicode==True. This flag is also available on the String type and its descendants. New in 0.4.2.
[Tue Jan 6 2009] [21:06:46] <cocooncrash> So, try "encoding='latin1'", then 'iso-8859-1', then 'iso-8859-15'
[Tue Jan 6 2009] [21:06:56] <cocooncrash> If none of those work, fiddle with the other unicode settings.
[Tue Jan 6 2009] [21:08:36] <TRB143> Tried the other settings but will try the encoding ones thanks.
"""

from sqlalchemy import  *
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.types import Text, Unicode
import sqlite3

from openlp.plugins.songs.lib.songtable import Author

metadata = MetaData()

author_table = Table('authors', metadata, 
    Column('authorid', Integer, primary_key=True), 
    Column('authorname', Unicode(length=40)), 
    Column('first_name', Unicode(length=40)), 
    Column('last_name',Unicode(length=40)),     
)
    
#mapper(Author,author_table)
class test0():
    def __init__(self):
        self.conn = sqlite3.connect("testdb/danish.sqlite")
        self.conn.text_factory = str        

    def test1(self):
        c = self.conn.cursor()
        text = c.execute("""select * from authors""") .fetchall()
        print text

class test1():
    def __init__(self):
        self.db = create_engine("sqlite:///testdb/danish.sqlite", encoding='latin1' , convert_unicode=False, assert_unicode=False)
        self.db.echo = True
        self.db.convert_unicode=False
        metadata.bind = self.db
        metadata.bind.echo = True
        self.Session = sessionmaker(autoflush=True, autocommit=False)
        self.Session.configure(bind=self.db)

    def test1(self):
        session = self.Session()
        print session.query(Author).order_by(Author.authorname).all()
        
if __name__ == '__main__':
    app = test0()
    app.test1()   
    app = test1()
    app.test1()
