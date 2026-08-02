"""Server-side UploadThing integration for incident evidence files.

Evidence uploads are sent from the Django server to UploadThing so that files
survive on serverless platforms (Vercel) where the local filesystem is
ephemeral. The only value persisted on the Incident is the UploadThing file
key; the public URL is derived at render time.

Flow (server-side upload, no callbacks):
1. POST /v7/prepareUpload  -> presigned S3 POST fields + file key
2. POST the presigned URL  -> multipart form-data (S3-style fields + file)
3. Store the returned file key on the incident.
"""

import json
import uuid

import urllib.request
import urllib.error

from django.conf import settings


class UploadThingError(Exception):
    """Raised when an UploadThing request fails."""


API_BASE_URL = "https://api.uploadthing.com"


def _api_key():
    return (settings.UPLOADTHING_TOKEN or settings.UPLOADTHING_SECRET or "").strip()


def is_enabled():
    return bool(_api_key())


def _post_json(path, payload):
    req = urllib.request.Request(
        API_BASE_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-uploadthing-api-key": _api_key(),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise UploadThingError(
            f"UploadThing {path} failed: HTTP {exc.code} {exc.read().decode('utf-8', 'replace')}"
        ) from exc
    except urllib.error.URLError as exc:
        raise UploadThingError(f"UploadThing {path} unreachable: {exc.reason}") from exc


def prepare_upload(filename, size, content_type):
    """Request a presigned S3-style POST target for a single file."""
    payload = {
        "files": [
            {
                "name": filename,
                "size": size,
                "type": content_type,
                "customId": None,
                "contentDisposition": "inline",
                "acl": "public-read",
            }
        ]
    }
    response = _post_json("/v7/prepareUpload", payload)
    items = response.get("data") if isinstance(response, dict) else response
    if not items:
        raise UploadThingError("UploadThing prepareUpload returned no presigned data.")
    return items[0]


def _multipart_post(url, fields, filename, content_type, file_bytes):
    boundary = "----PRG" + uuid.uuid4().hex
    parts = []
    for key, value in (fields or {}).items():
        if value is None:
            continue
        parts.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{key}"\r\n'
                f"\r\n"
                f"{value}\r\n"
            ).encode("utf-8")
        )
    parts.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n"
            f"\r\n"
        ).encode("utf-8")
        + file_bytes
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    req = urllib.request.Request(
        url,
        data=b"".join(parts),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
    except urllib.error.HTTPError as exc:
        raise UploadThingError(
            f"UploadThing upload failed: HTTP {exc.code} {exc.read().decode('utf-8', 'replace')}"
        ) from exc
    except urllib.error.URLError as exc:
        raise UploadThingError(f"UploadThing upload unreachable: {exc.reason}") from exc


def upload_evidence(file):
    """Upload a Django file-like object to UploadThing.

    Returns a (file_key, public_url) tuple.
    """
    if not is_enabled():
        raise UploadThingError("UploadThing is not configured.")

    file.seek(0)
    file_bytes = file.read()
    filename = getattr(file, "name", "evidence") or "evidence"
    content_type = getattr(file, "content_type", None) or "application/octet-stream"

    prepared = prepare_upload(filename, len(file_bytes), content_type)
    if prepared.get("fields"):
        _multipart_post(
            prepared["url"], prepared["fields"], filename, content_type, file_bytes
        )
    else:
        # Fallback for responses that return a direct PUT presigned URL.
        _put_bytes(prepared["url"], file_bytes, content_type)

    return prepared["key"], build_url(prepared["key"])


def _put_bytes(url, file_bytes, content_type):
    req = urllib.request.Request(
        url,
        data=file_bytes,
        headers={"Content-Type": content_type},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
    except urllib.error.HTTPError as exc:
        raise UploadThingError(
            f"UploadThing upload failed: HTTP {exc.code} {exc.read().decode('utf-8', 'replace')}"
        ) from exc
    except urllib.error.URLError as exc:
        raise UploadThingError(f"UploadThing upload unreachable: {exc.reason}") from exc


def build_url(file_key):
    """Public CDN URL for an UploadThing file key."""
    base = (settings.UPLOADTHING_CDN_URL or "https://utfs.io/f").rstrip("/")
    return f"{base}/{file_key}"


def delete_evidence(file_key):
    """Best-effort delete of a remote file. Failures are swallowed."""
    if not file_key or not is_enabled():
        return
    try:
        _post_json("/v6/deleteFiles", {"fileKeys": [file_key]})
    except UploadThingError:
        pass
