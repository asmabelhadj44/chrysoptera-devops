# Cloud Cost Comparison for IoT Ingestion — Chrysoptera

**Scenario:** 100 solar sites, each sending 1 sensor reading every 5 minutes.
- 288 messages/site/day → **28,800 messages/day** → **~864,000 messages/month**
- Assumed payload size: ~1 KB per reading (voltage, current, temperature, timestamp)

## Azure IoT Hub

| Tier | Price/month | Daily message cap | Fits our load? |
|------|------------|--------------------|-----------------|
| Free | $0 | 8,000/day | No — under our 28,800/day |
| S1 | $25 | 400,000/day | Yes — ~7% utilized |
| S2 | $250 | 6,000,000/day | Overkill at this scale |

**Cost at our scale: ~$25/month.** The Free tier is disqualified twice over: it's short on daily message quota, and it also lacks cloud-to-device messaging and device management, which we'd likely want later to push firmware updates or config changes to sites. S1 gives ~14x headroom before needing to upgrade.

## AWS IoT Core

Billed per component rather than per tier:
- **Messaging:** $1.00 per million messages → 864,000 messages ≈ **$0.86/month**
- **Connectivity:** $0.042 per device/year for 24/7 connection → 100 devices ≈ **$4.20/year (~$0.35/month)**
- **Registry/Shadow + Rules:** negligible at this volume (a few cents)

**Cost at our scale: ~$1.20/month.** AWS's pay-per-component model is dramatically cheaper at small scale because there's no fixed monthly unit fee — you only pay for what you actually send.

## GCP Pub/Sub

Google **retired its managed IoT Core service in August 2023** — there is no direct "IoT platform" equivalent to AWS IoT Core or Azure IoT Hub anymore. Pub/Sub can still ingest the messages, but device registration, per-device auth, and device management would need to be built ourselves (e.g., with Cloud IoT-adjacent open-source tools or a custom auth layer).

- **Pricing:** $40 per TiB of throughput, first **10 GiB/month free**
- Our load: 864,000 messages × ~1 KB ≈ **0.82 GiB/month** — comfortably inside the free tier

**Cost at our scale: effectively $0/month for messaging** — but this excludes the engineering cost of building device management ourselves, which the other two platforms provide out of the box.

## Summary Table

| Provider | Monthly cost @ 100 sites | Device management included? | Notes |
|----------|--------------------------|------------------------------|-------|
| Azure IoT Hub | ~$25 | Yes | Simple flat pricing, most headroom for a startup budget |
| AWS IoT Core | ~$1.20 | Yes | Cheapest at small scale, more granular billing to track |
| GCP Pub/Sub | ~$0 (messaging only) | No — build it yourself | Cheapest raw messaging, but hidden dev cost |

## Recommendation

For Chrysoptera at MVP scale (dozens to low hundreds of solar sites), **AWS IoT Core** offers the best balance: near-zero cost, full device management included, and pricing that scales linearly with actual usage rather than jumping in large tier steps like Azure. Azure IoT Hub is a strong second choice if the team prefers flat, predictable billing over granular pay-per-use. GCP is not recommended unless the team is prepared to build and maintain its own device management layer.
