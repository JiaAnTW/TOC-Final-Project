import pymysql

class Model():
    def __init__(self):
        try:
            self.db = pymysql.connect("localhost","waku","0000","waku" )
        except:
            print("database connection fail")
            exit(1)

    def index(self):
        try:
            cursor = self.db.cursor()
        except:
            self._reconnect()
            
        try:
            query = "SELECT * FROM pin"
            cursor.execute(query)
            data = cursor.fetchone()
            print ("data is "+str(data))
        except:
            print("Error when query [index]")

    
    def create_location(self,newSpot):
        try:
            cursor = self.db.cursor()
        except:
            self._reconnect()
        try:    
            query = "INSERT INTO pin(name,\
                address, location) \
                VALUES ('%s', '%s',  geomFromText('POINT(%s)'))"% \
                (newSpot['name'], newSpot['address'], newSpot['location'])
            cursor.execute(query)
            data = cursor.fetchone()
            print ("data is "+str(data))
        except:
            print("Error when query [create_location]")

    
    def _reconnect(self):
        try:
            self.db = pymysql.connect("localhost","waku","0000","waku" )
        except:
            print("Reconnect database fail, program stop")
            exit(1)


    def __del__(self):
        self.db.close()

test=Model()
test.index()