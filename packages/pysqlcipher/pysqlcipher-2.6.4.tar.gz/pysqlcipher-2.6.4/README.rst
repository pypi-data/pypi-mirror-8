pysqlcipher
===========

This library is a fork of pysqlite.
It is still in beta state (although it's strongly used in development in some
linux environments). It links against against libsqlcipher.

Original code (c) 2004-2007 Gerhard Häring

Packaging for SQLCipher (c) 2013-2014 Kali Kaneko


Usage
-----
You have to pass the ``PRAGMA key`` before doing any operations::

  from pysqlcipher import dbapi2 as sqlite
  conn = sqlite.connect('test.db')
  c = conn.cursor()
  c.execute("PRAGMA key='test'")
  c.execute('''create table stocks (date text, trans text, symbol text, qty real, price real)''')
  c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
  conn.commit()
  c.close()

You can quickly verify that your database file in indeed encrypted::

  hexdump -C test.db                                                                                                        
  ab 7f 61 7a 33 9d 07 f4  08 68 c9 b0 4f e3 34 60  |..az3....h..O.4`|
  bb 9d 9c 3d 9e ce 69 57  b6 2f 36 c4 fd 13 bd 61  |...=..iW./6....a|
  77 bf e3 1d 65 b5 ea f7  d2 fc 98 31 23 66 a0 1e  |w...e......1#f..|
  a4 4f fa 66 49 36 84 a1  3e 0c 21 98 84 07 eb 07  |.O.fI6..>.!.....|

Build against libsqlcipher
--------------------------

For convenience, this package uses a sqlcipher amalgamation during the regular
install. See https://www.sqlite.org/amalgamation.html

For production use, you should build against ``libsqlcipher`` installed in your
system, you can do it like this::

  python setup.py build_sqlcipher

And then::

  python setup.py install
