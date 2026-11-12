import logo from "./assets/logo2.jpeg";
import background from "./assets/logo1.jpeg";

import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import {
  LayoutDashboard,
  Users,
  Upload,
  ClipboardList,
  FileText,
  LogOut,
  UserCheck,
  ChevronRight,
  CheckCircle2,
  Clock3,
  AlertTriangle,
  Eye,
  ShieldCheck
} from "lucide-react";

import "./styles.css";


/* =========================================================
   API
========================================================= */

const API =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";


function auth() {
  return {
    Authorization:
      "Bearer " +
      localStorage.getItem("zp_token")
  };
}


/* =========================================================
   GET
========================================================= */

async function get(path) {

  const response = await fetch(
    API + path,
    {
      headers: auth()
    }
  );

  const data =
    await response.json();

  if (!response.ok) {

    throw Error(
      data.detail ||
      "Request failed"
    );
  }

  return data;
}


/* =========================================================
   POST
========================================================= */

async function post(path, body) {

  const response = await fetch(
    API + path,
    {
      method: "POST",

      headers: {
        ...auth(),
        "Content-Type":
          "application/json"
      },

      body:
        JSON.stringify(body)
    }
  );

  const data =
    await response.json();

  if (!response.ok) {

    throw Error(
      data.detail ||
      "Request failed"
    );
  }

  return data;
}


/* =========================================================
   PUT
========================================================= */

async function put(path, body) {

  const response = await fetch(
    API + path,
    {
      method: "PUT",

      headers: {
        ...auth(),
        "Content-Type":
          "application/json"
      },

      body:
        JSON.stringify(body)
    }
  );

  const data =
    await response.json();

  if (!response.ok) {

    throw Error(
      data.detail ||
      "Request failed"
    );
  }

  return data;
}


/* =========================================================
   APP
========================================================= */

function App() {

  const [token, setToken] =
    useState(
      localStorage.getItem(
        "zp_token"
      )
    );

  const [user, setUser] =
    useState(
      JSON.parse(
        localStorage.getItem(
          "zp_user"
        ) || "null"
      )
    );


  if (!token || !user) {

    return (

      <Login

        done={(data) => {

          localStorage.setItem(
            "zp_token",
            data.token
          );

          localStorage.setItem(
            "zp_user",
            JSON.stringify(
              data.user
            )
          );

          setToken(
            data.token
          );

          setUser(
            data.user
          );

        }}

      />

    );
  }


  return (

    <Portal

      user={user}

      logout={() => {

        localStorage.removeItem(
          "zp_token"
        );

        localStorage.removeItem(
          "zp_user"
        );

        setToken(null);
        setUser(null);

      }}

    />

  );
}


/* =========================================================
   LOGIN
========================================================= */

function Login({ done }) {

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");


  async function login(event) {

    event.preventDefault();

    setError("");


    try {

      const response =
        await fetch(
          API +
          "/api/auth/login",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body:
              JSON.stringify({
                email,
                password
              })
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw Error(
          data.detail ||
          "Login failed"
        );
      }


      done(data);

    } catch (error) {

      setError(
        error.message
      );

    }
  }


  return (

    <div

      className="login"

      style={{
        backgroundImage:
          `url(${background})`
      }}

    >

      <div className="loginOverlay">

        <div className="loginCard">

          <div className="logo">

            <img
              src={logo}
              alt="EvaLink Logo"
            />

            <span>

              EvaLink

              <small>
                AI Answer Evaluation
              </small>

            </span>

          </div>


          <p className="eyebrow">
            College evaluation portal
          </p>


          <h1>
            Sign in
          </h1>


          <p className="muted">
            Use your college account
            to continue.
          </p>


          <form
            onSubmit={login}
          >

            <label>

              Email

              <input

                type="email"

                placeholder=
                  "name@college.edu"

                value={email}

                onChange={(event) =>
                  setEmail(
                    event.target.value
                  )
                }

                required

              />

            </label>


            <label>

              Password

              <input

                type="password"

                placeholder=
                  "Password"

                value={password}

                onChange={(event) =>
                  setPassword(
                    event.target.value
                  )
                }

                required

              />

            </label>


            {error && (

              <div className="error">

                {error}

              </div>

            )}


            <button
              className="primary full"
              type="submit"
            >

              Sign in

              <ChevronRight
                size={16}
              />

            </button>

          </form>


          <div className="loginHint">

            Admin and Teacher permissions
            are enforced by the backend.

          </div>

        </div>

      </div>

    </div>

  );
}


/* =========================================================
   PORTAL
========================================================= */

function Portal({
  user,
  logout
}) {

  const isAdmin =
    user.role === "ADMIN";


  const [page, setPage] =
    useState("dashboard");


  const [refresh, setRefresh] =
    useState(0);


  return (

    <div className="app">


      {/* =================================================
          SIDEBAR
      ================================================= */}

      <aside>


        <div className="brand">

          <img
            src={logo}
            alt="EvaLink Logo"
          />

          <div>

            <strong>
              EvaLink
            </strong>

            <small>
              College evaluation
            </small>

          </div>

        </div>


        <div className="role">

          {isAdmin
            ? "ADMIN"
            : "TEACHER"}

          {" "}PORTAL

        </div>


        <nav>


          {(

            isAdmin

              ?

              [

                [
                  "dashboard",
                  "Dashboard",
                  LayoutDashboard
                ],

                [
                  "assign",
                  "Assignments",
                  UserCheck
                ],

                [
                  "teachers",
                  "Teachers",
                  Users
                ],

                [
                  "documents",
                  "Documents",
                  FileText
                ]

              ]

              :

              [

                [
                  "dashboard",
                  "Dashboard",
                  LayoutDashboard
                ],

                [
                  "assign",
                  "My assignments",
                  ClipboardList
                ]

              ]

          ).map(
            ([id, label, Icon]) => (

              <button

                key={id}

                className={
                  page === id
                    ? "active"
                    : ""
                }

                onClick={() =>
                  setPage(id)
                }

              >

                <Icon size={17} />

                {label}

              </button>

            )
          )}

        </nav>


        <div className="sideBottom">


          <div className="profile">

            <div className="avatar">

              {user.name?.[0] ||
                "U"}

            </div>


            <div>

              <b>
                {user.name}
              </b>

              <small>
                {user.department ||
                  user.role}
              </small>

            </div>

          </div>


          <button
            onClick={logout}
          >

            <LogOut
              size={15}
            />

            Sign out

          </button>

        </div>

      </aside>


      {/* =================================================
          MAIN
      ================================================= */}

      <main>


        <header>

          <div>

            <p className="eyebrow">

              {isAdmin
                ? "Administration"
                : "Teacher workspace"}

            </p>


            <h1>

              {page === "dashboard"

                ? "Dashboard"

                : page === "assign"

                ? (
                    isAdmin
                      ? "Assign answer scripts"
                      : "My assignments"
                  )

                : page === "teachers"

                ? "Teacher accounts"

                : "Documents"

              }

            </h1>

          </div>


          <div className="user">

            {user.name}

            <div className="avatar dark">

              {user.name?.[0] ||
                "U"}

            </div>

          </div>

        </header>


        {page === "dashboard" && (

          <Dashboard

            admin={isAdmin}

            go={setPage}

            refresh={refresh}

          />

        )}


        {page === "assign" && (

          <Assignments

            admin={isAdmin}

            refresh={refresh}

            bump={() =>
              setRefresh(
                value =>
                  value + 1
              )
            }

          />

        )}


        {page === "teachers" && (

          <Teachers />

        )}


        {page === "documents" && (

          <Documents />

        )}

      </main>

    </div>

  );
}


/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard({
  admin,
  go
}) {

  const [rows, setRows] =
    useState([]);


  useEffect(() => {

    get("/api/assignments")

      .then(setRows)

      .catch(() => {});

  }, []);


  return (

    <section>


      <div className="hero">

        <div>

          <span className="pill">

            {admin
              ? "College administration"
              : "Evaluation queue"}

          </span>


          <h2>

            {admin

              ? "Distribute marking work across the college."

              : "Review the answer scripts assigned to you."

            }

          </h2>


          <p>

            {admin

              ? "Upload papers and rubrics, assign scripts to teachers by department, and track completion."

              : "Evaluate assigned scripts and inspect why each mark was awarded."

            }

          </p>

        </div>


        <button

          className="primary"

          onClick={() =>
            go("assign")
          }

        >

          {admin
            ? "Assign scripts"
            : "Open assignments"}

          <ChevronRight
            size={16}
          />

        </button>

      </div>


      <div className="stats">


        <Card

          icon={ClipboardList}

          label="Assignments"

          value={
            rows.length
          }

        />


        <Card

          icon={CheckCircle2}

          label="Completed"

          value={
            rows.filter(
              x =>
                x.status ===
                "COMPLETED"
            ).length
          }

        />


        <Card

          icon={Clock3}

          label="Processing"

          value={
            rows.filter(
              x =>
                x.status ===
                "PROCESSING"
            ).length
          }

        />


        <Card

          icon={AlertTriangle}

          label="Failed"

          value={
            rows.filter(
              x =>
                x.status ===
                "FAILED"
            ).length
          }

        />

      </div>


      <div className="sectionHead">

        <div>

          <h3>
            Recent assignments
          </h3>

          <p>
            Every answer script has
            one accountable teacher.
          </p>

        </div>

      </div>


      <AssignmentTable
        rows={rows}
      />

    </section>

  );
}


/* =========================================================
   CARD
========================================================= */

function Card({
  icon: Icon,
  label,
  value
}) {

  return (

    <div className="stat">

      <Icon size={17} />

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  );
}


/* =========================================================
   ASSIGNMENT TABLE
========================================================= */

function AssignmentTable({
  rows
}) {

  const [open, setOpen] =
    useState(null);


  return (

    <div className="table">


      <div className="thead">

        <span>
          Answer script
        </span>

        <span>
          Teacher
        </span>

        <span>
          Status
        </span>

        <span>
          Result
        </span>

        <span></span>

      </div>


      {rows.map(item => (

        <React.Fragment
          key={item.id}
        >

          <div className="tr">


            <span>

              <b>
                {item.filename}
              </b>

              <small>
                Assignment #{item.id}
              </small>

            </span>


            <span>
              {item.teacher}
            </span>


            <span>

              <em
                className={
                  "status " +
                  (
                    item.status ||
                    ""
                  ).toLowerCase()
                }
              >

                {item.status}

              </em>


              {item.error && (

                <small className="errText">

                  {item.error.slice(
                    0,
                    90
                  )}

                </small>

              )}

            </span>


            <span>

              {item.score != null

                ? `${item.score}/${item.maximum}`

                : "—"

              }

            </span>


            <button

              className="icon"

              onClick={() => {

                if (
                  item.evaluation_id
                ) {

                  setOpen(
                    item.evaluation_id
                  );

                }

              }}

            >

              {item.evaluation_id && (

                <Eye size={17} />

              )}

            </button>

          </div>


          {open ===
            item.evaluation_id && (

            <Evaluation

              id={open}

              close={() =>
                setOpen(null)
              }

            />

          )}

        </React.Fragment>

      ))}


      {!rows.length && (

        <div className="emptyRow">

          No assignments yet.

        </div>

      )}

    </div>

  );
}


/* =========================================================
   ASSIGNMENTS
========================================================= */

function Assignments({
  admin,
  bump
}) {

  const [rows, setRows] =
    useState([]);

  const [docs, setDocs] =
    useState([]);

  const [teachers, setTeachers] =
    useState([]);

  const [qps, setQps] =
    useState([]);

  const [rubrics, setRubrics] =
    useState([]);


  const [form, setForm] =
    useState({

      doc: "",
      teacher: "",
      qp: "",
      rub: "",
      due: ""

    });


  const [message, setMessage] =
    useState("");


  const [chooser, setChooser] =
    useState(null);


  const [models, setModels] =
    useState([]);


  const [modelLoading, setModelLoading] =
    useState(false);


  function load() {

    get("/api/assignments")
      .then(setRows)
      .catch(() => {});


    if (admin) {

      get("/api/admin/unassigned")
        .then(setDocs)
        .catch(() => {});


      get("/api/admin/teachers")
        .then(setTeachers)
        .catch(() => {});


      get("/api/admin/question-papers")
        .then(setQps)
        .catch(() => {});


      get("/api/admin/rubrics")
        .then(setRubrics)
        .catch(() => {});

    }

  }


  useEffect(() => {

    load();

  }, []);


  async function upload(
    path,
    file
  ) {

    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );


    try {

      const response =
        await fetch(
          API + path,
          {
            method: "POST",
            headers: auth(),
            body: formData
          }
        );


      const data =
        await response.json();


      setMessage(

        response.ok

          ? "Uploaded successfully."

          : (
              data.detail ||
              "Upload failed."
            )

      );


      load();

    } catch (error) {

      setMessage(
        error.message
      );

    }

  }


  async function assign() {

    try {

      await post(
        "/api/admin/assign",
        {
          document_id:
            Number(form.doc),

          teacher_id:
            Number(form.teacher),

          question_paper_id:
            Number(form.qp),

          rubric_id:
            Number(form.rub),

          due_date:
            form.due
        }
      );


      setMessage(
        "Answer script assigned."
      );


      setForm({
        doc: "",
        teacher: "",
        qp: "",
        rub: "",
        due: ""
      });


      load();

      bump();

    } catch (error) {

      setMessage(
        error.message
      );

    }

  }


  async function openModelChooser(
    id
  ) {

    setModelLoading(true);

    setMessage("");


    try {

      const available =
        await get(
          "/api/evaluation-models"
        );


      setModels(
        available.models || []
      );


      setChooser(id);

    } catch (error) {

      setMessage(
        error.message
      );

    } finally {

      setModelLoading(false);

    }

  }


  async function evaluateWithModel(
    modelKey
  ) {

    const id =
      chooser;


    setChooser(null);


    setMessage(
      "Starting evaluation with " +
      modelKey.toUpperCase() +
      "…"
    );


    try {

      const result =
        await post(
          "/api/evaluate/" +
          id,
          {
            model:
              modelKey
          }
        );


      setMessage(
        "Evaluation started with " +
        (
          result.model ||
          modelKey
        ) +
        "."
      );


      load();


      setTimeout(
        load,
        2500
      );


      setTimeout(
        load,
        7000
      );


    } catch (error) {

      setMessage(
        error.message
      );

    }

  }


  return (

    <section>


      {admin && (

        <>


          {/* =================================================
              UPLOADS
          ================================================= */}

          <div className="assignBox">

            <div>

              <p className="eyebrow">
                Admin setup
              </p>

              <h3>
                Evaluation inputs
              </h3>

              <p>
                Upload the question paper,
                valuation scheme and answer
                scripts.
              </p>

            </div>


            <div className="uploadRow">


              <label className="upload">

                <Upload size={17} />

                Question paper

                <input

                  type="file"

                  accept=".pdf"

                  onChange={event => {

                    const file =
                      event.target
                        .files?.[0];

                    if (file) {

                      upload(
                        "/api/admin/upload/question",
                        file
                      );

                    }

                  }}

                />

              </label>


              <label className="upload">

                <Upload size={17} />

                Answer schema / rubric

                <input

                  type="file"

                  accept=".pdf"

                  onChange={event => {

                    const file =
                      event.target
                        .files?.[0];

                    if (file) {

                      upload(
                        "/api/admin/upload/rubric",
                        file
                      );

                    }

                  }}

                />

              </label>


              <label className="upload">

                <Upload size={17} />

                Answer script

                <input

                  type="file"

                  accept=".pdf,.png,.jpg,.jpeg"

                  onChange={event => {

                    const file =
                      event.target
                        .files?.[0];

                    if (file) {

                      upload(
                        "/api/upload/answer",
                        file
                      );

                    }

                  }}

                />

              </label>

            </div>

          </div>


          {/* =================================================
              ASSIGNMENT
          ================================================= */}

          <div className="assignBox">

            <p className="eyebrow">
              Assignment
            </p>

            <h3>
              Send a script to a teacher
            </h3>


            <div className="formGrid">


              <Select

                label="Answer script"

                value={form.doc}

                set={value =>
                  setForm({
                    ...form,
                    doc: value
                  })
                }

                items={
                  docs.map(
                    item => [
                      item.id,
                      item.filename
                    ]
                  )
                }

              />


              <Select

                label="Teacher"

                value={form.teacher}

                set={value =>
                  setForm({
                    ...form,
                    teacher: value
                  })
                }

                items={
                  teachers.map(
                    item => [
                      item.id,
                      `${item.name} · ${item.department}`
                    ]
                  )
                }

              />


              <Select

                label="Question paper"

                value={form.qp}

                set={value =>
                  setForm({
                    ...form,
                    qp: value
                  })
                }

                items={
                  qps.map(
                    item => [
                      item.id,
                      item.filename
                    ]
                  )
                }

              />


              <Select

                label="Rubric"

                value={form.rub}

                set={value =>
                  setForm({
                    ...form,
                    rub: value
                  })
                }

                items={
                  rubrics.map(
                    item => [
                      item.id,
                      item.filename
                    ]
                  )
                }

              />


              <label>

                Due date

                <input

                  type="date"

                  value={form.due}

                  onChange={event =>
                    setForm({
                      ...form,
                      due:
                        event.target.value
                    })
                  }

                />

              </label>


              <button

                className="primary"

                onClick={assign}

              >

                Assign

                <UserCheck
                  size={16}
                />

              </button>

            </div>

          </div>

        </>

      )}


      {message && (

        <div className="notice">

          {message}

        </div>

      )}


      <div className="sectionHead">

        <div>

          <h3>

            {admin
              ? "All assignments"
              : "My assigned answer scripts"}

          </h3>

          <p>

            {admin
              ? "Monitor work across departments."
              : "Only scripts assigned to your account are shown."}

          </p>

        </div>

      </div>


      <div className="table">


        <div className="thead">

          <span>
            Script
          </span>

          <span>

            {admin
              ? "Teacher"
              : "Due date"}

          </span>

          <span>
            Status
          </span>

          <span>
            Result
          </span>

          <span>
            Action
          </span>

        </div>


        {rows.map(item => (

          <div
            className="tr"
            key={item.id}
          >


            <span>

              <b>
                {item.filename}
              </b>

              <small>
                #{item.id}
              </small>

            </span>


            <span>

              {admin
                ? item.teacher
                : item.due_date ||
                  "—"}

            </span>


            <span>

              <em
                className={
                  "status " +
                  (
                    item.status ||
                    ""
                  ).toLowerCase()
                }
              >

                {item.status}

              </em>

            </span>


            <span>

              {item.score != null

                ? `${item.score}/${item.maximum}`

                : "—"

              }

            </span>


            <span>

              {!admin &&
                item.status !==
                  "PROCESSING" && (

                <button

                  className="primary mini"

                  onClick={() =>
                    openModelChooser(
                      item.id
                    )
                  }

                >

                  {item.status ===
                    "COMPLETED"

                    ? "Re-run"

                    : "Evaluate"

                  }

                </button>

              )}

            </span>

          </div>

        ))}


      </div>


      {/* =================================================
          MODEL LOADING
      ================================================= */}

      {modelLoading && (

        <div className="modelModal">

          <div className="modelDialog">

            <div className="spinnerLine">

              Loading available
              evaluation models…

            </div>

          </div>

        </div>

      )}


      {/* =================================================
          MODEL SELECTOR
      ================================================= */}

      {chooser && (

        <div

          className="modelModal"

          onClick={() =>
            setChooser(null)
          }

        >

          <div

            className="modelDialog"

            onClick={event =>
              event.stopPropagation()
            }

          >

            <div className="modelDialogHead">

              <div>

                <p className="eyebrow">
                  Step before evaluation
                </p>

                <h3>
                  Choose the AI model
                </h3>

                <p>
                  Select which evaluator
                  should score this
                  answer script.
                </p>

              </div>


              <button

                className="closeBtn"

                onClick={() =>
                  setChooser(null)
                }

              >
                ×
              </button>

            </div>


            <div className="modelGrid">


              {models.map(model => (

                <button

                  className="modelCard"

                  key={model.key}

                  onClick={() =>
                    evaluateWithModel(
                      model.key
                    )
                  }

                >

                  <div className="modelLogo">

                    {model.name[0]}

                  </div>


                  <div className="modelInfo">

                    <b>
                      {model.name}
                    </b>

                    <span>
                      {model.model}
                    </span>

                    <small>
                      {model.provider}
                      {" · "}
                      {model.requires}
                    </small>

                  </div>


                  <ChevronRight
                    size={18}
                  />

                </button>

              ))}

            </div>


            <div className="modelNote">

              <ShieldCheck
                size={15}
              />

              The same question schema
              and student OCR are sent
              to whichever model you select.

            </div>

          </div>

        </div>

      )}

    </section>

  );
}


/* =========================================================
   SELECT
========================================================= */

function Select({
  label,
  value,
  set,
  items
}) {

  return (

    <label>

      {label}

      <select

        value={value}

        onChange={event =>
          set(
            event.target.value
          )
        }

      >

        <option value="">
          Choose
        </option>


        {items.map(
          ([id, name]) => (

            <option

              value={id}

              key={id}

            >

              {name}

            </option>

          )
        )}

      </select>

    </label>

  );
}


/* =========================================================
   TEACHERS
========================================================= */

function Teachers() {

  const [rows, setRows] =
    useState([]);


  const [form, setForm] =
    useState({

      full_name: "",
      email: "",
      password: "",
      department: "",
      college: ""

    });


  const [message, setMessage] =
    useState("");


  function load() {

    get("/api/admin/teachers")

      .then(setRows)

      .catch(() => {});

  }


  useEffect(() => {

    load();

  }, []);


  async function save() {

    try {

      await post(
        "/api/admin/teachers",
        form
      );


      setMessage(
        "Teacher account created."
      );


      setForm({

        full_name: "",
        email: "",
        password: "",
        department: "",
        college: ""

      });


      load();

    } catch (error) {

      setMessage(
        error.message
      );

    }

  }


  return (

    <section>


      <div className="sectionHead">

        <div>

          <h3>
            Teacher accounts
          </h3>

          <p>
            Each teacher gets an
            independent login.
          </p>

        </div>

      </div>


      <div className="assignBox">

        <div className="formGrid">


          {Object.keys(form).map(
            key => (

              <label key={key}>

                {key.replace(
                  "_",
                  " "
                )}

                <input

                  type={
                    key === "password"
                      ? "password"
                      : "text"
                  }

                  value={
                    form[key]
                  }

                  onChange={event =>
                    setForm({
                      ...form,
                      [key]:
                        event.target
                          .value
                    })
                  }

                />

              </label>

            )
          )}


          <button

            className="primary"

            onClick={save}

          >

            Create teacher

          </button>

        </div>


        {message && (

          <div className="notice">

            {message}

          </div>

        )}

      </div>


      <div className="table">


        <div className="thead">

          <span>
            Name
          </span>

          <span>
            Email
          </span>

          <span>
            Department
          </span>

          <span>
            College
          </span>

          <span>
            Status
          </span>

        </div>


        {rows.map(item => (

          <div
            className="tr"
            key={item.id}
          >

            <span>
              <b>
                {item.name}
              </b>
            </span>

            <span>
              {item.email}
            </span>

            <span>
              {item.department}
            </span>

            <span>
              {item.college}
            </span>

            <span>

              <em className="status completed">

                Active

              </em>

            </span>

          </div>

        ))}

      </div>

    </section>

  );
}


/* =========================================================
   DOCUMENTS
========================================================= */

function Documents() {

  const [rows, setRows] =
    useState([]);


  useEffect(() => {

    get("/api/admin/documents")

      .then(setRows)

      .catch(() => {});

  }, []);


  return (

    <section>


      <div className="sectionHead">

        <div>

          <h3>
            Document repository
          </h3>

          <p>
            Question papers, rubrics
            and answer scripts.
          </p>

        </div>

      </div>


      <div className="table">


        <div className="thead">

          <span>
            File
          </span>

          <span>
            Type
          </span>

          <span>
            Uploaded
          </span>

          <span></span>

          <span></span>

        </div>


        {rows.map(item => (

          <div
            className="tr"
            key={item.id}
          >

            <span>

              <b>
                {item.filename}
              </b>

              <small>
                Document #{item.id}
              </small>

            </span>


            <span>
              {item.type}
            </span>


            <span>

              {new Date(
                item.uploaded_at
              ).toLocaleString()}

            </span>


            <span></span>

            <span></span>

          </div>

        ))}

      </div>

    </section>

  );
}


/* =========================================================
   EVALUATION
   BOTH ADMIN + TEACHER OVERRIDE
========================================================= */

function Evaluation({
  id,
  close
}) {

  const [result, setResult] =
    useState(null);


  const [editing, setEditing] =
    useState(null);


  const [mark, setMark] =
    useState("");


  const [reason, setReason] =
    useState("");


  const [saving, setSaving] =
    useState(false);


  const [message, setMessage] =
    useState("");


  const currentUser =
    JSON.parse(
      localStorage.getItem(
        "zp_user"
      ) || "null"
    );


  const canOverride =
    currentUser &&
    (
      currentUser.role ===
      "ADMIN"
      ||
      currentUser.role ===
      "TEACHER"
    );


  async function load() {

    try {

      const data =
        await get(
          "/api/evaluations/" +
          id
        );

      setResult(data);

    } catch (error) {

      setMessage(
        error.message
      );

    }

  }


  useEffect(() => {

    load();

  }, [id]);


  /* =======================================================
     START OVERRIDE
  ======================================================= */

  function startOverride(
    score
  ) {

    const currentMark =

      score.admin_override
      ??
      score.teacher_override
      ??
      score.final_mark
      ??
      score.awarded_mark;


    setEditing(
      score.id
    );


    setMark(
      String(currentMark)
    );


    setReason("");


    setMessage("");

  }


  /* =======================================================
     CANCEL
  ======================================================= */

  function cancelOverride() {

    setEditing(null);

    setMark("");

    setReason("");

  }


  /* =======================================================
     SAVE OVERRIDE
  ======================================================= */

  async function saveOverride(
    score
  ) {

    const numericMark =
      Number(mark);


    if (
      !Number.isFinite(
        numericMark
      )
      ||
      numericMark < 0
      ||
      numericMark >
        Number(
          score.maximum_mark
        )
    ) {

      setMessage(
        `Enter a mark between 0 and ${score.maximum_mark}.`
      );

      return;

    }


    if (!reason.trim()) {

      setMessage(
        "Please enter a reason for the override."
      );

      return;

    }


    setSaving(true);

    setMessage("");


    try {

      await put(

        `/api/evaluations/${id}/scores/${score.id}`,

        {
          mark:
            numericMark,

          reason:
            reason.trim()
        }

      );


      setMessage(
        "Mark override saved successfully."
      );


      cancelOverride();


      await load();

    } catch (error) {

      setMessage(
        error.message
      );

    } finally {

      setSaving(false);

    }

  }


  if (!result) {

    return (

      <div className="evalInline">

        Loading result…

      </div>

    );

  }


  return (

    <div className="evalInline">


      {/* =================================================
          EVALUATION HEADER
      ================================================= */}

      <div className="evalTop">


        <div>

          <p className="eyebrow">

            {result.model_name}

          </p>


          <h3>

            {result.student_name ||
              "Student"}

          </h3>


          <p className="muted">

            Original AI evaluation
            is preserved even after
            an override.

          </p>

        </div>


        <div className="scoreBig">

          {result.total_mark}

          <small>

            / {result.maximum_mark}

          </small>

        </div>


        <button

          className="icon"

          onClick={close}

        >

          ×

        </button>

      </div>


      {message && (

        <div className="notice">

          {message}

        </div>

      )}


      {/* =================================================
          SCORES
      ================================================= */}

      {result.scores.map(
        score => {


          const finalMark =

            score.admin_override
            ??
            score.teacher_override
            ??
            score.final_mark
            ??
            score.awarded_mark;


          return (

            <div

              className="scoreRow scoreRowEditable"

              key={score.id}

            >


              <div className="scoreContent">


                <div className="scoreQuestionHead">


                  <b>

                    Question{" "}

                    {score.question_number}

                  </b>


                  <span className="scoreBadge">

                    Final:{" "}

                    {finalMark}

                    /

                    {score.maximum_mark}

                  </span>

                </div>


                {/* =======================================
                    STUDENT ANSWER
                ======================================= */}

                <p className="answer">

                  {score.answer_text}

                </p>


                {/* =======================================
                    AI MARK
                ======================================= */}

                <div className="why">

                  <strong>
                    AI mark:
                  </strong>{" "}

                  {score.awarded_mark}

                  /

                  {score.maximum_mark}


                  {score.why_awarded && (

                    <>

                      {" — "}

                      {score.why_awarded}

                    </>

                  )}

                </div>


                {/* =======================================
                    EVIDENCE
                ======================================= */}

                {score.evidence && (

                  <div className="evidence">

                    <strong>
                      Evidence:
                    </strong>{" "}

                    {score.evidence}

                  </div>

                )}


                {/* =======================================
                    TEACHER OVERRIDE
                ======================================= */}

                {score.teacher_override !==
                  null &&
                  score.teacher_override !==
                  undefined && (

                  <div className="overrideInfo teacherOverride">

                    <strong>

                      Teacher override:

                    </strong>{" "}

                    {score.teacher_override}

                    /

                    {score.maximum_mark}


                    {score.teacher_override_reason && (

                      <>

                        {" — "}

                        {
                          score.teacher_override_reason
                        }

                      </>

                    )}

                  </div>

                )}


                {/* =======================================
                    ADMIN OVERRIDE
                ======================================= */}

                {score.admin_override !==
                  null &&
                  score.admin_override !==
                  undefined && (

                  <div className="overrideInfo adminOverride">

                    <strong>

                      Admin override:

                    </strong>{" "}

                    {score.admin_override}

                    /

                    {score.maximum_mark}


                    {score.admin_override_reason && (

                      <>

                        {" — "}

                        {
                          score.admin_override_reason
                        }

                      </>

                    )}

                  </div>

                )}


              </div>


              {/* =================================================
                  ACTIONS
              ================================================= */}

              <div className="scoreActions">


                <strong className="finalMark">

                  {finalMark}

                  /

                  {score.maximum_mark}

                </strong>


                {canOverride &&
                  editing !== score.id && (

                  <button

                    className="primary mini"

                    onClick={() =>
                      startOverride(
                        score
                      )
                    }

                  >

                    Override Mark

                  </button>

                )}

              </div>


              {/* =================================================
                  OVERRIDE FORM
              ================================================= */}

              {editing === score.id && (

                <div className="overrideBox">


                  <div className="overrideTitle">

                    Override Question{" "}

                    {score.question_number}

                  </div>


                  <div className="overrideGrid">


                    <label>

                      New mark

                      <input

                        type="number"

                        min="0"

                        max={
                          score.maximum_mark
                        }

                        step="0.5"

                        value={mark}

                        onChange={
                          event =>
                            setMark(
                              event.target.value
                            )
                        }

                      />

                    </label>


                    <label>

                      Reason for override

                      <textarea

                        rows="3"

                        placeholder=
                          "Explain why the mark was changed..."

                        value={reason}

                        onChange={
                          event =>
                            setReason(
                              event.target.value
                            )
                        }

                      />

                    </label>

                  </div>


                  <div className="overrideButtons">


                    <button

                      className="secondary"

                      onClick={
                        cancelOverride
                      }

                      disabled={saving}

                    >

                      Cancel

                    </button>


                    <button

                      className="primary"

                      onClick={() =>
                        saveOverride(
                          score
                        )
                      }

                      disabled={saving}

                    >

                      {saving
                        ? "Saving…"
                        : "Save Override"}

                    </button>

                  </div>

                </div>

              )}

            </div>

          );

        }

      )}

    </div>

  );
}


/* =========================================================
   RENDER
========================================================= */

createRoot(
  document.getElementById("root")
).render(
  <App />
);