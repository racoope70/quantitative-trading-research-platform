# C3 Environment-Variable and Secret-Reference Contract

Status: `HOST_NEUTRAL_STATIC_PREPARATION`

This contract is limited to C3 environment identity, configuration identity, and offline diagnostics. It does not authorize provider, broker, market-data, dataset, model, order, or trading activity.

| Variable / class | Classification | C3 rule |
|---|---|---|
| `C3_EVIDENCE_DIRECTORY` | Optional nonsecret | Relative local development-evidence path only; default `.c3-evidence`. It is not scientific-host evidence. |
| `C3_OFFLINE_REQUIRED` | Optional nonsecret | Defaults to `true`; `false` is rejected. |
| Package-source credentials | Prohibited | No credentials are permitted for the accepted public package-source allowlist. |
| Provider secret names such as `APCA_API_KEY_ID` / `APCA_API_SECRET_KEY` | Provider-specific deferred / secret reference | Values are prohibited during C3 and must not be read by C3 code. Names are retained only as historical evidence. |
| Broker credentials | Broker-specific prohibited | No value or operational setting is permitted during C3. |
| Market-data credentials | Later-phase deferred | No value or operational setting is permitted during C3. |
| Dataset/model/holdout/execution/trading settings | Later-phase deferred | Must not become operational C3 settings. |

No credential value may be committed, emitted in diagnostics, or written to test output. The host-neutral C3 configuration implementation rejects operational/provider/broker-prefixed environment values rather than silently accepting them.
