# TikTok and Shopee live events

Connect your audience to your AI avatar: receive platform events in your application, normalize them, and forward them to your rented Aidol Room Cloud session. The running room handles AI replies and speech according to its reply settings.

## Choose your integration

| Platform | Event collection | Delivery to the avatar |
|---|---|---|
| TikTok LIVE | Your authorized collector, or an independently evaluated TikTok LIVE library | Aidol room events API with platform=tiktok |
| Shopee Live | Aidol Event Router's existing browser workflow, or your own authorized integration | Aidol room events API with platform=shopee |

**Aidol's developer API receives events. It does not currently provide an endpoint that starts a TikTok or Shopee collector just by passing a live URL.** The starter does not bundle either collector. Event availability varies by source: do not assume every platform exposes all supported Aidol event types.

## TikTok LIVE

One third-party option to evaluate is [TikTokLive for Python](https://github.com/isaackogan/TikTokLive). It is an unofficial project, not an official TikTok API. Review its current installation instructions, event classes, connection requirements, and applicable platform terms before integrating it. This starter does not guarantee its availability or compatibility.

After your collector receives a comment, map its source message ID, nickname, and text to this callback:

    def on_tiktok_comment(message_id, nickname, text):
        return client.send(
            'comment', nickname, text,
            platform='tiktok',
            event_id='tt:' + str(message_id),
        )

For an interaction your collector supports:

    def on_tiktok_follow(event_id, nickname):
        return client.send(
            'follow', nickname, platform='tiktok',
            event_id='tt:' + str(event_id), reply=True,
        )

These are mapping callbacks, not a complete TikTok collector. Register equivalent callbacks with your chosen collector and validate IDs against the Aidol event ID format. Gift collectors may emit multiple updates for one gift streak: normalize these deliberately so you do not double count or trigger repeated replies.

## Shopee Live

For the existing Aidol Event Router workflow:

1. Select Shopee and open its browser from Router.
2. Let the account owner sign in manually and open the relevant live page.
3. Start capture after the page is ready.
4. Connect Router to the rented room using its supported room connection workflow.

Router's Shopee collector observes live network messages; this starter does not reproduce its collector or expose private Shopee endpoints. Do not put account cookies, browser profiles, credentials, or private network captures in this repository.

For your own authorized Shopee integration, call the Aidol client when your collector receives a comment:

    def on_shopee_comment(message_id, nickname, text):
        return client.send(
            'comment', nickname, text,
            platform='shopee',
            event_id='sh:' + str(message_id),
        )

No general public Shopee Live comment API is claimed here. If using Shopee partner capabilities, confirm the actual account permissions and current documentation with Shopee.

## One event format for both platforms

    {
      "events": [{
        "id": "sh:comment-123",
        "type": "comment",
        "platform": "shopee",
        "user": {"id": "viewer-42", "name": "Alex"},
        "text": "Is this product available in blue?"
      }],
      "auto_reply_interactions": true
    }

POST this JSON to /rooms/{session_id}/events with your developer Bearer key. Use platform=tiktok for TikTok events. For gifts include gift_name and quantity when the source supplies them.

The room must already be live with comment replies enabled. For non-comment responses, enable the relevant room interaction settings and send auto_reply_interactions=true. Filters, cooldowns, queues, balance, and service readiness still apply; event receipt does not guarantee every event will produce speech. No separate AI or speech request is needed per comment.

## Reconnection and duplicates

- Reconnect collectors with bounded exponential backoff and show their actual connection status.
- Preserve the source event ID across reconnects and retries. IDs must be 1–128 characters using letters, digits, underscores, dots, colons, or hyphens.
- Keep the same payload and reply flag on retries. Do not invent a new ID just because the avatar has not spoken yet.
- Batch bursts within API limits: up to 100 events/request, 256 KiB/request, and 60 requests/minute/key.
- Keep pairing codes, API keys, account credentials, and viewing URLs private.

See [Audience interactions](AUDIENCE_INTERACTIONS.md) for the complete room-side flow and [the event bridge example](examples/event_bridge.py) for a runnable JSON forwarding test.
