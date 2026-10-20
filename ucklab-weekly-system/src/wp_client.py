"""
wp_client.py - Unified WordPress Authenticated REST & Admin Client for UCKLab
Handles seamless session cookie + REST nonce authentication and fallback to Basic Auth.
Provides reliable media upload, post publishing with featured_media, and cache purging.
"""

import os
import sys
import re
import json
import base64
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

WP_URL = os.getenv("WP_URL", "https://ucdigin.net").rstrip("/")
WP_USER = os.getenv("WP_USER", os.getenv("WP_ADMIN_USER", "AutoBot_Editor"))
WP_PASS = os.getenv("WP_APP_PASSWORD", os.getenv("WP_ADMIN_PASS", "1y1X o32Y FSRb RaJ9 bGTj bPyL"))
WP_APP_PWD = os.getenv("WP_APP_PASSWORD", WP_PASS)

class WordPressClient:
    def __init__(self, wp_url=None, user=None, password=None):
        self.wp_url = (wp_url or WP_URL).rstrip("/")
        self.user = user or WP_USER
        self.password = password or WP_PASS
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "UCKLab-Executive-AutoBot/2026.1 (Windows NT 10.0; Win64; x64)"
        })
        self.basic_auth_header = "Basic " + base64.b64encode(f"{self.user}:{self.password}".encode()).decode()
        self.rest_nonce = None
        self.logged_in = False
        # Do not use cookie login when using WordPress Application Passwords
        if " " not in self.password:
            self._authenticate()

    def _authenticate(self):
        """Authenticates via wp-login.php and extracts REST nonce from wp-admin."""
        login_url = f"{self.wp_url}/wp-login.php"
        try:
            res = self.session.post(login_url, data={
                "log": self.user,
                "pwd": self.password,
                "rememberme": "forever",
                "wp-submit": "Log In"
            }, timeout=20)
            
            # Check login cookies
            has_login_cookie = any("wordpress_logged_in" in c.name for c in self.session.cookies)
            if has_login_cookie or res.status_code == 200:
                self.logged_in = True
                self._fetch_rest_nonce()
        except Exception as e:
            print(f"⚠️ [WP Client] Session login exception: {e}")

    def _fetch_rest_nonce(self):
        """Extracts X-WP-Nonce from wp-admin HTML."""
        try:
            admin_res = self.session.get(f"{self.wp_url}/wp-admin/", timeout=20)
            if admin_res.status_code == 200:
                match = re.search(r'"nonce":"([a-zA-Z0-9]+)"', admin_res.text) or \
                        re.search(r'wpApiSettings\s*=\s*{[^}]*"nonce":"([a-zA-Z0-9]+)"', admin_res.text)
                if match:
                    self.rest_nonce = match.group(1)
        except Exception as e:
            print(f"⚠️ [WP Client] Nonce fetch exception: {e}")

    def get_auth_headers(self, content_type="application/json"):
        """Returns valid headers for WordPress REST API requests."""
        headers = {
            "Authorization": self.basic_auth_header
        }
        if content_type:
            headers["Content-Type"] = content_type

        if self.rest_nonce:
            headers["X-WP-Nonce"] = self.rest_nonce

        return headers

    def upload_media(self, file_path, filename=None, alt_text="", title="", mime_type="image/jpeg"):
        """
        Uploads a binary media file to WordPress Media Library.
        Returns: (media_id, source_url)
        """
        if not os.path.exists(file_path):
            print(f"❌ [WP Client] Media file not found: {file_path}")
            return None, None

        if not filename:
            filename = os.path.basename(file_path)

        if not self.rest_nonce:
            self._authenticate()

        headers = self.get_auth_headers(content_type=mime_type)
        headers["Content-Disposition"] = f'attachment; filename="{filename}"'

        endpoint = f"{self.wp_url}/wp-json/wp/v2/media"
        with open(file_path, "rb") as f:
            file_data = f.read()

        try:
            res = self.session.post(endpoint, data=file_data, headers=headers, timeout=35)
            if res.status_code == 201:
                data = res.json()
                media_id = data.get("id")
                source_url = data.get("source_url")
                print(f"  ✓ [WP Client] 미디어 업로드 성공 (ID: {media_id}) -> {filename}")

                # Optional: Update alt_text and title
                if alt_text or title:
                    patch_headers = self.get_auth_headers("application/json")
                    self.session.post(
                        f"{endpoint}/{media_id}",
                        json={"alt_text": alt_text, "title": title},
                        headers=patch_headers,
                        timeout=15
                    )
                return media_id, source_url
            else:
                print(f"  ⚠️ [WP Client] Media upload failed ({res.status_code}): {res.text[:150]}")
        except Exception as e:
            print(f"  ⚠️ [WP Client] Media upload exception: {e}")

        return None, None

    def create_post(self, payload):
        """
        Creates or publishes a post via WordPress REST API.
        Returns: (success_bool, post_id, post_link)
        """
        if not self.rest_nonce:
            self._authenticate()

        headers = self.get_auth_headers("application/json")
        endpoint = f"{self.wp_url}/wp-json/wp/v2/posts"

        try:
            res = self.session.post(endpoint, json=payload, headers=headers, timeout=40)
            if res.status_code in (200, 201):
                data = res.json()
                post_id = data.get("id")
                post_link = data.get("link")
                return True, post_id, post_link
            else:
                print(f"  ❌ [WP Client] Post create error ({res.status_code}): {res.text[:200]}")
                return False, None, res.text
        except Exception as e:
            print(f"  ❌ [WP Client] Post create exception: {e}")
            return False, None, str(e)

    def purge_litespeed_cache(self):
        """Purges LiteSpeed Cache completely."""
        try:
            admin_url = f"{self.wp_url}/wp-admin/admin.php?page=litespeed"
            r = self.session.get(admin_url, timeout=15)
            purge_match = re.search(r'href="([^"]*litespeed_type=purge_all[^"]*)"', r.text)
            if purge_match:
                purge_url = purge_match.group(1).replace("&amp;", "&")
                if not purge_url.startswith("http"):
                    purge_url = f"{self.wp_url}/wp-admin/{purge_url.lstrip('/')}"
                self.session.get(purge_url, timeout=15)
                print("  ✓ [WP Client] LiteSpeed Cache 전체 퍼지 성공!")
                return True
        except Exception as e:
            print(f"  ⚠️ [WP Client] LiteSpeed Cache 퍼지 예외: {e}")
        return False

# Global singleton client instance
_wp_client_instance = None

def get_wp_client():
    global _wp_client_instance
    if _wp_client_instance is None:
        _wp_client_instance = WordPressClient()
    return _wp_client_instance
