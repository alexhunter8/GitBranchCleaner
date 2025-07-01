# GitBranchCleaner

Small CLI to list, filter, and clean stale local git branches with safety checks.

## Usage

- List stale >180 days (dry run):
  
  
  python3 src/gbclean.py --days 180 --dry-run

- Delete merged only (confirm):
  
  
  python3 src/gbclean.py --days 120 --delete-merged


## Notes
- Uses local git; no network needed.
- If parsing ISO dates fails, they are skipped.
