"""
PrivGuard — UploadThing integration tests
==========================================
Verifies the server-side evidence upload flow against mocked HTTP so the
module can be tested without a live UploadThing account or network access.
Run: python manage.py test tests.test_uploadthing -v2
"""
import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, override_settings
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from incidents import uploadthing


class FakeResponse:
    """Minimal context-manager response object standing in for urlopen()."""

    def __init__(self, payload=b"", code=200):
        self._payload = payload
        self.code = code
        self.reason = "OK"

    def read(self, *args, **kwargs):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return False


def get_header(req, name):
    return next(
        (v for k, v in req.headers.items() if k.lower() == name.lower()),
        None,
    )


PREPARE_RESPONSE = json.dumps({
    "data": [{
        "url": "https://s3.example.com/upload",
        "fields": {
            "key": "uploaded_key",
            "Policy": "abc",
            "bucket": "ut-files",
        },
        "key": "uploaded_key",
        "fileUrl": "https://utfs.io/f/uploaded_key",
        "ufsUrl": "https://utfs.io/f/uploaded_key",
    }]
}).encode()


@override_settings(UPLOADTHING_TOKEN="", UPLOADTHING_SECRET="")
class UploadThingDisabledTests(TestCase):
    def test_not_enabled_without_credentials(self):
        self.assertFalse(uploadthing.is_enabled())
        self.assertFalse(settings.UPLOADTHING_ENABLED)

    def test_upload_raises_when_disabled(self):
        f = SimpleUploadedFile("a.png", b"x", content_type="image/png")
        with self.assertRaises(uploadthing.UploadThingError):
            uploadthing.upload_evidence(f)


@override_settings(
    UPLOADTHING_TOKEN="sk_test_token",
    UPLOADTHING_SECRET="",
    UPLOADTHING_CDN_URL="https://utfs.io/f",
)
class UploadThingEnabledTests(TestCase):
    def test_is_enabled_with_token(self):
        self.assertTrue(uploadthing.is_enabled())

    @patch("incidents.uploadthing.urllib.request.urlopen")
    def test_upload_s3_post_flow(self, mock_urlopen):
        mock_urlopen.side_effect = [
            FakeResponse(PREPARE_RESPONSE),
            FakeResponse(b""),
        ]
        f = SimpleUploadedFile("screenshot.png", b"\x00" * 2048, content_type="image/png")

        key, url = uploadthing.upload_evidence(f)

        self.assertEqual(key, "uploaded_key")
        self.assertEqual(url, "https://utfs.io/f/uploaded_key")
        self.assertEqual(mock_urlopen.call_count, 2)

        prepare_req = mock_urlopen.call_args_list[0][0][0]
        self.assertIn("/v7/prepareUpload", prepare_req.full_url)
        body = json.loads(prepare_req.data.decode())
        self.assertEqual(body["files"][0]["name"], "screenshot.png")
        self.assertEqual(body["files"][0]["size"], 2048)
        self.assertEqual(body["files"][0]["type"], "image/png")
        self.assertEqual(body["files"][0]["acl"], "public-read")
        self.assertEqual(
            get_header(prepare_req, "x-uploadthing-api-key"), "sk_test_token"
        )

        upload_req = mock_urlopen.call_args_list[1][0][0]
        self.assertEqual(upload_req.full_url, "https://s3.example.com/upload")
        self.assertIn("multipart/form-data", get_header(upload_req, "Content-Type"))
        body_bytes = upload_req.data
        self.assertIn(b'name="file"', body_bytes)

    @patch("incidents.uploadthing.urllib.request.urlopen")
    def test_upload_put_fallback(self, mock_urlopen):
        resp = json.dumps({
            "data": [{
                "url": "https://ingest.uploadthing.com/PRESIGNED",
                "key": "put_key",
            }]
        }).encode()
        mock_urlopen.side_effect = [FakeResponse(resp), FakeResponse(b"")]

        f = SimpleUploadedFile("doc.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        key, url = uploadthing.upload_evidence(f)

        self.assertEqual(key, "put_key")
        self.assertEqual(url, "https://utfs.io/f/put_key")
        self.assertEqual(mock_urlopen.call_count, 2)
        put_req = mock_urlopen.call_args_list[1][0][0]
        self.assertEqual(put_req.get_method(), "PUT")
        self.assertEqual(put_req.full_url, "https://ingest.uploadthing.com/PRESIGNED")

    @patch("incidents.uploadthing.urllib.request.urlopen")
    def test_prepare_upload_http_error_raises(self, mock_urlopen):
        mock_urlopen.side_effect = __import__(
            "urllib.error", fromlist=["HTTPError"]
        ).HTTPError(
            "https://api.uploadthing.com/v7/prepareUpload",
            401,
            "Unauthorized",
            None,
            None,
        )
        f = SimpleUploadedFile("a.png", b"x", content_type="image/png")
        with self.assertRaises(uploadthing.UploadThingError):
            uploadthing.upload_evidence(f)

    @patch("incidents.uploadthing.urllib.request.urlopen")
    def test_delete_evidence_swallows_errors(self, mock_urlopen):
        mock_urlopen.side_effect = __import__(
            "urllib.error", fromlist=["HTTPError"]
        ).HTTPError("https://api.uploadthing.com/v6/deleteFiles", 500, "boom", None, None)
        uploadthing.delete_evidence("some_key")  # must not raise

    @patch("incidents.uploadthing.urllib.request.urlopen")
    def test_delete_evidence_calls_api(self, mock_urlopen):
        mock_urlopen.side_effect = [FakeResponse(json.dumps({
            "success": True, "deletedCount": 1,
        }).encode())]
        uploadthing.delete_evidence("some_key")
        req = mock_urlopen.call_args_list[0][0][0]
        self.assertIn("/v6/deleteFiles", req.full_url)
        body = json.loads(req.data.decode())
        self.assertEqual(body["fileKeys"], ["some_key"])

    def test_build_url_custom_cdn(self):
        with override_settings(UPLOADTHING_CDN_URL="https://cdn.example.com/f/"):
            self.assertEqual(
                uploadthing.build_url("key123"), "https://cdn.example.com/f/key123"
            )


class EvidenceUrlPropertyTests(TestCase):
    def test_local_file_uses_storage_url(self):
        from incidents.models import Incident
        inc = Incident()
        inc.evidence_file = "evidence/user_1/123_test.png"
        with override_settings(UPLOADTHING_ENABLED=False):
            self.assertFalse(inc.evidence_is_remote)

    def test_remote_key_detected(self):
        from incidents.models import Incident
        inc = Incident()
        inc.evidence_file = "some_remote_key.png"
        with override_settings(UPLOADTHING_ENABLED=True, UPLOADTHING_CDN_URL="https://utfs.io/f"):
            self.assertTrue(inc.evidence_is_remote)
            self.assertEqual(inc.evidence_url, "https://utfs.io/f/some_remote_key.png")

    def test_legacy_local_path_not_remote_when_enabled(self):
        from incidents.models import Incident
        inc = Incident()
        inc.evidence_file = "evidence/user_1/old.png"
        with override_settings(UPLOADTHING_ENABLED=True):
            self.assertFalse(inc.evidence_is_remote)


class FormUploadLimitTests(TestCase):
    def test_form_rejects_oversized_file(self):
        from incidents.forms import IncidentForm
        big = SimpleUploadedFile(
            "big.png", b"\x00" * (101 * 1024), content_type="image/png"
        )
        form = IncidentForm(data={
            "platform_category": "email",
            "date_of_occurrence": "2025-01-01",
            "incident_classification": "phishing",
            "narrative": "Test",
            "actor_involvement": "stranger",
            "severity_rating": 1,
        }, files={"evidence_file": big})
        self.assertFalse(form.is_valid())
        self.assertIn("evidence_file", form.errors)

    def test_form_accepts_small_file(self):
        from incidents.forms import IncidentForm
        small = SimpleUploadedFile(
            "small.png", b"\x00" * (10 * 1024), content_type="image/png"
        )
        form = IncidentForm(data={
            "platform_category": "email",
            "date_of_occurrence": "2025-01-01",
            "incident_classification": "phishing",
            "narrative": "Test",
            "actor_involvement": "stranger",
            "severity_rating": 1,
        }, files={"evidence_file": small})
        self.assertTrue(form.is_valid())
