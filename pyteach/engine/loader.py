"""Lesson content loader."""

import yaml
from pathlib import Path
from typing import Dict, List, Any


class LessonLoader:
    """Load lessons from YAML files."""

    def __init__(self, lessons_dir: Path = None):
        """Initialize loader.

        Args:
            lessons_dir: Directory containing lesson YAML files
        """
        if lessons_dir is None:
            lessons_dir = Path(__file__).parent.parent / "lessons"
        self.lessons_dir = lessons_dir

    def load_lesson(self, lesson_id: str) -> Dict[str, Any]:
        """Load a lesson by ID.

        Args:
            lesson_id: Lesson identifier (e.g., '01_intro')

        Returns:
            Dictionary with lesson content

        Raises:
            FileNotFoundError: If lesson not found
        """
        lesson_file = self.lessons_dir / f"{lesson_id}.yaml"
        if not lesson_file.exists():
            raise FileNotFoundError(f"Lesson {lesson_id} not found at {lesson_file}")

        with open(lesson_file, "r") as f:
            return yaml.safe_load(f)

    def list_lessons(self) -> List[str]:
        """List all available lessons (sorted).

        Returns:
            List of lesson IDs
        """
        yaml_files = sorted(self.lessons_dir.glob("*.yaml"))
        return [f.stem for f in yaml_files]
