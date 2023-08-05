# sqlite db functionality
import sqlite3 as lite

class SqliteDB:
  def __init__(self, bot=None):
    self.bot = bot

    self._prepare_database()

    self.con.close()


  def _prepare_database(self):
    # perhaps TODO
    self.con = lite.connect(self.bot.conf.getNick(self.bot.network) + ".db", check_same_thread=False)
    self.cur = self.con.cursor()
    self.cur.execute('CREATE TABLE IF NOT EXISTS admins (id INT PRIMARY KEY, username CHAR(32) DEFAULT NULL UNIQUE)') 
    self.cur.execute('CREATE TABLE IF NOT EXISTS img (id INT PRIMARY KEY, url CHAR(128) DEFAULT NULL, user CHAR(32) DEFAULT NULL, time DATETIME DEFAULT CURRENT_TIMESTAMP, channel CHAR(32) DEFAULT NULL)')
    self.cur.execute('CREATE TABLE IF NOT EXISTS lastfm (lastfm_username CHAR(64) NOT NULL, nick CHAR(32) NOT NULL)')
    self.cur.execute('CREATE TABLE IF NOT EXISTS qdb (id INT PRIMARY KEY, quote TEXT NOT NULL, date DATETIME DEFAULT CURRENT_TIMESTAMP)')
    self.cur.execute('CREATE TABLE IF NOT EXISTS qdb_votes (vote_id PRIMARY KEY, quote_id INT NOT NULL, votes INT DEFAULT 0)')


  def _open(self):
    self.con = lite.connect(self.bot.conf.getNick(self.bot.network) + ".db", check_same_thread=False)
    self.cur = self.con.cursor()

  def e(self, sql):
    try:
      self._open()
      self.cur.execute(sql) 
      if "INSERT" in sql or "REPLACE" in sql:
        self.con.commit()
        self.con.close()
      elif "SELECT" in sql:
        e = self.cur.fetchall()
        self.con.close()
        return e
    except Exception, e:
      print e
      self.con.rollback()
      self.con.close()
      return None

  def _insertImg(self, user, url, channel):
    self._open()
    if user == "" or user == None:
      user = "nobody"

    self.cur.execute("INSERT INTO img (user, url, channel) VALUES (?, ?, ?)", (user, url, channel))
    self.con.commit()

    self.con.close()

  def _getImgs(self):
    self._open()
    try:
      self.cur.execute("SELECT * FROM img ORDER BY time DESC")
      data = self.cur.fetchall()
      self.con.close()
    except:
      self.con.close()
      return None

    return data

  def _isAdmin(self, username):
    self._open()
    try:
      self.cur.execute("SELECT * FROM admins WHERE username = ?",(username))
      data = self.cur.fetchall()
      self.con.close()
    except:
      self.con.close()
      return None

    return data
