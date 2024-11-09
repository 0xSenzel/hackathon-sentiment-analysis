import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresConnection:
    def __init__(self, config=None):
        self.config = config or {
            'dbname': 'postgres',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.config['dbname'],
                user=self.config['user'],
                password=self.config['password'],
                host=self.config['host'],
                port=self.config['port']
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            print("Successfully connected to PostgreSQL database")
            return True
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {str(e)}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                return self.cursor.fetchall()
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error executing query: {str(e)}")
            return False

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect() 