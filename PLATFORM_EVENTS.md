# Open-source audience event integrations

Use an independent event collector and forward its events to your rented Aidol Room. You do not need to reproduce Aidol Event Router.

## TikTok LIVE

- Python: [TikTokLive](https://github.com/isaackogan/TikTokLive).
- Node.js: [TikTok-Live-Connector](https://github.com/zerodytrash/TikTok-Live-Connector).

These are unofficial third-party libraries, both licensed AGPL-3.0. Read their current documentation and license before integrating or distributing your application. Aidol does not maintain these projects.

## Shopee Live

Browse [public Shopee Live projects on GitHub](https://github.com/search?q=shopee+live+comments&type=repositories). Aidol has not yet verified a maintained, licensed incoming-event collector to recommend. Check that a project receives audience comments rather than only sending chat messages, and review its license.

## Forward events to Aidol Room

Connect the starter client to a running room. In your collector callback, call:

    client.send("comment", viewer_name, comment_text,
                platform="tiktok", event_id=str(message_id))

Use platform="shopee" for Shopee and stable event IDs to avoid duplicates. Enable comment replies in the Room settings. See [Audience interactions](AUDIENCE_INTERACTIONS.md) for other event types. Acceptance does not guarantee speech: room settings, cooldowns, filters and balance apply.

Collect only from accounts you are authorized to access, follow platform rules and keep credentials private. Dependencies keep their own licenses; the MIT license of this starter does not replace them.
