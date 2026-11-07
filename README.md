# Aidol Room Cloud — AI Livestream Starter

**Build your own AI livestreaming software with the Aidol Room Cloud API.**

An open-source Python starter for developers building custom AI livestreaming applications. Create your own interface and workflows, connect to a rented Aidol Room Cloud session, send audience interactions, and retrieve a private Browser Source URL for OBS.

Use, modify, distribute, and build commercial applications with this sample under the [MIT License](LICENSE).

## What can you build?

- AI livestreaming applications with your own branding and user experience.
- Audience interaction tools connected to sources you are authorized to access.
- Desktop dashboards for room pairing, interaction delivery, and OBS integration.
- Integrations between AI live sessions and existing sales or content workflows.

## Current capabilities

| Feature | Availability |
|---|---|
| Pair with a rented room using a one-time ALC code | Supported |
| Send comments, joins, follows, shares, likes, and gifts | Supported |
| Automatically retrieve the room's Browser Source URL | Supported |
| Copy the URL for OBS or open it in a browser | Supported |
| Python API client and desktop demo | Included |
| Create/rent rooms, configure avatars/scripts, or start/stop live through this client | Not implemented; use the Room web dashboard |
| Built-in TikTok, Facebook, or Shopee event collection | Not included |

This is a starter application, not a complete room-management SDK. Prepare and start your live session in the web dashboard before using this sample to send interactions.

## Quick start

### Requirements

- Python 3.10 or later.
- Tkinter for the desktop application. Tkinter availability depends on your Python installation; on some systems it is installed separately.
- An Aidol Room Cloud account with an active rented room.

The client uses Python's standard library and requires no pip packages.

```sh
git clone https://github.com/Fast-Tony/aidol-room-cloud-starter.git
cd aidol-room-cloud-starter
python demo_gui.py
```

Use `python3` instead of `python` if that is how Python is installed on your system.

### Connect your room

1. Sign in to [Aidol Room Cloud](https://room.genaidol.com) and rent a room.
2. Select your avatar and script, then start the live session in the Room dashboard.
3. Get a one-time ALC code from the room's Router connection section.
4. Enter the code in the sample application and click **Connect room**.
5. The app retrieves the Browser Source URL automatically. Click **Copy OBS URL**.
6. In OBS, select **Sources → + → Browser** and paste the URL.
7. Enable comment replies in the room settings, then send a test interaction from the app.

If a viewing URL is not available yet, the app checks again every 15 seconds.

## Integrate with your application

```python
from client import AidolClient

client = AidolClient()
room = client.connect('ALC-CODE-FROM-ROOM')

# room['browser_source_url'] contains a private viewing URL when available.
# Do not print it to public logs.

receipt = client.send(
    'comment',
    'Alex',
    'Which colors are available?',
    platform='custom',
    event_id='source-message-123',
)
```

### Included files

- `client.py`: reusable Python API client and command-line entry point.
- `demo_gui.py`: English-language desktop demo with room pairing, interaction testing, and OBS URL retrieval.
- `LICENSE`: MIT License for this sample source code.

### Delivery behavior

- Supported event types: `comment`, `join`, `follow`, `share`, `like`, and `gift`.
- Each API key is scoped to one room. It cannot start or stop a live session.
- Reuse the same event ID and content when retrying an event to prevent duplicates.
- HTTP 202 acknowledges receipt; it does not confirm that the AI response has been spoken.
- Replies depend on room configuration, an active rental, and available voice/AI services.
- The sample does not collect platform events itself. Connect your authorized event source to the client.

## API and resources

- [Aidol Room Cloud](https://room.genaidol.com)
- API base URL: `https://genaidol.com/cloud-api/developer/v1`
- [API reference](https://genaidol.com/cloud-api/developer/v1/docs)

## Credentials and licensing

Keep API keys, pairing codes, and private viewing URLs out of source control and public logs. The demo keeps its API key in memory rather than saving it to disk.

The MIT License covers this sample source code. Access to Aidol Room Cloud remains subject to platform permissions, account requirements, and service charges.
