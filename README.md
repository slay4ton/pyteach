# PyTeach — Interactive Python Learning Script

An interactive CLI-based tool to teach beginners Python fundamentals through hands-on lessons, exercises, quizzes, and instant feedback.

## Features

- 📚 **7-lesson curriculum** covering Python basics
- ✍️ **Interactive code snippets** — edit and run Python code in real-time
- 🧪 **Auto-graded exercises** — unit-test based validation with instant feedback
- 📋 **Quizzes** — test your knowledge after each lesson
- 💾 **Progress tracking** — resume where you left off
- 🎯 **Hints & solutions** — reveal on-demand
- 🔒 **Safe execution** — student code runs in isolated subprocesses

## Quick Start

### Installation

```bash
git clone https://github.com/slay4ton/pyteach.git
cd pyteach
pip install -e .
```

### Run

```bash
pyteach
```

## Curriculum

1. **Intro** — Install Python, run your first script
2. **Variables & Types** — int, float, str, bool
3. **Operators** — arithmetic, comparison, logical
4. **Conditionals** — if/elif/else
5. **Loops** — for, while
6. **Functions** — def, parameters, return
7. **Collections** — lists, tuples, dicts

## Project Structure

```
pyteach/
├── pyteach/
│   ├── __main__.py
│   ├── cli.py
│   ├── lessons/
│   ├── exercises/
│   ├── engine/
│   └── utils/
├── tests/
├── pyproject.toml
└── README.md
```

## Development

```bash
pytest
```

## License

MIT
