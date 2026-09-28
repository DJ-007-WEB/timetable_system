# ExamSched

Constraint-based examination scheduler using conflict graphs, DSATUR coloring, capacity-aware room allocation, and Hungarian faculty assignment.

## Required workbook
`Student_Courses`, `Courses`, `Rooms`, `Teachers`. The `Teachers` sheet must include `teaching_year` with FY, SY, TY or B.Tech. This is a hard invigilation constraint: teachers are only assigned to exams for the year group they teach. `ALL` is allowed only for explicitly general/cross-year staff.

## Run
`cd backend && pip install -r requirements.txt && python app.py`

Set variables from `backend/.env.example`. Existing accounts without passwords must be initialized with `MIGRATION_DEFAULT_PASSWORD` using `python migrate_users.py`.

## Tests
`cd backend && python -m unittest discover -s tests -p "test_*.py" -v`

## Docker
`docker build -t examsched .` then `docker run --env-file backend/.env -p 5000:5000 examsched`.

## Engineering fixes
- Safe date-adjustment invariant and regression tests.
- FY/SY/TY/B.Tech teacher eligibility as a hard constraint.
- Department compatibility as a hard constraint.
- Teacher collision uses date+slot.
- Capacity-aware room allocation.
- Versioned timetable publication with rollback; clear archives instead of deleting history.
- Server-side sessions and coordinator authorization for administrative operations.
- Stronger password policy, no teacher-ID-derived login fallback, protected uploads, size limits and configurable CORS.
- MongoDB indexes, Docker/Gunicorn and CI.
- Frontend inline JS moved to `frontend/app.js`.

## Teacher eligibility (MongoDB is authoritative)

The exam workbook does **not** contain `teaching_year`. The `Teachers` sheet remains `teacher_id, name, role` (plus any existing non-eligibility columns). A teacher's `teaching_years` field is stored in MongoDB and is a hard scheduling constraint:

- `FY` → FY exams only
- `SY` → SY exams only
- `TY` → TY exams only
- `BTECH` → B.Tech exams only
- `ALL` → explicitly permitted for all years

A teacher with an empty `teaching_years` list is not assigned an invigilation duty until configured.

### Teacher configuration

Teacher eligibility is stored directly in MongoDB. No teacher-year migration script is required. Configure each teacher's `teaching_years` field directly in the `teachers` collection, for example:

```js
teaching_years: ["SY", "TY", "BTECH"]
```

or:

```js
teaching_years: ["FY"]
```

The scheduler reads this field directly from MongoDB. The exam workbook remains unchanged and does not contain teaching-year eligibility. A teacher with an empty `teaching_years` list is not assigned an invigilation duty until configured.

### CSRF protection

Authenticated state-changing requests require an `X-CSRF-Token` header. The frontend obtains the token from `/csrf-token` automatically. This protects cookie-based sessions from cross-site request forgery.
