import sys
sys.path.insert(0, "/home/chmullig/webapps/mdb/htdocs/")
from phoneserver import app as application
application.config['MDB_FILE'] = "/home/chmullig/webapps/mdb/htdocs/mdb-cs3157-www"
