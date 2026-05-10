"""Progress tracking and persistence."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class ProgressTracker:
    """Track and persist user progress."""

    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize tracker.

        Args:
            data_dir: Directory to store progress data (defaults to ~/.pyteach)
        """
        if data_dir is None:
            data_dir = Path.home() / ".pyteach"
        self.data_dir = data_dir
        self.progress_file = data_dir / "progress.json"
        self.data_dir.mkdir(exist_ok=True, parents=True)
        self._load()

    def _load(self):
        """Load progress from disk."""
        if self.progress_file.exists():
            with open(self.progress_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"completed_lessons": [], "quiz_scores": {}, "last_lesson": None}

    def _save(self):
        """Save progress to disk."""
        with open(self.progress_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def mark_lesson_complete(self, lesson_id: str):
        """Mark a lesson as complete."""
        if lesson_id not in self.data["completed_lessons"]:
            self.data["completed_lessons"].append(lesson_id)
        self.data["last_lesson"] = lesson_id
        self._save()

    def is_complete(self, lesson_id: str) -> bool:
        """Check if a lesson is complete."""
        return lesson_id in self.data["completed_lessons"]

    def get_completed_lessons(self) -> List[str]:
        """Get list of completed lessons."""
        return self.data["completed_lessons"]

    def get_last_lesson(self) -> Optional[str]:
        """Get the last lesson worked on."""
        return self.data.get("last_lesson")

    def record_quiz_score(self, lesson_id: str, score: int):
        """Record a quiz score."""
        self.data["quiz_scores"][lesson_id] = score
        self._save()

    def get_quiz_scores(self) -> Dict[str, int]:
        """Get all quiz scores."""
        return self.data.get("quiz_scores", {})

    def reset(self):
        """Reset all progress."""
        self.data = {"completed_lessons": [], "quiz_scores": {}, "last_lesson": None}
        self._save()
