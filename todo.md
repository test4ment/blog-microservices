# alembic.ini
sqlalchemy.url = postgresql://user:password@localhost/blog_db

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
