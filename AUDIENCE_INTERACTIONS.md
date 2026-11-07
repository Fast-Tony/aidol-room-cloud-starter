# Make your AI avatar respond to audience events

Your application collects audience events and sends them to a rented room. Aidol Room Cloud handles response generation, voice synthesis, and avatar playback. You do not need a separate LLM or TTS call for each comment.

**Flow: your authorized event source → your event callback → Aidol Room Cloud events API → AI reply → avatar speech in the live output.**

## 1. Prepare the room

Rent a room, choose your avatar and voice, configure the brain/product information, and start live in the Room dashboard. Enable automatic comment replies. For joins, follows, shares, likes, and gifts, enable the corresponding interaction replies and cooldown settings.

Get the room's one-time ALC code and call client.connect(code). Keep the returned API key private. The room must be running, with an active rental, sufficient balance, and working AI/voice services.

## 2. Collect events in your software

Use the platform SDK, webhook, or collector you are authorized to access. Register a callback and map its fields to the room API. This starter does not include a TikTok, Facebook, or Shopee collector.

| Collector field | API field |
|---|---|
| Stable source event/message ID | id |
| Category | type |
| Lowercase platform identifier | platform |
| Viewer ID | user.id |
| Viewer display name | user.name |
| Comment content | text |
| Gift name and count | gift_name, quantity |

Supported types: comment, join, follow, share, like, gift. Event IDs use 1–128 letters, digits, underscores, dots, colons, or hyphens.

## 3. Forward a comment from your callback

    from client import AidolClient

    client = AidolClient()
    client.connect('ALC-CODE-FROM-ROOM')

    def on_comment(message):
        return client.send(
            'comment', message['viewer_name'], message['text'],
            platform='custom', event_id=str(message['message_id']),
        )

Register on_comment with your collector. Once the comment reaches the live room, its runtime handles the AI response according to room settings. No additional speech-generation request is needed.

For non-comment interactions, request replies explicitly:

    client.send('follow', 'Alex', platform='custom',
                event_id='follow-123', reply=True)

The reply flag sets auto_reply_interactions=true. The room's corresponding interaction settings must also be enabled. Comment events use the room's automatic comment reply setting.

## 4. HTTP integration for any language

Base URL: https://genaidol.com/cloud-api/developer/v1

Exchange the ALC code using POST /connect with a JSON body containing code. Save the returned api_key and session_id securely, then send:

    POST /cloud-api/developer/v1/rooms/{session_id}/events
    Authorization: Bearer YOUR_DEVELOPER_KEY
    Content-Type: application/json

    {
      "events": [{
        "id": "comment-123",
        "type": "comment",
        "platform": "custom",
        "user": {"id": "viewer-42", "name": "Alex"},
        "text": "Which colors are available?"
      }],
      "auto_reply_interactions": true
    }

For gifts, set type to gift and include gift_name and an integer quantity. Preserve the source's event ID; on retries, keep the same ID, content, and reply flag. Changing content under the same ID returns 409.

Limits: 1–100 events/request, 256 KiB/request, 60 requests/minute/key. Batch events instead of sending an unbounded request for every like.

## 5. Test the bridge

Run from the repository root:

    python examples/event_bridge.py

Enter a fresh ALC code when prompted. Paste one event object per line:

    {"id":"demo-001","type":"comment","platform":"custom","user":{"id":"42","name":"Alex"},"text":"Which colors are available?"}

An empty line exits. Replace standard input with your event callback when integrating your collector.

## If the avatar does not reply

HTTP 202 and status received acknowledge event receipt, not completed speech. Filters, reply settings, cooldowns, and the speech queue may delay or suppress a response. Check that live is running, the relevant replies are enabled, and balance and services are available.

ROOM_NOT_ACTIVE means the rental is inactive. ROOM_CONNECTION_EXPIRED requires pairing with a fresh ALC code. On 429, slow down and honor the retry interval. On ambiguous delivery, retain the original event ID. Never resend an accepted event with a new ID merely because speech has not played yet.

Do not publish API keys, pairing codes, or private viewing URLs. The developer key is scoped to one room.
