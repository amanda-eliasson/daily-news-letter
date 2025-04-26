import os

# url and headers
OMNI_URL = "https://omni.se/"
SCRAPER_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# HTML class names
OMNI_CLUSTER_CONTAINER_CLASS = "TeaserCluster_clusterContainer__o70EC"
OMNI_HEADER_CLASS = "StoryVignette_titleLink__SSEOi"
OMNI_TITLE_CLASS = "TeaserHeading_teaserTitle__ShOGe"
OMNI_TEASER_CLASS = "TeaserText_teaserText__23krM"
OMNI_TIMESTAMP_CLASS = "Timestamp_timestamp__9fbnE"

# Default messages
NO_HEADER_MSG = "No Header"
NO_TITLE_MSG = "No title"
NO_TEXT_MSG = "No text"
UNDEFINED_TIME_MSG = "Undefined time"

# paths
TMP_DIR=os.getenv("TMP_DIR", "/tmp/files")
GPT_MODEL_NAME=os.getenv("GPT_MODEL_NAME", "gpt-4o-mini")