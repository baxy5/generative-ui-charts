import os
import uuid
from pydantic import BaseModel, Field
import boto3
from datetime import datetime
from botocore.config import Config


class Files(BaseModel):
    page_title: str = Field(default=None, description="Title of the page.")
    html: str = Field(default=None, description="HTML code.")
    css: str = Field(default=None, description="CSS code.")
    js: str = Field(default=None, description="Javascript code.")


class R2ObjectStorage:
    """A utility class for storing data to Cloudflare R2 object storage.

    This class provides common functions and utilities for uploading files and data
    to Cloudflare R2 object storage. It handles authentication, file uploads,
    and URL generation for hosted content.
    """

    def __init__(self, public_url: str) -> None:
        self.public_url = public_url

    def create_separate_files(self, files):
        """Build separate codes."""

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{files["page_title"]}</title>
            <link rel="stylesheet" href="./styles.css">
        </head>
        <body>
            <div class="component-container">
                {files["html"]}
            </div>
            
            <script src="./app.js"></script>
            <script>
                // Initialize component when DOM is loaded
                document.addEventListener('DOMContentLoaded', function() {{
                    if (window.initializeComponent) {{
                        window.initializeComponent('1');
                    }}
                }});
            </script>
        </body>
        </html>
        """

        css_content = files["css"]

        js_content = files["js"]

        return {"html": html_content, "css": css_content, "javascript": js_content}

    async def upload_to_storage(self, files) -> str:
        """Upload files to Cloudflare R2 Object Storage and return the hosted URL."""

        # Cloudflare R2 Config
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        access_key_id = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
        secret_access_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        bucket_name = os.getenv("CLOUDFLARE_R2_BUCKET_NAME")

        if not all([account_id, access_key_id, secret_access_key]):
            raise ValueError("Missing required Cloudflare R2 environment variables")

        # Configure boto3 client for Cloudflare R2
        r2_client = boto3.client(
            "s3",
            endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version="s3v4"),
            region_name="auto",
        )

        # Create unique folder id for this app
        current_time = datetime.now().strftime("%Y%m%d%H%M")
        folder_key = f"artifact-{current_time}-{str(uuid.uuid4()).replace('-', '')[:4]}"

        # Seperate files
        separated_files = self.create_separate_files(files)

        files_to_upload = [
            ("index.html", separated_files["html"], "text/html"),
            ("styles.css", separated_files["css"], "text/css"),
            ("app.js", separated_files["javascript"], "application/javascript"),
        ]

        try:
            for filename, content, content_type in files_to_upload:
                file_key = f"{folder_key}/{filename}"

                r2_client.put_object(
                    Bucket=bucket_name,
                    Key=file_key,
                    Body=content,
                    ContentType=content_type,
                )

            return f"{self.public_url}/{folder_key}/index.html"

        except Exception as e:
            raise Exception(f"Failed to upload files to Cloudflare R2: {str(e)}")
