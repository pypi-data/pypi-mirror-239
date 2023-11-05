# Certbot DNS Authenticator for PowerDNS

PowerDNS DNS Autenticator plugin for Certbot DNS-01 challenge.

This plugin uses the PowerDNS HTTP REST API.

## Install

```
pip install certbot-dns-powerdns-bbr
```

## Usage

Create credential file.

```
mkdir -m 600 /etc/letsencrypt/.secret
touch /etc/letsencrypt/.secret/dns-powerdns-bbr.ini
chmod 600 /etc/letsencrypt/.secret/dns-powerdns-bbr.ini
```

/etc/letsencrypt/.secret/dns-powerdns-bbr.ini
```ini:/etc/letsencrypt/.secret/dns-powerdns-bbr.ini
dns_powerdns_bbr_endpoint = http://localhost:8081
dns_powerdns_bbr_server_id = localhost
dns_powerdns_bbr_api_key = <Your API Key>
```

Run certbot certonly with credentials file path.

```
certbot certonly \
  --authenticator dns-powerdns-bbr \
  --dns-powerdns-bbr-credentials /etc/letsencrypt/.secret/dns-powerdns-bbr.ini \
  --dns-powerdns-bbr-propergation-seconds 60 \
  -d 'your.1st.domain.here' \
  -d 'your.2nd.domain.here'
```
