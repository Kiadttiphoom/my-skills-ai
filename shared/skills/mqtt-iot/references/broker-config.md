# Broker configuration

Read when setting up or hardening a broker. Options below are for Mosquitto 2.x; check
`man mosquitto.conf` for your installed version before relying on less common options.

## Mosquitto 2.x defaults that surprise people

- With no `listener` configured, Mosquitto listens on localhost only.
- `allow_anonymous` defaults to `false` once you define listeners in 2.x; clients
  without credentials are refused.
- `per_listener_settings false` (default) means auth settings apply globally. Set it to
  `true` when different listeners need different auth (e.g. local plaintext for a
  bridge, TLS + passwords for devices).

## Production config

```conf
# /etc/mosquitto/conf.d/production.conf
per_listener_settings true

# Local-only plaintext for on-host services
listener 1883 127.0.0.1
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl

# Device listener: TLS + username/password
listener 8883
protocol mqtt
cafile   /etc/mosquitto/certs/ca.pem
certfile /etc/mosquitto/certs/server.pem
keyfile  /etc/mosquitto/certs/server.key
tls_version tlsv1.2
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/acl

persistence true
persistence_location /var/lib/mosquitto/
autosave_interval 300

max_queued_messages 1000      # per-client queue cap for offline persistent sessions
max_inflight_messages 20
message_size_limit 262144     # 256 KB; reject oversized payloads
max_keepalive 300

log_dest syslog
log_type error
log_type warning
log_type notice
connection_messages true
```

## Credentials

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd admin     # -c creates/overwrites the file: only the first time
sudo mosquitto_passwd /etc/mosquitto/passwd dev-a1b2c3
sudo mosquitto_passwd -b /etc/mosquitto/passwd dev-a1b2c4 "$(openssl rand -base64 24)"   # scripted provisioning
sudo chown mosquitto: /etc/mosquitto/passwd && sudo chmod 600 /etc/mosquitto/passwd
sudo systemctl reload mosquitto          # SIGHUP reloads password and ACL files
```

`-c` on an existing file erases every other user — confirm before running it on a live
broker.

## ACL file

```conf
# /etc/mosquitto/acl
# Admin / backend users
user admin
topic readwrite #

user ingest
topic read acme/+/+/telemetry/#
topic read acme/+/+/status
topic read acme/+/+/state

user ops
topic write acme/+/+/cmd/#
topic write acme/+/+/config
topic read  acme/+/+/cmd/+/result

# Device rules: %u = username (must equal device id)
pattern write acme/+/%u/telemetry/#
pattern write acme/+/%u/state
pattern write acme/+/%u/status
pattern read  acme/+/%u/cmd/#
pattern write acme/+/%u/cmd/+/result
pattern read  acme/+/%u/config
```

- Mosquitto denies silently: a subscriber receives nothing rather than an error (MQTT 5
  clients may get a reason code on SUBACK). Test denials explicitly.
- `%c` substitutes the client ID; using `%u` with client ID = username enforced by
  provisioning is simpler to reason about.

## Client certificates (mutual TLS)

```conf
listener 8883
cafile   /etc/mosquitto/certs/device-ca.pem
certfile /etc/mosquitto/certs/server.pem
keyfile  /etc/mosquitto/certs/server.key
require_certificate true
use_identity_as_username true     # certificate CN becomes the username for ACL patterns
```

Issue one certificate per device with CN = device ID. Revoke by CRL (`crlfile`) or by
removing the device from ACLs. Keep the CA private key offline.

## Bridging (edge broker to cloud)

```conf
connection cloud
address broker.example.com:8883
bridge_cafile /etc/mosquitto/certs/ca.pem
remote_username site-plant1
remote_password <secret>
topic acme/plant1/+/telemetry/# out 1
topic acme/plant1/+/cmd/# in 1
cleansession false
```

## Monitoring

- `$SYS/broker/clients/connected`, `$SYS/broker/messages/received`,
  `$SYS/broker/load/messages/received/1min`, `$SYS/broker/store/messages/count`.
- Restrict `$SYS` read access to admin/monitoring users.
- Export to Prometheus with a `$SYS`-based exporter.

## EMQX equivalents

| Concern | EMQX approach |
|---|---|
| Config | `emqx.conf` (HOCON) or the dashboard (port 18083); change the default dashboard password immediately |
| Password auth | Authentication chain: built-in database, or external (PostgreSQL, Redis, HTTP, JWT) |
| ACLs | Authorization sources: built-in rules, file, database, HTTP; `${username}` / `${clientid}` placeholders |
| TLS | `listeners.ssl.default` with `ssl_options` (certfile, keyfile, cacertfile, verify) |
| Shared subscriptions | `$share/<group>/topic` (also `$queue/` legacy) |
| Routing to databases/Kafka | Rule engine + data integrations (availability depends on edition/version) |
| Clustering | Native; plan node discovery (static, DNS, k8s) |

EMQX changed its open-source licensing in recent releases; confirm the license and
feature set of the exact version before committing to it.
