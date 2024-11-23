-- https://www.postgresql.org/docs/current/ssl-tcp.html#SSL-SERVER-FILES
ALTER SYSTEM SET ssl_cert_file TO '/var/lib/postgresql/data/postgresql-server-chain.crt';
ALTER SYSTEM SET ssl_key_file TO '/var/lib/postgresql/data/postgresql-server.key';
ALTER SYSTEM SET ssl TO 'ON';
