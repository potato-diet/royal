from course_scraper import CourseScraper;

course_scraper = CourseScraper(None)
for course in course_scraper.invoke():
    print(course.url())
