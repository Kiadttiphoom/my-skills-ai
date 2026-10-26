---
name: mqtt-iot
description: Designs and debugs MQTT for IoT fleets — topic hierarchies, QoS selection, retained messages, last will, persistent sessions, MQTT 5 features (session expiry, message expiry, shared subscriptions, reason codes), device client reconnect logic, and broker setup and hardening on Mosquitto 2.x or EMQX with TLS, per-device credentials and ACLs. Use when connecting ESP32, Raspberry Pi or other devices to a broker, designing topic schemes, when clients disconnect in loops, messages are lost or duplicated, retained state goes stale, or when securing a broker exposed to the internet.
license: MIT
---

# MQTT for IoT

Done well means: topics follow one documented scheme, each message type has a chosen
QoS and retain flag with a reason, every device has a unique client ID and its own
credentials restricted by ACL to its own topics, connections use TLS, devices reconnect
with jittered backoff, and offline devices are visible through last-will status.

## Ground rules

- Never expose port 1883 (plaintext) to the internet. Use 8883 with TLS; plaintext only
  on a trusted local network or localhost.
- One identity per device: unique client ID, unique username/cert. Shared credentials
  mean one leaked device compromises the fleet and ACLs cannot isolate devices.
- Duplicate client IDs kick each other off in an endless reconnect loop. Derive the ID
  from hardware (MAC, chip ID, serial).
- Devices subscribe only to their own command topics, never `#`.
- Treat every received payload as untrusted input: validate size, schema, and ranges.

## Workflow

```
- [ ] 1. Write the topic scheme and message catalog (topic, direction, QoS, retain, payload schema)
- [ ] 2. Choose broker and deployment; configure listeners, TLS, auth, ACLs
- [ ] 3. Implement the device client: unique ID, LWT, backoff, session settings
- [ ] 4. Implement backend consumers (shared subscriptions for scale-out)
- [ ] 5. Test with mosquitto_sub/pub; test ACL denials explicitly
- [ ] 6. Failure tests: broker restart, network drop, device power loss, slow consumer
- [ ] 7. Monitor: connected clients, message rates, dropped/queued messages
```

### 1. Topic scheme

```
<org>/<site>/<device-id>/telemetry/<sensor>     device → cloud, frequent
<org>/<site>/<device-id>/state                  device → cloud, retained (current state)
<org>/<site>/<device-id>/status                 "online"/"offline", retained, set by LWT
<org>/<site>/<device-id>/cmd/<command>          cloud → device
<org>/<site>/<device-id>/cmd/<command>/result   device → cloud, response
<org>/<site>/<device-id>/config                 cloud → device, retained desired config
```

Rules: no leading `/` (it creates an empty first level), lowercase, no spaces, device ID
in a fixed position (so ACL patterns work), no personal data in topic names (they show
up in broker logs). Version the payload (`"v": 2`), not the topic, unless the change is
incompatible.

### Message catalog (one row per message type)

```markdown
| Topic | Dir | QoS | Retain | Payload | Rate |
|---|---|---|---|---|---|
| acme/plant1/{id}/telemetry/temp | D→C | 0 | no | {"v":1,"ts":1730000000,"c":21.4} | 1/min |
| acme/plant1/{id}/status | D→C | 1 | yes | "online" / LWT "offline" | on change |
| acme/plant1/{id}/cmd/reboot | C→D | 1 | no | {"id":"uuid","after_s":5} | rare |
| acme/plant1/{id}/config | C→D | 1 | yes | {"v":1,"interval_s":60} | on change |
```

### QoS and retain decisions

| Message | QoS | Retain | Why |
|---|---|---|---|
| Frequent telemetry, next sample supersedes | 0 | no | Loss tolerable, cheapest |
| Telemetry you must not lose (billing, alarms) | 1 + idempotent consumer (dedupe on message id/ts) | no | At-least-once; duplicates possible |
| Commands | 1, with command id and result message | no | Retaining commands replays them on reconnect |
| Current state / desired config | 1 | yes | New subscribers get the latest value immediately |
| Online/offline status | 1 | yes (LWT also retained) | Dashboards see status without waiting |

- QoS 2 is rarely worth it: more round trips and broker state, and end-to-end exactly-once
  still needs idempotency in your app. Prefer QoS 1 + dedupe.
- QoS is per hop: the delivered QoS is the minimum of the publish and the subscription QoS.
- Clear a retained message by publishing an empty payload with retain set.
- Never retain events or commands; a device rebooting next week would execute them.

### 3. Device client essentials

- **LWT**: set at connect: topic `.../status`, payload `offline`, QoS 1, retain. After
  connecting, publish `online` retained to the same topic.
- **Keepalive** 30–60 s; the broker declares the client dead after 1.5× keepalive.
  Shorter keepalive costs battery on cellular/Wi-Fi sleepers.
- **Sessions**: devices that must receive commands sent while offline use a persistent
  session (MQTT 3.1.1 `clean_session=false`; MQTT 5 `clean_start=false` +
  `session_expiry_interval`, e.g. 1 day). Fire-and-forget sensors use clean sessions.
- **MQTT 5 message expiry** on commands (`message_expiry_interval`) prevents stale
  commands executing hours later.
- **Backoff**: reconnect at 1 s, doubling to a cap of 60–300 s, with random jitter, so a
  broker restart does not get stampeded by the whole fleet at once.
- **Offline buffering**: bounded ring buffer on device; drop oldest or downsample when full.
- Time-stamp telemetry on the device (seconds since epoch from NTP/RTC), not on arrival.

Python client (paho-mqtt 2.x requires choosing the callback API version):

```python
import json, random, ssl, time
import paho.mqtt.client as mqtt

DEVICE = "dev-a1b2c3"
BASE = f"acme/plant1/{DEVICE}"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print("connect failed:", reason_code)
        return
    client.publish(f"{BASE}/status", "online", qos=1, retain=True)
    client.subscribe(f"{BASE}/cmd/+", qos=1)

def on_message(client, userdata, msg):
    if len(msg.payload) > 4096:
        return
    cmd = json.loads(msg.payload)
    # validate cmd fields, execute, then publish result to f"{msg.topic}/result"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=DEVICE, protocol=mqtt.MQTTv5)
client.username_pw_set(DEVICE, open("/etc/device/mqtt_password").read().strip())
client.tls_set(ca_certs="/etc/device/ca.pem", tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.will_set(f"{BASE}/status", "offline", qos=1, retain=True)
client.reconnect_delay_set(min_delay=1, max_delay=120)
client.on_connect, client.on_message = on_connect, on_message
client.connect("broker.example.com", 8883, keepalive=60)
client.loop_start()
while True:
    client.publish(f"{BASE}/telemetry/temp", json.dumps({"v": 1, "ts": int(time.time()), "c": 21.4}), qos=0)
    time.sleep(60 + random.uniform(-2, 2))
```

On ESP-IDF use the `esp-mqtt` component (`esp_mqtt_client_init` with `broker.address.uri`
set to `mqtts://...` and the CA cert); it reconnects automatically — set its reconnect
timeout and LWT fields in the config struct.

### 2. Broker choice

| Situation | Broker |
|---|---|
| Single site, up to tens of thousands of clients, simple ops | Mosquitto 2.x |
| Clustering, rule engine, built-in dashboard, large fleets | EMQX (check the license terms of the version you deploy) |
| Fully managed | AWS IoT Core, Azure Event Grid MQTT, HiveMQ Cloud |
| Home automation | Mosquitto add-on with Home Assistant — see home-assistant |

For Mosquitto listener/TLS/password/ACL configuration and EMQX equivalents, read
[references/broker-config.md](references/broker-config.md) when setting up or hardening
a broker.

### 4. Backend consumers

- Scale consumers with MQTT 5 shared subscriptions: `$share/ingest/acme/+/+/telemetry/#`;
  the broker load-balances messages across the group.
- Bridge to a durable log (Kafka, a database) quickly; MQTT brokers are not long-term
  storage.
- Consumers must be idempotent under QoS 1 redelivery.

## Testing commands

```bash
# watch everything for one device (as an admin user with read ACL)
mosquitto_sub -h broker.example.com -p 8883 --cafile ca.pem -u admin -P "$PW" \
  -t 'acme/plant1/dev-a1b2c3/#' -v -F '%I %t %r %q %p'

# send a command with MQTT 5 message expiry (60 s)
mosquitto_pub -h broker.example.com -p 8883 --cafile ca.pem -u ops -P "$PW" -V mqttv5 \
  -t 'acme/plant1/dev-a1b2c3/cmd/reboot' -q 1 -m '{"id":"7f3a","after_s":5}' \
  -D publish message-expiry-interval 60

# prove ACLs: a device must NOT read another device's commands
mosquitto_sub -h broker.example.com -p 8883 --cafile ca.pem -u dev-a1b2c3 -P "$DEVPW" \
  -t 'acme/plant1/dev-zzz/cmd/#' -v     # expect no messages / subscription refused
```

## Debugging table

| Symptom | Likely cause |
|---|---|
| Connect/disconnect loop every few seconds | Duplicate client ID; or keepalive shorter than device's blocking time |
| `Connection refused: not authorised` | Wrong credentials, or Mosquitto 2.x default of no anonymous access |
| Subscribed but receives nothing | ACL denies read (silently on Mosquitto), topic typo, leading slash |
| Commands executed twice | QoS 1 redelivery without idempotency (track command ids) |
| Old command runs after reboot | Retained command or persistent session without message expiry |
| Dashboard shows device online when dead | LWT not set or not retained; keepalive too long |
| Broker memory grows | Persistent sessions for clients that never return; set session expiry and `max_queued_messages` |

## Verification

1. ACL tests: each device can publish/subscribe only under its own ID; cross-device
   attempts fail.
2. Kill a device's power: its `status` turns `offline` within ~1.5× keepalive.
3. Restart the broker: the fleet reconnects over a spread of seconds (jitter), not in
   one spike; persistent-session devices receive queued commands.
4. TLS: `openssl s_client -connect broker.example.com:8883 -servername broker.example.com`
   shows a valid chain; plaintext 1883 is closed from outside.
5. Duplicate-delivery test: replay a QoS 1 command; the device executes it once.
