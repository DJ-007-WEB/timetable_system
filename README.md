# ExamSched

Constraint-based examination scheduling system using conflict-graph construction, DSATUR coloring, capacity-aware room allocation, and Hungarian-based faculty assignment, with Flask + MongoDB persistence and coordinator/faculty workflows.

## Workbook
Required sheets include `Student_Courses`, `Courses`, `Rooms`, and `Teachers`. The exam workbook does **not** contain `teaching_year`, `teaching_years`, or `years_taught`.

Teacher academic-year eligibility is stored in MongoDB in the `teachers.teaching_years` field and is a hard scheduling constraint:

- `FY` -> FY exams
- `SY` -> SY exams
- `TY` -> TY exams
- `BTECH` -> B.Tech exams
- `ALL` -> explicitly allowed across years
- `[]` -> no invigilation until configured

The same MongoDB documents provide the authoritative teacher department used for department compatibility checks.

## Run locally

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Configure `backend/.env` from `backend/.env.example`. Do not commit `.env` or uploaded files.

Existing MongoDB accounts should already have real `password_hash` values. `backend/migrate_users.py` is only for initializing legacy accounts that genuinely lack passwords; it does not migrate teacher-year eligibility.

## Security / reliability fixes

- Student conflict invariant is revalidated after date-adjustment moves.
- Teacher assignment enforces role, academic-year eligibility, department compatibility, collision avoidance and maximum workload.
- Weak teacher-ID/password fallbacks are removed.
- Signup enforces a strong password policy and teacher indexes prevent duplicate identities.
- Cookie-based sessions use CSRF protection on state-changing requests; the frontend obtains the token from `/csrf-token` automatically.
- Upload size/type checks and configurable CORS are enabled.
- Errors returned to clients are generic; details stay in server logs.
- Timetable publication is versioned; previous versions are retained and can be inspected/rolled back instead of being destructively deleted.
- MongoDB lookup indexes, health checks, Docker/Gunicorn support and CI regression tests are included.

## Tests

```bash
cd backend
python -m unittest discover -s tests -p "test_*.py" -v
```

The test suite covers DSATUR, date-adjustment conflicts, room allocation, teacher academic-year rules, MongoDB-sourced teaching years, and API CSRF behavior.

## Docker

```bash
docker build -t examsched .
docker run --env-file backend/.env -p 5000:5000 examsched
```

## Teacher eligibility example

Configure eligibility directly in MongoDB:

```js
{ teacher_id: "T001", teaching_years: ["FY"] }
```

or:

```js
{ teacher_id: "T016", teaching_years: ["SY", "TY", "BTECH"] }
```

No Excel migration or teacher-year column is required.
