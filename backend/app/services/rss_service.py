import logging
import os
import xml.etree.ElementTree as ET
from utils.config import DATA_FOLDER


class RssService:
    def __init__(self):
        self.recent_activities = self.load_rss_feed()

    def load_rss_feed(self):
        recent_activities = []
        try:
            tree = ET.parse(os.path.join(DATA_FOLDER, "rss_feed.xml"))
            root = tree.getroot()

            for item in root.findall("./channel/item"):
                activity = {
                    "title": item.find("title").text,
                    "description": item.find("description").text,
                    "link": item.find("link").text,
                    "pubDate": item.find("pubDate").text,
                }
                recent_activities.append(activity)

            logging.info("Recent activities loaded successfully from RSS feed.")
        except Exception as e:
            logging.error(f"Failed to load recent activities: {e}")
        return recent_activities
