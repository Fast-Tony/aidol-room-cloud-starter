# Official TikTok and Shopee integrations

Use platform-approved APIs and event subscriptions to connect your application to Aidol Room Cloud. This guide covers official integration paths only.

## Official developer portals

| Platform | Official starting point |
|---|---|
| TikTok | [TikTok for Developers](https://developers.tiktok.com/) |
| TikTok Shop | [TikTok Shop Partner Center](https://partner.tiktokshop.com/) |
| Shopee | [Shopee Open Platform](https://open.shopee.com/) |

**Access to a developer portal, seller API, or webhook does not by itself grant access to live comments, likes, follows, or gifts.** Availability depends on the approved product, region, application permissions, and account authorization. This starter has not verified a generally available official real-time LIVE comments API for either platform. Do not treat order notifications, video comments, or other webhook categories as LIVE audience events.

## 1. Register and request the correct permissions

1. Register your application in the appropriate official developer or partner portal.
2. Describe your AI livestream interaction use case during application review.
3. Ask the platform which approved product, endpoint, or subscription grants the specific live events you need in your region.
4. Obtain account-owner authorization using the platform's documented flow.
5. Enable only the event categories actually granted to your application.

If LIVE audience events are not available to your application, contact the platform's developer/partner support. Do not assume entering a live URL or obtaining an access token enables them. This repository does not supply an alternative collection method.

## 2. Implement the documented platform delivery mechanism

Follow the exact documentation granted to your application, including its current authorization, token refresh, signature verification, challenge handling, delivery acknowledgements, retries, and rate limits. Use a webhook only if the approved API specifies webhooks; otherwise use its documented mechanism.

No platform event names, signature algorithms, or LIVE endpoints are invented in this guide. TikTok's public webhook documentation is available at [Webhooks events](https://developers.tiktok.com/doc/webhooks-events); confirm that your requested event is explicitly supported for your approved product. For Shopee and TikTok Shop, consult the documentation and permissions shown in your official partner account.

## 3. Forward verified events to your rented Aidol room

After validating an event received through the official platform mechanism, map its documented fields to the Aidol event schema. The callback below receives already verified, normalized values; it is not a TikTok or Shopee SDK implementation.

    def forward_verified_comment(client, platform, message_id, viewer_name, text):
        if platform not in ('tiktok', 'shopee'):
            raise ValueError('Unsupported platform')
        return client.send(
            'comment', viewer_name, text,
            platform=platform,
            event_id=str(message_id),
        )

Preserve the original event identity across retries. Aidol IDs allow 1–128 letters, digits, underscores, dots, colons, or hyphens; deterministically map longer or incompatible platform IDs before forwarding. Only map a platform event to a follow, gift, or other Aidol type when its documented meaning matches.

Aidol accepts comment, join, follow, share, like, and gift events. This does not imply either platform grants all those events.

## 4. Let the room handle the AI response

Start the rented room and enable automatic comment replies. Once a valid comment is forwarded, Aidol handles the AI response and voice playback according to the room settings. No separate AI or speech-generation call is required. For supported non-comment interactions, request replies with reply=True and enable the relevant room settings.

Filters, cooldowns, queues, balance, and service readiness still apply. HTTP 202 confirms event receipt, not that a spoken reply has completed. See [Audience interactions](AUDIENCE_INTERACTIONS.md) for the Aidol payload, batching limits, retry behavior, and troubleshooting.

Keep platform access tokens, app secrets, Aidol keys, and private viewing URLs on trusted systems and out of this public repository.
