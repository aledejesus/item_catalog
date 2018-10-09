-- Creating a password like this is not safe. This is only made
-- for demonstration purposes.
CREATE ROLE vagrant
  WITH PASSWORD 'password'
  NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN;