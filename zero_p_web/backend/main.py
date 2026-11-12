import os
import uuid
import json
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

import bcrypt
from jose import jwt

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent

load_dotenv(BACKEND_DIR / ".env")
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Depends,
    Header,
    BackgroundTasks
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
    func,
    inspect,
    text
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
    Session
)


# =========================================================
# CONFIG
# =========================================================

BASE = Path(__file__).resolve().parent

DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

UPLOADS = DATA / "uploads"
UPLOADS.mkdir(exist_ok=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///" + str(DATA / "zero_p.db")
)

JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "CHANGE_THIS_IN_PRODUCTION"
)


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    } if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# =========================================================
# DATABASE MODELS
# =========================================================

class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    full_name: Mapped[str] = mapped_column(
        String(150)
    )

    email: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255)
    )

    role: Mapped[str] = mapped_column(
        String(20)
    )

    department: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    college: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    path: Mapped[str] = mapped_column(
        String(500)
    )

    document_type: Mapped[str] = mapped_column(
        String(40)
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class Assignment(Base):

    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id")
    )

    question_paper_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id")
    )

    rubric_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id")
    )

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    assigned_by: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="ASSIGNED"
    )

    due_date: Mapped[str] = mapped_column(
        String(30),
        default=""
    )

    error: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class Evaluation(Base):

    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    assignment_id: Mapped[int] = mapped_column(
        ForeignKey("assignments.id")
    )

    student_name: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    total_mark: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    maximum_mark: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="AI_EVALUATED"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class Score(Base):

    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    evaluation_id: Mapped[int] = mapped_column(
        ForeignKey("evaluations.id")
    )

    student_name: Mapped[str] = mapped_column(
        String(150)
    )

    question_number: Mapped[str] = mapped_column(
        String(30)
    )

    answer_text: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    # ORIGINAL AI MARK
    awarded_mark: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    maximum_mark: Mapped[float] = mapped_column(
        Float,
        default=0
    )

    why_awarded: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    evidence: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    # =====================================================
    # TEACHER OVERRIDE
    # =====================================================

    teacher_override: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    teacher_override_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # =====================================================
    # ADMIN OVERRIDE
    # =====================================================

    admin_override: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    admin_override_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # =====================================================
    # FINAL MARK
    # =====================================================

    final_mark: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    overridden_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    overridden_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


# =========================================================
# CREATE TABLES
# =========================================================

Base.metadata.create_all(engine)


# =========================================================
# DATABASE MIGRATION
# =========================================================

def migrate_database():

    inspector = inspect(engine)

    if "scores" not in inspector.get_table_names():
        return

    columns = {
        column["name"]
        for column in inspector.get_columns("scores")
    }

    migrations = {
        "teacher_override":
            "ALTER TABLE scores ADD COLUMN teacher_override REAL",

        "teacher_override_reason":
            "ALTER TABLE scores ADD COLUMN teacher_override_reason TEXT",

        "admin_override":
            "ALTER TABLE scores ADD COLUMN admin_override REAL",

        "admin_override_reason":
            "ALTER TABLE scores ADD COLUMN admin_override_reason TEXT",

        "final_mark":
            "ALTER TABLE scores ADD COLUMN final_mark REAL",

        "overridden_by":
            "ALTER TABLE scores ADD COLUMN overridden_by INTEGER",

        "overridden_at":
            "ALTER TABLE scores ADD COLUMN overridden_at DATETIME"
    }

    with engine.begin() as connection:

        for column, sql in migrations.items():

            if column not in columns:

                try:
                    connection.execute(text(sql))
                except Exception as error:
                    print(
                        "[Zero-P] Migration warning:",
                        column,
                        error
                    )


migrate_database()


# =========================================================
# SEED USERS
# =========================================================

def seed():

    session = SessionLocal()

    try:

        if not session.query(User).filter_by(
            email="admin@zerop.local"
        ).first():

            session.add(
                User(
                    full_name="System Administrator",
                    email="admin@zerop.local",
                    password_hash=bcrypt.hashpw(
                        b"Admin@123",
                        bcrypt.gensalt()
                    ).decode(),
                    role="ADMIN",
                    department="Administration",
                    college="Zero-P College"
                )
            )

        if not session.query(User).filter_by(
            email="teacher@zerop.local"
        ).first():

            session.add(
                User(
                    full_name="Demo Teacher",
                    email="teacher@zerop.local",
                    password_hash=bcrypt.hashpw(
                        b"Teacher@123",
                        bcrypt.gensalt()
                    ).decode(),
                    role="TEACHER",
                    department="Computer Science",
                    college="Zero-P College"
                )
            )

        session.commit()

    finally:

        session.close()


seed()


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="Zero-P API",
    version="3.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def db():

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


# =========================================================
# AUTH
# =========================================================

def create_token(user):

    return jwt.encode(
        {
            "sub": str(user.id),
            "role": user.role,
            "exp":
                datetime.now(timezone.utc)
                + timedelta(hours=8)
        },
        JWT_SECRET,
        algorithm="HS256"
    )


def current_user(
    authorization: str = Header(default=""),
    session: Session = Depends(db)
):

    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=401,
            detail="Login required"
        )

    try:

        payload = jwt.decode(
            authorization[7:],
            JWT_SECRET,
            algorithms=["HS256"]
        )

        user = session.get(
            User,
            int(payload["sub"])
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired login"
        )

    if not user or not user.is_active:

        raise HTTPException(
            status_code=401,
            detail="Account inactive"
        )

    return user


def admin(
    user=Depends(current_user)
):

    if user.role != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user


# =========================================================
# HEALTH
# =========================================================

@app.get("/api/health")
def health():

    return {
        "status": "ok"
    }


# =========================================================
# LOGIN
# =========================================================

@app.post("/api/auth/login")
def login(
    payload: dict,
    session: Session = Depends(db)
):

    email = (
        payload.get("email") or ""
    ).strip().lower()

    password = (
        payload.get("password") or ""
    ).encode()

    user = session.query(User).filter_by(
        email=email
    ).first()

    if (
        not user
        or not user.is_active
        or not bcrypt.checkpw(
            password,
            user.password_hash.encode()
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "token": create_token(user),
        "user": {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "college": user.college
        }
    }


@app.get("/api/me")
def me(
    user=Depends(current_user)
):

    return {
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "role": user.role,
        "department": user.department,
        "college": user.college
    }


# =========================================================
# TEACHERS
# =========================================================

@app.get("/api/admin/teachers")
def get_teachers(
    _: User = Depends(admin),
    session: Session = Depends(db)
):

    return [
        {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "department": user.department,
            "college": user.college,
            "active": user.is_active
        }

        for user in
        session.query(User)
        .filter_by(role="TEACHER")
        .order_by(User.full_name)
        .all()
    ]


@app.post("/api/admin/teachers")
def create_teacher(
    payload: dict,
    _: User = Depends(admin),
    session: Session = Depends(db)
):

    email = (
        payload.get("email") or ""
    ).strip().lower()

    if (
        not payload.get("full_name")
        or not email
        or not payload.get("password")
    ):

        raise HTTPException(
            status_code=400,
            detail="Name, email and password are required"
        )

    if session.query(User).filter_by(
        email=email
    ).first():

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    user = User(
        full_name=payload["full_name"],
        email=email,
        password_hash=bcrypt.hashpw(
            payload["password"].encode(),
            bcrypt.gensalt()
        ).decode(),
        role="TEACHER",
        department=payload.get(
            "department",
            ""
        ),
        college=payload.get(
            "college",
            ""
        )
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "id": user.id,
        "name": user.full_name,
        "email": user.email
    }


# =========================================================
# DOCUMENT UPLOAD
# =========================================================

async def save_doc(
    file,
    kind,
    user,
    session
):

    extension = Path(
        file.filename or ""
    ).suffix.lower()

    if extension not in {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg"
    }:

        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG and JPEG files are supported"
        )

    name = (
        f"{uuid.uuid4()}{extension}"
    )

    path = UPLOADS / name

    path.write_bytes(
        await file.read()
    )

    document = Document(
        filename=file.filename,
        path=str(path),
        document_type=kind,
        uploaded_by=user.id
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    return {
        "id": document.id,
        "filename": document.filename
    }


@app.post("/api/upload/answer")
async def upload_answer(
    file: UploadFile = File(...),
    user=Depends(current_user),
    session: Session = Depends(db)
):

    return await save_doc(
        file,
        "ANSWER_SCRIPT",
        user,
        session
    )


@app.post("/api/admin/upload/question")
async def upload_question(
    file: UploadFile = File(...),
    user=Depends(admin),
    session: Session = Depends(db)
):

    return await save_doc(
        file,
        "QUESTION_PAPER",
        user,
        session
    )


@app.post("/api/admin/upload/rubric")
async def upload_rubric(
    file: UploadFile = File(...),
    user=Depends(admin),
    session: Session = Depends(db)
):

    return await save_doc(
        file,
        "ANSWER_SCHEMA",
        user,
        session
    )


# =========================================================
# DOCUMENT LISTS
# =========================================================

@app.get("/api/admin/documents")
def documents(
    _: User = Depends(admin),
    session: Session = Depends(db)
):

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "type": document.document_type,
            "uploaded_at":
                document.uploaded_at.isoformat()
        }

        for document in
        session.query(Document)
        .order_by(Document.uploaded_at.desc())
        .all()
    ]


@app.get("/api/admin/unassigned")
def unassigned(
    _: User = Depends(admin),
    session: Session = Depends(db)
):

    assigned = {
        assignment.document_id

        for assignment in
        session.query(Assignment).all()
    }

    documents = (
        session.query(Document)
        .filter_by(
            document_type="ANSWER_SCRIPT"
        )
        .all()
    )

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "uploaded_at":
                document.uploaded_at.isoformat()
        }

        for document in documents
        if document.id not in assigned
    ]


@app.get("/api/admin/question-papers")
def question_papers(
    _: User = Depends(admin),
    session: Session = Depends(db)
):

    return [
        {
            "id": document.id,
            "filename": document.filename
        }

        for document in
        session.query(Document)
        .filter_by(
            document_type="QUESTION_PAPER"
        )
        .order_by(Document.id.desc())
        .all()
    ]


@app.get("/api/admin/rubrics")
def rubrics(
    _: User = Depends(admin),
    session: Session = Depends(db)
):

    return [
        {
            "id": document.id,
            "filename": document.filename
        }

        for document in
        session.query(Document)
        .filter_by(
            document_type="ANSWER_SCHEMA"
        )
        .order_by(Document.id.desc())
        .all()
    ]


# =========================================================
# ASSIGN
# =========================================================

@app.post("/api/admin/assign")
def assign(
    payload: dict,
    administrator: User = Depends(admin),
    session: Session = Depends(db)
):

    document_id = int(
        payload["document_id"]
    )

    teacher_id = int(
        payload["teacher_id"]
    )

    question_paper_id = int(
        payload["question_paper_id"]
    )

    rubric_id = int(
        payload["rubric_id"]
    )

    teacher = session.get(
        User,
        teacher_id
    )

    if (
        not teacher
        or teacher.role != "TEACHER"
    ):

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    for document_id_to_check in [
        document_id,
        question_paper_id,
        rubric_id
    ]:

        if not session.get(
            Document,
            document_id_to_check
        ):

            raise HTTPException(
                status_code=404,
                detail="Required document not found"
            )

    assignment = Assignment(
        document_id=document_id,
        teacher_id=teacher_id,
        question_paper_id=question_paper_id,
        rubric_id=rubric_id,
        assigned_by=administrator.id,
        due_date=payload.get(
            "due_date",
            ""
        )
    )

    session.add(assignment)
    session.commit()
    session.refresh(assignment)

    return {
        "id": assignment.id,
        "status": assignment.status
    }


# =========================================================
# ASSIGNMENTS
# =========================================================

@app.get("/api/assignments")
def assignments(
    user=Depends(current_user),
    session: Session = Depends(db)
):

    query = session.query(Assignment)

    if user.role == "TEACHER":

        query = query.filter_by(
            teacher_id=user.id
        )

    output = []

    for assignment in query.order_by(
        Assignment.assigned_at.desc()
    ).all():

        document = session.get(
            Document,
            assignment.document_id
        )

        teacher = session.get(
            User,
            assignment.teacher_id
        )

        evaluation = (
            session.query(Evaluation)
            .filter_by(assignment_id=assignment.id)
            .order_by(Evaluation.id.desc())
            .first()
        )

        output.append(
            {
                "id": assignment.id,
                "filename":
                    document.filename
                    if document
                    else "",
                "teacher":
                    teacher.full_name
                    if teacher
                    else "",
                "teacher_id":
                    assignment.teacher_id,
                "status":
                    assignment.status,
                "due_date":
                    assignment.due_date,
                "error":
                    assignment.error,
                "evaluation_id":
                    evaluation.id
                    if evaluation
                    else None,
                "score":
                    evaluation.total_mark
                    if evaluation
                    else None,
                "maximum":
                    evaluation.maximum_mark
                    if evaluation
                    else None,
                "model":
                    evaluation.model_name
                    if evaluation
                    else None
            }
        )

    return output


# =========================================================
# PROCESSING
# =========================================================

def process_job(
    assignment_id,
    model
):
    print(
    "### UPDATED PROCESS_JOB IS RUNNING ###",
    flush=True)
    session = SessionLocal()

    assignment = session.get(
        Assignment,
        assignment_id
    )

    if not assignment:

        session.close()
        return

    try:

        assignment.status = "PROCESSING"
        assignment.error = ""

        session.commit()

        from processing_service import (
            run_full_evaluation
        )

        answer = session.get(
            Document,
            assignment.document_id
        )

        question_paper = session.get(
            Document,
            assignment.question_paper_id
        )

        rubric = session.get(
            Document,
            assignment.rubric_id
        )

        result = run_full_evaluation(
            answer.path,
            question_paper.path,
            rubric.path,
            model
        )
        print("\n[DEBUG] run_full_evaluation returned")
        print("[DEBUG] Result type:", type(result))
        print("[DEBUG] Result:", result.keys() if isinstance(result, dict) else "NOT A DICTIONARY")
        print("\n[DEBUG] Extracting evaluation and student data")

        data = result["evaluation"]
        student = result["student"]

        print("[DEBUG] Evaluation type:", type(data))
        print("[DEBUG] Student type:", type(student))

        evaluation = Evaluation(
            assignment_id=assignment.id,
            student_name=
                student.get(
                    "student_name",
                    ""
                ),
            total_mark=float(
                data.get(
                    "total_awarded_marks",
                    0
                )
            ),
            maximum_mark=float(
                data.get(
                    "total_max_marks",
                    0
                )
            ),
            model_name=data.get(
                "model",
                model
            ),
            status="AI_EVALUATED"
        )

        session.add(evaluation)
        session.flush()

        # =================================================
        # OCR ANSWERS
        # =================================================

        answers = {}

        try:

            ocr_data = json.loads(
                Path(
                    result["ocr_path"]
                ).read_text(
                    encoding="utf-8"
                )
            )

            for page in ocr_data.get(
                "pages",
                []
            ):

                for answer_data in (
                    page.get(
                        "answers",
                        []
                    ) or []
                ):

                    number = str(
                        answer_data.get(
                            "answer_number",
                            ""
                        )
                    )

                    text_value = (
                        answer_data.get(
                            "answer_text",
                            ""
                        )
                    )

                    if number:

                        if number in answers:
                            answers[number] += (
                                "\n\n"
                                + text_value
                            )

                        else:
                            answers[number] = text_value

       
        except Exception as error:

            assignment.status = "FAILED"
            assignment.error = str(error)

            session.commit()

            print("\n========== EVALUATION ERROR ==========")
            traceback.print_exc()
            print("======================================\n")


        # =================================================
        # CREATE SCORES
        # =================================================

        for item in data.get(
            "evaluations",
            []
        ):

            question_number = str(
                item.get(
                    "question_number",
                    item.get(
                        "number",
                        ""
                    )
                )
            )

            criteria = item.get(
                "criteria",
                []
            ) or []

            why = (
                item.get(
                    "marking_explanation"
                )
                or item.get(
                    "overall_feedback",
                    ""
                )
            )

            evidence = " | ".join(
                str(
                    criterion.get(
                        "evidence",
                        ""
                    )
                )

                for criterion in criteria

                if criterion.get(
                    "evidence"
                )
            )

            ai_mark = float(
                item.get(
                    "awarded_marks",
                    0
                )
            )

            maximum_mark = float(
                item.get(
                    "max_marks",
                    0
                )
            )

            score = Score(
                evaluation_id=evaluation.id,
                student_name=
                    evaluation.student_name,
                question_number=
                    question_number,
                answer_text=
                    answers.get(
                        question_number,
                        ""
                    ),
                awarded_mark=
                    ai_mark,
                maximum_mark=
                    maximum_mark,
                why_awarded=
                    why,
                evidence=
                    evidence,
                final_mark=
                    ai_mark
            )

            session.add(score)

        assignment.status = "COMPLETED"

        session.commit()

    except Exception as error:

        assignment.status = "FAILED"

        assignment.error = str(error)

        session.commit()

        print(
            "[Zero-P] Evaluation failed:",
            error
        )

    finally:

        session.close()


# =========================================================
# MODELS
# =========================================================

@app.get("/api/evaluation-models")
def evaluation_models(
    user=Depends(current_user)
):

    return {
        "models": [

            {
                "key": "gpt",
                "name": "GPT",
                "model":
                    os.getenv(
                        "WEB_GPT_MODEL",
                        "gpt-5.6-luna"
                    ),
                "provider": "OpenAI",
                "requires": "OPENAI_API_KEY"
            },

            {
                "key": "claude",
                "name": "Claude",
                "model":
                    os.getenv(
                        "WEB_CLAUDE_MODEL",
                        "claude-sonnet-4-6"
                    ),
                "provider": "Anthropic",
                "requires": "ANTHROPIC_API_KEY"
            },

            {
                "key": "llama",
                "name": "Llama",
                "model":
                    os.getenv(
                        "WEB_LLAMA_MODEL",
                        "llama3.1:8b"
                    ),
                "provider": "Ollama",
                "requires": "Local Ollama"
            }

        ]
    }


# =========================================================
# START EVALUATION
# =========================================================

@app.post(
    "/api/evaluate/{assignment_id}"
)
def evaluate(
    assignment_id: int,
    payload: dict,
    background_tasks:
        BackgroundTasks,
    user=Depends(current_user),
    session: Session = Depends(db)
):

    assignment = session.get(
        Assignment,
        assignment_id
    )

    if not assignment:

        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    if (
        user.role == "TEACHER"
        and assignment.teacher_id != user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="This script is not assigned to you"
        )

    if assignment.status == "PROCESSING":

        return {
            "status": "processing",
            "assignment_id":
                assignment.id
        }

    requested = (
        payload.get("model") or ""
    ).strip().lower()

    model_map = {

        "gpt":
            os.getenv(
                "WEB_GPT_MODEL",
                "gpt-5.6-luna"
            ),

        "claude":
            os.getenv(
                "WEB_CLAUDE_MODEL",
                "claude-sonnet-4-6"
            ),

        "llama":
            os.getenv(
                "WEB_LLAMA_MODEL",
                "llama3.1:8b"
            )
    }

    if requested not in model_map:

        raise HTTPException(
            status_code=400,
            detail="Choose one of: gpt, claude, llama"
        )

    model = model_map[requested]

    background_tasks.add_task(
        process_job,
        assignment.id,
        model
    )

    return {
        "status": "queued",
        "assignment_id":
            assignment.id,
        "model_key":
            requested,
        "model":
            model
    }


# =========================================================
# GET EVALUATION
# =========================================================

@app.get(
    "/api/evaluations/{evaluation_id}"
)
def evaluation(
    evaluation_id: int,
    user=Depends(current_user),
    session: Session = Depends(db)
):

    evaluation = session.get(
        Evaluation,
        evaluation_id
    )

    if not evaluation:

        raise HTTPException(
            status_code=404,
            detail="Evaluation not found"
        )

    assignment = session.get(
        Assignment,
        evaluation.assignment_id
    )

    if (
        user.role == "TEACHER"
        and assignment.teacher_id != user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    scores = (
        session.query(Score)
        .filter_by(
            evaluation_id=evaluation.id
        )
        .order_by(Score.id)
        .all()
    )

    return {

        "id":
            evaluation.id,

        "student_name":
            evaluation.student_name,

        "total_mark":
            evaluation.total_mark,

        "maximum_mark":
            evaluation.maximum_mark,

        "model_name":
            evaluation.model_name,

        "status":
            evaluation.status,

        "scores": [

            {

                "id":
                    score.id,

                "question_number":
                    score.question_number,

                "answer_text":
                    score.answer_text,

                "awarded_mark":
                    score.awarded_mark,

                "maximum_mark":
                    score.maximum_mark,

                "why_awarded":
                    score.why_awarded,

                "evidence":
                    score.evidence,

                "teacher_override":
                    score.teacher_override,

                "teacher_override_reason":
                    score.teacher_override_reason,

                "admin_override":
                    score.admin_override,

                "admin_override_reason":
                    score.admin_override_reason,

                "final_mark":
                    score.final_mark
                    if score.final_mark is not None
                    else score.awarded_mark
            }

            for score in scores
        ]
    }


# =========================================================
# OVERRIDE MARK
# =========================================================

@app.put(
    "/api/evaluations/{evaluation_id}/scores/{score_id}"
)
def override_mark(
    evaluation_id: int,
    score_id: int,
    payload: dict,
    user=Depends(current_user),
    session: Session = Depends(db)
):

    # -----------------------------------------------------
    # ONLY ADMIN OR TEACHER
    # -----------------------------------------------------

    if user.role not in {
        "ADMIN",
        "TEACHER"
    }:

        raise HTTPException(
            status_code=403,
            detail="Only Admin or Teacher can override marks."
        )

    # -----------------------------------------------------
    # FIND SCORE
    # -----------------------------------------------------

    score = session.get(
        Score,
        score_id
    )

    if not score:

        raise HTTPException(
            status_code=404,
            detail="Score not found."
        )

    if score.evaluation_id != evaluation_id:

        raise HTTPException(
            status_code=400,
            detail="Score does not belong to this evaluation."
        )

    evaluation = session.get(
        Evaluation,
        evaluation_id
    )

    if not evaluation:

        raise HTTPException(
            status_code=404,
            detail="Evaluation not found."
        )

    assignment = session.get(
        Assignment,
        evaluation.assignment_id
    )

    # -----------------------------------------------------
    # TEACHER CAN ONLY CHANGE OWN ASSIGNMENTS
    # -----------------------------------------------------

    if (
        user.role == "TEACHER"
        and assignment.teacher_id != user.id
    ):

        raise HTTPException(
            status_code=403,
            detail="You can only override marks for your own assignments."
        )

    # -----------------------------------------------------
    # MARK
    # -----------------------------------------------------

    try:

        mark = float(
            payload.get("mark")
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Mark must be a number."
        )

    if mark < 0:

        raise HTTPException(
            status_code=400,
            detail="Mark cannot be negative."
        )

    if mark > score.maximum_mark:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Mark cannot exceed "
                f"{score.maximum_mark}."
            )
        )

    reason = (
        payload.get("reason") or ""
    ).strip()

    if not reason:

        raise HTTPException(
            status_code=400,
            detail="Override reason is required."
        )

    # -----------------------------------------------------
    # SAVE OVERRIDE
    # -----------------------------------------------------

    now = datetime.now(
        timezone.utc
    )

    if user.role == "TEACHER":

        score.teacher_override = mark

        score.teacher_override_reason = reason

    elif user.role == "ADMIN":

        score.admin_override = mark

        score.admin_override_reason = reason

    score.overridden_by = user.id

    score.overridden_at = now

    # -----------------------------------------------------
    # FINAL MARK PRIORITY
    #
    # ADMIN > TEACHER > AI
    # -----------------------------------------------------

    if score.admin_override is not None:

        score.final_mark = (
            score.admin_override
        )

    elif score.teacher_override is not None:

        score.final_mark = (
            score.teacher_override
        )

    else:

        score.final_mark = (
            score.awarded_mark
        )

    # -----------------------------------------------------
    # RECALCULATE TOTAL
    # -----------------------------------------------------

    total = (
        session.query(
            func.coalesce(
                func.sum(
                    Score.final_mark
                ),
                0
            )
        )
        .filter(
            Score.evaluation_id ==
            evaluation.id
        )
        .scalar()
    )

    evaluation.total_mark = (
        float(total or 0)
    )

    if user.role == "ADMIN":

        evaluation.status = "ADMIN_REVIEWED"

    else:

        evaluation.status = "TEACHER_REVIEWED"

    session.commit()

    session.refresh(score)

    return {

        "success":
            True,

        "score_id":
            score.id,

        "ai_mark":
            score.awarded_mark,

        "teacher_override":
            score.teacher_override,

        "admin_override":
            score.admin_override,

        "final_mark":
            score.final_mark,

        "maximum_mark":
            score.maximum_mark,

        "evaluation_total":
            evaluation.total_mark,

        "overridden_by":
            user.id,

        "overridden_role":
            user.role,

        "overridden_at":
            score.overridden_at.isoformat()
    }