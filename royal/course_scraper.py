from dataclasses import dataclass
from sqlite3 import Cursor
from typing import List
import requests
import re

@dataclass
class Course:
    code: str
    id: str

    def url(self):
        return "https://coursefinder.utoronto.ca/course-search/search/courseInquiry?methodToCall=start&viewId=CourseDetails-InquiryView&courseId=" + self.id

class CourseScraper:
    def __init__(self, db: Cursor):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def invoke(self) -> List[Course]:
        # Have to make an initial request to set the authorization cookies.
        init_url = "https://coursefinder.utoronto.ca/course-search/search/courseSearch?viewId=CourseSearch-FormView&methodToCall=start"
        self.session.get(init_url)

        list_url = "https://coursefinder.utoronto.ca/course-search/search/courseSearch/course/search?queryText=&requirements=&campusParam=St.+George%2CScarborough%2CMississauga"
        data = self.session.get(list_url).json()["aaData"]
        for x in data:
            match = re.search("/(\w+)'>(\w+)<", x[1])
            if match:
                yield Course(match[2], match[1])
