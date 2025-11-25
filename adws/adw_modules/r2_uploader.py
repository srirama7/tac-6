"""R2 Uploader stub module for screenshot uploads.

This module provides a placeholder implementation for R2 uploads.
In production, this would upload screenshots to Cloudflare R2 bucket.
"""

import os
import logging
from typing import List, Dict, Optional


class R2Uploader:
    """Stub R2 uploader that returns local file paths as URLs.

    In production, this would upload files to Cloudflare R2 and return
    public URLs. For now, it just returns the local file paths.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the R2 uploader.

        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

        # Check for R2 configuration (optional)
        self.r2_endpoint = os.getenv("R2_ENDPOINT")
        self.r2_access_key = os.getenv("R2_ACCESS_KEY_ID")
        self.r2_secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
        self.r2_bucket = os.getenv("R2_BUCKET_NAME")
        self.r2_public_url = os.getenv("R2_PUBLIC_URL")

        self.configured = all([
            self.r2_endpoint,
            self.r2_access_key,
            self.r2_secret_key,
            self.r2_bucket
        ])

        if not self.configured:
            self.logger.info("R2 not configured - screenshots will use local paths")

    def upload_screenshots(
        self,
        screenshot_paths: List[str],
        adw_id: str
    ) -> Dict[str, str]:
        """Upload screenshots and return URL mapping.

        Args:
            screenshot_paths: List of local file paths to upload
            adw_id: ADW workflow ID for organizing uploads

        Returns:
            Dict mapping local paths to public URLs (or local paths if not configured)
        """
        url_mapping: Dict[str, str] = {}

        for path in screenshot_paths:
            if not path:
                continue

            if not os.path.exists(path):
                self.logger.warning(f"Screenshot not found: {path}")
                continue

            if self.configured:
                # Would upload to R2 here
                # For now, just use local path
                url = f"file://{os.path.abspath(path)}"
            else:
                # Use local file path as URL
                url = f"file://{os.path.abspath(path)}"

            url_mapping[path] = url
            self.logger.debug(f"Mapped screenshot: {path} -> {url}")

        return url_mapping

    def upload_file(self, local_path: str, remote_key: str) -> Optional[str]:
        """Upload a single file to R2.

        Args:
            local_path: Path to local file
            remote_key: Key (path) for the file in R2

        Returns:
            Public URL if successful, None otherwise
        """
        if not os.path.exists(local_path):
            self.logger.error(f"File not found: {local_path}")
            return None

        if self.configured:
            # Would upload to R2 here
            # For now, return local path
            return f"file://{os.path.abspath(local_path)}"
        else:
            return f"file://{os.path.abspath(local_path)}"
