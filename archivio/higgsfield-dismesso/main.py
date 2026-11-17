"""Seedance 2.5 text-to-video via the official Higgsfield SDK.

The key is read from .env.local (HF_KEY=key-id:key-secret) and never printed.
Run with: uv run main.py
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env.local"))

import higgsfield_client  # noqa: E402  (imported after the key is in the environment)
from higgsfield_client.exceptions import CredentialsMissedError, HiggsfieldClientError  # noqa: E402

MODEL = "bytedance/seedance-2.5/text-to-video"
ARGUMENTS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}


def main() -> int:
    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGUMENTS,
            on_enqueue=lambda request_id: print(f"Richiesta in coda: {request_id}"),
            on_queue_update=lambda status: print(f"Stato: {type(status).__name__}"),
        )
    except CredentialsMissedError:
        print("HF_KEY mancante: aggiungilo in higgsfield/.env.local (key-id:key-secret).", file=sys.stderr)
        return 1
    except HiggsfieldClientError as error:
        print(f"Errore dall'API Higgsfield: {error}", file=sys.stderr)
        return 1

    # subscribe() returns the final payload whatever the outcome, so check it explicitly
    status = result.get("status")
    if status == "nsfw":
        print("Richiesta bloccata dalla moderazione (nsfw): nessun video.", file=sys.stderr)
        return 1
    if status in ("failed", "canceled"):
        print(f"Generazione non riuscita (stato: {status}): nessun video.", file=sys.stderr)
        return 1

    video_url = (result.get("video") or {}).get("url")
    if status != "completed" or not video_url:
        print(f"Risposta inattesa (stato: {status}), nessun URL video. Chiavi: {sorted(result)}", file=sys.stderr)
        return 1

    print(f"Video pronto: {video_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
