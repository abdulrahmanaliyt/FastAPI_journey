import jwt
from sqlalchemy.exc import IntegrityError

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select

from .database import engine, Base, SessionLocal
from .models import User, Student, Course, Enrollment
from .schemas import (
    UserCreate,
    UserResponse,
    Token,
    StudentCreate,
    StudentResponse,
    CourseCreate,
    CourseResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    StudentWithCoursesResponse,
)
from .security import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)

# Create tables in PostgreSQL automatically
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Course Enrollment System")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------
# AUTHENTICATION & AUTHORIZATION DEPENDENCIES
#-----------------------------------------

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdigit():
            raise credentials_exception

        user = db.get(User, int(user_id))

    except jwt.InvalidTokenError:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user


def require_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user



# API ENDPOINTS

@app.get("/")
def home():
    return {"message": "Welcome to the Student-Course Enrollment System!"}


# --- Auth Endpoints ---

@app.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        role="user"
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return user


@app.post("/auth/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/auth/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@app.get("/admin/dashboard")
def admin_dashboard(
    current_user: User = Depends(require_admin)
):
    return {
        "message": "Welcome to the Admin Dashboard",
        "admin": current_user.email
    }


@app.get("/users", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.scalars(select(User)).all()


# --- 1. Students Endpoints ---

@app.get("/students", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.scalars(select(Student)).all()


@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_in: StudentCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_admin)
):
    student = Student(name=student_in.name)
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Database constraint violation")

    db.refresh(student)
    return student


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student and associated enrollments deleted successfully"
    }


# --- 2. Courses Endpoints ---

@app.post("/courses", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_admin)
):
    course = Course(
        title=course_in.title, 
        duration=course_in.duration, 
        price=course_in.price
    )
    db.add(course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course violates a database constraint")
    
    db.refresh(course)
    return course


@app.get("/courses", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.scalars(select(Course)).all()


@app.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return {
        "message": "Course and associated enrollments deleted successfully"
    }

# --- 3. Enrollments Endpoints ---

@app.get("/enrollments", response_model=list[EnrollmentResponse])
def get_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.scalars(select(Enrollment).options(joinedload(Enrollment.student), joinedload(Enrollment.course))).unique().all()


@app.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_student(
    enrollment_in: EnrollmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.get(Student, enrollment_in.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.get(Course, enrollment_in.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollment = Enrollment(
        student_id=enrollment_in.student_id,
        course_id=enrollment_in.course_id
    )
    db.add(enrollment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student is already enrolled in this course")
    
    db.refresh(enrollment)
    return enrollment


@app.post("/enrollments/bulk", response_model=list[EnrollmentResponse], status_code=status.HTTP_201_CREATED)
def bulk_enroll_students(
    enrollments_in: list[EnrollmentCreate], 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enrollments = []
    try:
        for enrollment_in in enrollments_in:
            student = db.get(Student, enrollment_in.student_id)
            if not student:
                raise HTTPException(status_code=404, detail=f"Student with ID {enrollment_in.student_id} not found")

            course = db.get(Course, enrollment_in.course_id)
            if not course:
                raise HTTPException(status_code=404, detail=f"Course with ID {enrollment_in.course_id} not found")

            enrollment = Enrollment(
                student_id=enrollment_in.student_id,
                course_id=enrollment_in.course_id
            )
            db.add(enrollment)
            enrollments.append(enrollment)

        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Failed to process enrollments")
        
    for enrollment in enrollments:
        db.refresh(enrollment)
    return enrollments

@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    enrollment = db.get(Enrollment, enrollment_id)

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    db.delete(enrollment)
    db.commit()

    return {
        "message": "Enrollment deleted successfully"
    }

# --- 4. Relationship Exploration Endpoints ---

@app.get("/students/{student_id}/courses")
def get_courses_for_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(Student)
        .where(Student.id == student_id)
        .options(
            selectinload(Student.enrollments)
            .selectinload(Enrollment.course)
        )
    )

    student = db.scalars(stmt).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "student": student.name,
        "courses": [
            enrollment.course.title
            for enrollment in student.enrollments
        ]
    }


@app.get("/courses/{course_id}/students")
def get_students_for_course(
    course_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(Course)
        .where(Course.id == course_id)
        .options(
            selectinload(Course.enrollments)
            .selectinload(Enrollment.student)
        )
    )

    course = db.scalars(stmt).first()

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    return {
        "course": course.title,
        "students": [
            enrollment.student.name
            for enrollment in course.enrollments
            if enrollment.student
        ]
    }