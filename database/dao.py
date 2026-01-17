from database.DB_connect import DBConnect
from model.state import State

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                select distinct YEAR(s_datetime) as year
                from sighting s 
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_shapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                select distinct s.shape as shape
                from sighting s 
        """

        cursor.execute(query)

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    select * 
                    from state s  
            """

        cursor.execute(query)

        for row in cursor:
            if row["neighbors"] is None:
                state = State(row["id"], row["lat"], row["lng"], [])
            else:
                state = State(row["id"], row["lat"], row["lng"], row["neighbors"].split())
            result.append(state)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_sightings(y, s):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ 
                select s.state, count(*) as sightings
                from sighting s 
                where s.shape = %s 
                and year(s.s_datetime) = %s
                group by s.state  
                """

        cursor.execute(query, (s, y))

        for row in cursor:
            state = row["state"].upper()
            result[state] = row["sightings"]

        cursor.close()
        conn.close()
        return result