import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


DB_CONFIG = {
    'dbname': 'mygarden_planner',
    'user': 'iris',  
    'password': '',      
    'host': 'localhost',
    'port': 5432
}

def create_garden(name):
    garden_id = None
    
    conn = None 
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        
        cur = conn.cursor()
        
        sql = "INSERT INTO gardens (name) VALUES (%s) RETURNING id"
        cur.execute(sql, (name,))
        

        result = cur.fetchone()  
        if result:
            garden_id = result[0] 
        
        conn.commit()
        print(f"successful! gardenid:{garden_id}")

    except Exception as e:
        print(f"error:{e}")
 
        if conn:
            conn.rollback()
    

    finally:
        if conn:
         
            cur.close()
            conn.close()
    
  
    return garden_id

# def get_all_gardens():

#     gardens=[]
    
#     conn = None
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cur = conn.cursor()
       
#         sql = "SELECT id, name, created_at, updated_at  FROM gardens ORDER BY updated_at DESC"
#         cur.execute(sql)
#         gardens = cur.fetchall()
#         print(f"get{len(gardens)}gardens:{gardens}")
    
#     except Exception as e:
#         print(f"error:{e}")
    
#     finally:
#         if conn:
#             cur.close()
#             conn.close()
    
#     return gardens

def get_all_gardens():
    gardens = []
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor) 
        cur = conn.cursor()
        
        sql = "SELECT id, name, created_at, updated_at FROM gardens ORDER BY updated_at DESC"
        cur.execute(sql)
        gardens = cur.fetchall()
        print(f"get {len(gardens)} gardens: {gardens}")
    
    except Exception as e:
        print(f"error: {e}")
    
    finally:
        if conn:
            cur.close()
            conn.close()
    
    return gardens
    
    
def save_garden_plants(garden_id, plants): 
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
      
        del_sql = "DELETE FROM plants WHERE garden_id=%s"
        cur.execute(del_sql, (garden_id,))  
        
        
        for plant in plants:
            insert_sql = """
                INSERT INTO plants (garden_id, plant_id, plant_type, x, y, width, height)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            plant_data = (
                garden_id,
                plant['id'],
                plant['type'],
                plant['x'],
                plant['y'],
                plant['width'],
                plant['height']
            )
            cur.execute(insert_sql, plant_data)
        
        
        update_sql = "UPDATE gardens SET updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        cur.execute(update_sql, (garden_id,))  
        
        conn.commit()
        print(f"Saved {len(plants)} plants to garden {garden_id}")
    
    except Exception as e:
        print(f"Failed to save: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            cur.close()
            conn.close()
    
def load_garden_plants(garden_id):
   
    plants = []
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor) 
        cur = conn.cursor()
        
      
        sql = "SELECT plant_id, plant_type, x, y, width, height FROM plants WHERE garden_id = %s"
        cur.execute(sql, (garden_id,))
        
        
        plants = cur.fetchall()
        print(f"load{garden_id}:{plants}")
    
    except Exception as e:
        print(f"error:{e}")
    
    finally:
        if conn:
            cur.close()
            conn.close()
    
    return plants

def delete_garden(garden_id):

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
   
        sql = "DELETE FROM gardens WHERE id = %s"
        cur.execute(sql, (garden_id,))
        
        conn.commit()
        print(f"Deleted garden {garden_id}")
    
    except Exception as e:
        print(f"Failed to delete garden: {e}")
        if conn:
            conn.rollback()
        raise e
    
    finally:
        if conn:
            cur.close()
            conn.close()


