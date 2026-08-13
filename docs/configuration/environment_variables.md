# C3 Environment-Variable and Secret-Reference Contract

Status: `HOST_NEUTRAL_STATIC_PREPARATION`

This contract is limited to C3 environment identity, configuration identity, and offline diagnostics. It does not authorize provider, broker, market-data, dataset, model, order, or trading activity.

| Variable / class | Classification | C3 rule |
|---|---|---|
| `C3_EVIDENCE_DIRECTORY` | Optional nonsecret | Relative local development-evidence path only; default `.c3-evidence`. It is not scientific-host evidence. |
| `C3_OFFLINE_REQUIRED` | Optional nonsecret | Defaults to `true`; `false` is rejected. |
| Package-source credentials | Prohibited | No credentials are permitted for the accepted public package-source allowlist. |
| Provider secret names such as `APCA_API_KEY_ID` / `APCA_API_SECRET_KEY` | Provider-specific deferred / secret reference | Values are prohibited during C3 and must not be read by C3 code. Names are retained only as historical evidence. |
| Known historical universe/data names such as `TICKERS`, `BARS_FEED`, `DATA_TIMEFRAME` | Later-phase deferred / rejected | Explicitly rejected if supplied to the C3 settings boundary. |
| Known historical model/signal/risk names such as `WEIGHT_CAP`, `TAKE_PROFIT_PCT`, `STOP_LOSS_PCT`, `GROSS_CAP` | Later-phase deferred / rejected | Explicitly rejected if supplied to the C3 settings boundary. |
| Known historical execution/trading names such as `DRY_RUN`, `AUTO_RUN_LIVE`, `ORDER_TIMEOUT_SECONDS` | Later-phase deferred / rejected | Explicitly rejected if supplied to the C3 settings boundary. |
| Broker credentials | Broker-specific prohibited | No value or operational setting is permitted during C3. |
| Market-data credentials | Later-phase deferred | No value or operational setting is permitted during C3. |
| Unrelated ambient OS variables such as `PATH` and `HOME` | Outside C3 settings namespace | Ignored by `settings_from_mapping()`; they are not C3 configuration inputs. |

No credential value may be committed, emitted in diagnostics, or written to test output. The host-neutral C3 configuration implementation rejects both the accepted provider/broker prefixes and the explicit known historical application/operational variable set; it does not reject arbitrary ambient OS variables.
