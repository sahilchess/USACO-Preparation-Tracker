# USACO Preparation Tracker

A lightweight command-line tracker for logging USACO (and Codeforces) practice problems, then reviewing progress over time.

## Features

- Log solved problems with:
  - name
  - difficulty (`bronze`, `silver`, `gold`)
  - source (`usaco`, `codeforces`)
  - topic (with fallback to `other`)
  - time spent (minutes)
  - whether you looked up the solution
  - date solved
- View summary stats:
  - total solved
  - difficulty breakdown
  - looked-up rate
  - average solve time
  - weak-topic ranking by help rate
- List all logged problems, optionally filtered by topic

## Requirements

- Python 3.8+ (no external dependencies)

## Run

From the repository root:

```bash
python main.py
```

## Data Storage

The app stores progress in a local file:

- `usaco_data.json`

If the file does not exist, it is created automatically after the first logged problem.

## Menu

When you run the program, you can:

1. log a problem
2. view stats
3. list problems
4. exit