import sys

from lessons import evening_lesson, midday_lesson, morning_lesson
from telegram_client import send_message


LESSONS = {
    "morning": morning_lesson,
    "midday": midday_lesson,
    "evening": evening_lesson,
}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in LESSONS:
        print("Usage: python send_lesson.py [morning|midday|evening]")
        sys.exit(1)

    lesson_type = sys.argv[1]
    send_message(LESSONS[lesson_type]())
    print(f"Sent {lesson_type} lesson.")


if __name__ == "__main__":
    main()
