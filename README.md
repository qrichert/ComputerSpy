# Computer Spy

Computer Spy takes screenshots at a given interval and logs start and
close of app.

You can set it to save log data to a local directory or to a remote
directory (via HTTP) or both.

Configuration is done in `config.yaml`.

## Files

- `main.py` Main program, runs locally.
- `config.yaml` Configuration file (local)
- `dry_run.sh` Sets up the environment and ensures the program has all
  necessary authorizations (run it once, the first time).
- `run.sh` Runs the program in the background, spy mode.
- `cs.php` Server-side, data reception script (if configured). Data will
  be saved to `log/` in the same directory as the script.
