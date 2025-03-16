# Invoice Ninja

Simple Invoicing App

## Tech Stack

- Flask
- Cassandra
- ImgBB

# Local Installation

> Clone to the local machine using git

```
git clone https://github.com/coderanges/invoiceninja.git
```
> change directory and install depedencies using below commands

```
cd invoiceninja
pip install -r requirements.txt
```
> Database and Image hosting
### Cassandra
Install Cassandra from [here](https://cassandra.apache.org/download/)
### ImgBB
you can sign up at [ImgBB](https://imgbb.com/) and get your API key and then set it as env variable `ImgBB_API_KEY`

> Create .env file and add the following variables
# Configuration
```
CASSANDRA_HOSTS=127.0.0.1
CASSANDRA_KEYSPACE=invoice_generator
CASSANDRA_USER=cassandra
CASSANDRA_PASSWORD=cassandra
SECRET_KEY=your_secret_key
ImgBB_API_KEY=your_api_key
```

> Run local server using
### Linux based OS
```
python3 index.py
```
### MacOS
```
python index.py OR python3 index.py
```
### Windows
```
py index.py
```

> Now open any browser on your computer and enter this link `http://127.0.0.1:8082` and press enter.

You should be able to see the app running.

## License

[License](https://github.com/coderanges/invoiceninja.git)
