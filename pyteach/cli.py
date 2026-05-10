"""PyTeach CLI application using Typer."""

import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from pyteach.engine.loader import LessonLoader
from pyteach.engine.persistence import ProgressTracker
from pyteach.utils.formatting import print_header, print_success, print_error, print_info

app = typer.Typer(help="PyTeach: Learn Python interactively", no_args_is_help=True)
console = Console()


@app.command()
def start(
    lesson: Optional[str] = typer.Option(None, "--lesson", "-l", help="Start a specific lesson"),
    resume: bool = typer.Option(False, "--resume", "-r", help="Resume from last lesson"),
):
    """Start an interactive lesson."""
    print_header("Welcome to PyTeach!")

    progress = ProgressTracker()
    loader = LessonLoader()

    if resume:
        lesson_id = progress.get_last_lesson()
        if not lesson_id:
            print_info("No previous progress found. Starting with lesson 01_intro.")
            lesson_id = "01_intro"
    elif lesson:
        lesson_id = lesson
    else:
        _show_lesson_menu(loader, progress)
        return

    try:
        lesson_data = loader.load_lesson(lesson_id)
        print_success(f"\n📚 Loaded: {lesson_data['title']}\n")
        print(lesson_data["content"])

        for ex_idx, exercise in enumerate(lesson_data.get("exercises", []), 1):
            print_header(f"Exercise {ex_idx}: {exercise['prompt']}")
            print(exercise["template"])
            print_info("[Interactive execution in full implementation]")

        if lesson_data.get("quiz"):
            _run_quiz(lesson_data["quiz"], lesson_id, progress)

        progress.mark_lesson_complete(lesson_id)
        print_success(f"\n✅ Lesson {lesson_id} completed!")

    except FileNotFoundError:
        print_error(f"Lesson '{lesson_id}' not found.")
        sys.exit(1)


@app.command()
def list_lessons():
    """List all available lessons."""
    print_header("Available Lessons")
    loader = LessonLoader()
    progress = ProgressTracker()

    lessons = loader.list_lessons()
    table = Table(title="PyTeach Curriculum")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")

    for lesson_id in lessons:
        try:
            lesson = loader.load_lesson(lesson_id)
            status = "✅ Complete" if progress.is_complete(lesson_id) else "⭕ Not Started"
            table.add_row(lesson_id, lesson["title"], status)
        except Exception:
            pass

    console.print(table)


@app.command()
def progress():
    """Show your learning progress."""
    print_header("Your Progress")
    tracker = ProgressTracker()

    completed = tracker.get_completed_lessons()
    print_info(f"Lessons completed: {len(completed)}")
    if completed:
        print("  " + ", ".join(completed))

    quiz_scores = tracker.get_quiz_scores()
    if quiz_scores:
        print_info("\nQuiz Scores:")
        for lesson_id, score in quiz_scores.items():
            print(f"  {lesson_id}: {score}%")


@app.command()
def reset():
    """Reset all progress."""
    if typer.confirm("Are you sure you want to reset all progress?"):
        tracker = ProgressTracker()
        tracker.reset()
        print_success("✅ Progress reset.")
    else:
        print_info("Cancelled.")


def _show_lesson_menu(loader: LessonLoader, progress: ProgressTracker):
    """Show an interactive lesson selection menu."""
    print_header("Select a Lesson")
    lessons = loader.list_lessons()

    for idx, lesson_id in enumerate(lessons, 1):
        try:
            lesson = loader.load_lesson(lesson_id)
            status = "✅" if progress.is_complete(lesson_id) else "⭕"
            print(f"  {idx}. {status} {lesson_id}: {lesson['title']}")
        except Exception:
            pass

    choice = typer.prompt("Enter lesson number or ID")
    print_info(f"Selected: {choice}")


def _run_quiz(quiz_items, lesson_id: str, progress: ProgressTracker):
    """Run a quiz for a lesson."""
    print_header("📝 Quiz")
    score = 0

    for idx, item in enumerate(quiz_items, 1):
        print(f"\nQuestion {idx}: {item['question']}")
        for opt_idx, option in enumerate(item.get("options", []), 1):
            print(f"  {opt_idx}. {option}")

        answer = typer.prompt("Your answer")
        if answer == item.get("answer"):
            score += 1
            print_success("✅ Correct!")
        else:
            print_error(f"❌ Incorrect. Answer: {item.get('answer')}")

    percentage = (score / len(quiz_items)) * 100
    print_success(f"\nQuiz Score: {percentage:.0f}% ({score}/{len(quiz_items)})")
    progress.record_quiz_score(lesson_id, int(percentage))


if __name__ == "__main__":
    app()
