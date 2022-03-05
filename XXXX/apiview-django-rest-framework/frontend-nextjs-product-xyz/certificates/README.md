# Details about the self-signed certificate

The certificate is used only for the sole purpose of making the Authorization Code with PKCE work as expected. It must rely on HTTPS. If you are in need to update the certificate, you can issue the following command:

```shell
openssl req -x509 -out localhost.crt -keyout localhost.key \
  -days 1825 \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```

Then with the `local-ssl-proxy` package, you can execute the command `(local-ssl-proxy --source 8002 --target 3000) & next dev` in your package.json.
