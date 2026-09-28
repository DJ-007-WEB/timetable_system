import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from app import build_all_teacher_duties_payload, select_best_timetable_doc
except ImportError as exc:
    raise unittest.SkipTest(f"Application dependencies not installed: {exc}")


class DutyExportTests(unittest.TestCase):
    def test_prefers_current_timetable_assignments(self):
        timetable_doc = {
            "timetable": [{"date": "01-Jul-2026"}],
            "teacher_duties": [
                {
                    "teacher_id": "T1",
                    "teacher_name": "Alice",
                    "date": "01-Jul-2026",
                    "slot": "1",
                    "session": "FN",
                    "course_id": "CS101",
                    "role": "Junior",
                    "room_assigned": "R1",
                }
            ],
        }
        teachers = [
            {
                "teacher_id": "T1",
                "name": "Alice",
                "last_role": "Senior",
                "has_served_high_role": False,
                "history": [{"exam_date": "02-Jul-2026", "role_assigned": "Senior"}],
            }
        ]

        duties = build_all_teacher_duties_payload(timetable_doc, teachers)

        self.assertEqual(len(duties), 1)
        self.assertEqual(duties[0]["date"], "01-Jul-2026")
        self.assertEqual(duties[0]["teacher_name"], "Alice")
        self.assertEqual(duties[0]["slot"], "1")

    def test_falls_back_to_history_when_no_current_assignments(self):
        timetable_doc = {"timetable": [{"date": "01-Jul-2026"}]}
        teachers = [
            {
                "teacher_id": "T2",
                "name": "Bob",
                "last_role": "Junior",
                "history": [
                    {
                        "exam_date": "01-Jul-2026",
                        "slot_id": "2",
                        "session": "AN",
                        "course_id": "CS102",
                        "role_assigned": "Junior",
                        "room_assigned": "R2",
                    }
                ],
            }
        ]

        duties = build_all_teacher_duties_payload(timetable_doc, teachers)

        self.assertEqual(len(duties), 1)
        self.assertEqual(duties[0]["teacher_id"], "T2")
        self.assertEqual(duties[0]["slot"], "2")

    def test_selects_doc_with_most_duties_when_multiple_candidates_exist(self):
        candidates = [
            {"_id": 1, "teacher_duties": [{"teacher_id": "T1"}]},
            {
                "_id": 2,
                "teacher_duties": [
                    {"teacher_id": "T1"},
                    {"teacher_id": "T2"},
                    {"teacher_id": "T3"},
                ],
            },
        ]

        selected = select_best_timetable_doc(candidates)

        self.assertEqual(selected["_id"], 2)


if __name__ == "__main__":
    unittest.main()
