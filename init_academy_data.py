from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Category, Course, Step, CourseProgress
import uuid

# Create tables
Base.metadata.create_all(bind=engine)

def init_academy_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Category).first():
            print("Academy data already exists")
            return
        
        # Create categories
        categories_data = [
            {"id": "9a67dff7-3c38-4052-a335-0cef93438ff6", "title": "Web", "slug": "web"},
            {"id": "a89672f5-e00d-4be4-9194-cb9d29f82165", "title": "Firebase", "slug": "firebase"},
            {"id": "02f42092-bb23-4552-9ddb-cfdcc235d48f", "title": "Cloud", "slug": "cloud"},
            {"id": "5648a630-979f-4403-8c41-fc9790dea8cd", "title": "Android", "slug": "android"},
        ]
        
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.add(category)
        
        db.commit()
        
        # Create courses
        courses_data = [
            {
                "id": "694e4e5f-f25f-470b-bd0e-26b1d4f64028",
                "title": "Basics of Angular",
                "slug": "basics-of-angular",
                "description": "Introductory course for Angular and framework basics",
                "category": "web",
                "duration": 30,
                "total_steps": 11,
                "featured": True,
            },
            {
                "id": "f924007a-2ee9-470b-a316-8d21ed78277f",
                "title": "Basics of TypeScript",
                "slug": "basics-of-typeScript",
                "description": "Beginner course for Typescript and its basics",
                "category": "web",
                "duration": 60,
                "total_steps": 11,
                "featured": True,
            },
            {
                "id": "0c06e980-abb5-4ba7-ab65-99a228cab36b",
                "title": "Android N: Quick Settings",
                "slug": "android-n-quick-settings",
                "description": "Step by step guide for Android N: Quick Settings",
                "category": "android",
                "duration": 120,
                "total_steps": 11,
                "featured": False,
            },
            {
                "id": "1b9a9acc-9a36-403e-a1e7-b11780179e38",
                "title": "Build an App for the Google Assistant with Firebase",
                "slug": "build-an-app-for-the-google-assistant-with-firebase",
                "description": "Dive deep into Google Assistant apps using Firebase",
                "category": "firebase",
                "duration": 30,
                "total_steps": 11,
                "featured": False,
            },
            {
                "id": "55eb415f-3f4e-4853-a22b-f0ae91331169",
                "title": "Keep Sensitive Data Safe and Private",
                "slug": "keep-sensitive-data-safe-and-private",
                "description": "Learn how to keep your important data safe and private",
                "category": "android",
                "duration": 45,
                "total_steps": 11,
                "featured": False,
            },
        ]
        
        courses = []
        for course_data in courses_data:
            course = Course(**course_data)
            db.add(course)
            courses.append(course)
        
        db.commit()
        
        # Create demo course steps
        demo_content = """
        <h2 class="text-2xl sm:text-3xl">{title}</h2>
        <p class="lead">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus aperiam lab et fugiat id magnam minus nemo quam
            voluptatem. Culpa deleniti explica nisi quod soluta.
        </p>
        <p>
            Alias animi labque, deserunt distinctio eum excepturi fuga iure labore magni molestias mollitia natus, officia pofro
            quis sunt temporibus veritatis voluptatem, voluptatum. Aut blanditiis esse et illum maxim, obcaecati possimus
            voluptate! Accusamus <em>adipisci</em> amet aperiam, assumenda consequuntur fugiat inventore iusto magnam molestias
            natus necessitatibus, nulla pariatur.
        </p>
        <blockquote>
            <p>
                Ad aliquid amet asperiores lab distinctio doloremque <code>eaque</code>, exercitationem explicabo, minus mollitia
                natus necessitatibus odio omnis pofro rem.
            </p>
        </blockquote>
        <p>
            Consectetur <code>dicta enim</code> error eveniet expedita, facere in itaque labore <em>natus</em> quasi? Ad consectetur
            eligendi facilis magni quae quis, quo temporibus voluptas voluptate voluptatem!
        </p>
        """
        
        steps_data = [
            {"order": 0, "title": "Introduction", "subtitle": "Introducing the library and how it works"},
            {"order": 1, "title": "Get the sample code", "subtitle": "Where to find the sample code and how to access it"},
            {"order": 2, "title": "Create a Firebase project and Set up your app", "subtitle": "How to create a basic Firebase project and how to run it locally"},
            {"order": 3, "title": "Install the Firebase Command Line Interface", "subtitle": "Setting up the Firebase CLI to access command line tools"},
            {"order": 4, "title": "Deploy and run the web app", "subtitle": "How to build, push and run the project remotely"},
            {"order": 5, "title": "The Functions Directory", "subtitle": "Introducing the Functions and Functions Directory"},
            {"order": 6, "title": "Import the Cloud Functions and Firebase Admin modules", "subtitle": "Create your first Function and run it to administer your app"},
            {"order": 7, "title": "Welcome New Users", "subtitle": "How to create a welcome message for the new users"},
            {"order": 8, "title": "Images moderation", "subtitle": "How to moderate images; crop, resize, optimize"},
            {"order": 9, "title": "New Message Notifications", "subtitle": "How to create and push a notification to a user"},
            {"order": 10, "title": "Congratulations!", "subtitle": "Nice work, you have created your first application"},
        ]
        
        # Create steps for each course
        for course in courses:
            for step_data in steps_data:
                step = Step(
                    id=str(uuid.uuid4()),
                    order=step_data["order"],
                    title=step_data["title"],
                    subtitle=step_data["subtitle"],
                    content=demo_content.format(title=step_data["title"])
                )
                db.add(step)
                course.steps.append(step)
        
        db.commit()
        print("Academy data initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing academy data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_academy_data()