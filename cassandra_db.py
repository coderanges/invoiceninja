import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import dotenv

dotenv.load_dotenv()

# Configure Cassandra connection
CASSANDRA_HOSTS = os.environ.get('CASSANDRA_HOSTS', '127.0.0.1').split(',')
KEYSPACE = os.environ.get('CASSANDRA_KEYSPACE', 'invoice_generator')

auth_provider = PlainTextAuthProvider(
    username=os.environ.get('CASSANDRA_USER'),
    password=os.environ.get('CASSANDRA_PASSWORD')
)

cluster = Cluster(
    contact_points=CASSANDRA_HOSTS,
    auth_provider=auth_provider,
    port=9042
)
session = cluster.connect(KEYSPACE)
session.row_factory = dict_factory

# Create tables
session.execute(f"""
    CREATE TABLE IF NOT EXISTS {KEYSPACE}.invoices (
        invoice_id text PRIMARY KEY,
        image text,
        invoice_date text,
        invoice_due_date text,
        items list<text>,
        sub_total decimal,
        tax decimal,
        total decimal,
        created_at timestamp
    )
""")

session.execute(f"""
    CREATE TABLE IF NOT EXISTS {KEYSPACE}.users (
        email text PRIMARY KEY,
        password text,
        created_at timestamp
    )
""")

# Database operations
def add_invoice(data):
    query = """
        INSERT INTO invoices (
            invoice_id, image, invoice_date, invoice_due_date, items,
            sub_total, tax, total, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, toTimestamp(now()))
    """
    prepared = session.prepare(query)
    session.execute(prepared, (
        data['invoice_id'],
        data['image'],
        data['invoice_date'],
        data['invoice_due_date'],
        [str(item) for item in data['items']],
        float(data['sub_total']),
        float(data['tax']),
        float(data['total'])
    ))

def get_invoice(invoice_id):
    query = "SELECT * FROM invoices WHERE invoice_id = ?"
    prepared = session.prepare(query)
    result = session.execute(prepared, [invoice_id])
    return result.one()

def get_user(email):
    query = "SELECT * FROM users WHERE email = ?"
    prepared = session.prepare(query)
    result = session.execute(prepared, [email])
    return result.one()

def add_user(data):
    query = """
        INSERT INTO users (email, password, created_at)
        VALUES (?, ?, toTimestamp(now()))
    """
    prepared = session.prepare(query)
    session.execute(prepared, (
        data['email'],
        data['password']
    ))