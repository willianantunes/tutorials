# DNS Server with Bind9 and dnsmasq

To understand it, please read the article [Understanding DNS behavior with Bind9 and dnsmasq](https://www.willianantunes.com/blog/2024/03/understanding-dns-behavior-with-bind9-and-dnsmasq/).

## Start DNS Servers with zone `privatelink.database.windows.net`

Run the following command to start servers A and B:

```shell
docker compose up -d dns-a dns-b
```

## DNS Proxy with bind9

Run the server:

```shell
docker compose up dns-initial
```

In another terminal, you can query the `dns-initial` with the following commands:

```shell
dig -t A @127.0.0.1 -p 30010 willianantunes.com
dig -t A @127.0.0.1 -p 30010 db-a.privatelink.database.windows.net
dig -t A @127.0.0.1 -p 30010 db-b.privatelink.database.windows.net
```

## DNS Proxy with dnsmasq

Run the server:

```shell
docker compose up dns-initial-dnsmasq
```

In another terminal, you can query the `dns-initial-dnsmasq` with the following commands:

```shell
dig -t A @127.0.0.1 -p 30005 willianantunes.com
dig -t A @127.0.0.1 -p 30005 db-a.privatelink.database.windows.net
dig -t A @127.0.0.1 -p 30005 db-b.privatelink.database.windows.net
```

Sometimes the query will return `NXDOMAIN` either for `db-a` or `db-b`. This happens because the DNS Proxy returns the first answer it receives. Learned it from a [reddit post](https://www.reddit.com/r/dns/comments/1b1klcq/comment/ksfg2bx/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button).
