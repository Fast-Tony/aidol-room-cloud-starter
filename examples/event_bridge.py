"""Forward normalized JSON audience events to a running Aidol room."""
import getpass
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from client import AidolClient

def main():
    client = AidolClient()
    try:
        client.connect(getpass.getpass('One-time ALC room code: ').strip())
    except RuntimeError as exc:
        print('Connection failed:', exc, file=sys.stderr)
        return 1
    print('Connected. Paste one JSON event per line; empty line exits.')
    while True:
        try:
            line = input('event> ').strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        try:
            event = json.loads(line)
            result = client.request(
                'POST', '/rooms/' + client.session + '/events',
                {'events': [event], 'auto_reply_interactions': True},
                retry=True,
            )
            print('Received:', result.get('received', 0),
                  '| Duplicates:', result.get('duplicates', 0))
        except (ValueError, RuntimeError) as exc:
            print('Could not forward event:', exc, file=sys.stderr)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
