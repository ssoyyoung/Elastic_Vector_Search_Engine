import pymysql
import time
from sshtunnel import SSHTunnelForwarder

ssh_pkey = '/home/piclick.pem'

class Mysql():
  def __init__(self):
    self.remote_bind_address = (
        'p-kr-main-db.cluster-cfb73nu5n703.ap-northeast-2.rds.amazonaws.com', 3306)
    self.local_bind_address = ('127.0.0.1', 3308)

  def connectdb(self):
    tunnel = SSHTunnelForwarder(('15.165.153.49', 22),  # SSH hosting server
                                ssh_username='ubuntu',
                                ssh_pkey=ssh_pkey,
                                remote_bind_address=self.remote_bind_address,  # addr which SSH server can access
                                local_bind_address=self.local_bind_address)  # mapping addr which python will access

    tunnel.start()
    time.sleep(1)

    conn = pymysql.connect(host=tunnel.local_bind_host,
                            port=tunnel.local_bind_port,
                            user='piclick',
                            passwd='psr9566!',
                            db='piclick')
    return tunnel, conn

  def dbClose(self, tunnel, cur):
    cur.close()
    tunnel.close()

  def getProductInfo(self, pkeys):
    tunnel, conn = self.connectdb()
    cur = conn.cursor()

    try:
      cur.execute("SELECT COUNT(*) FROM `product_list` WHERE STATUS=1 AND cat_key='WC13'")
      products = cur.fetchall()
      
      return products
    except Exception as e:
      print(e)
    finally:
      self.dbClose(tunnel, cur)
