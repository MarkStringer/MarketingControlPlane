# Local agents

All agents run locally via cron — no GitHub Actions, no remote scheduler.

## Schedule

| Agent | Days | Time | Script |
|---|---|---|---|
| content-scout | Mon, Thu | 09:00 | `scripts/run-content-scout.sh` |
| reply-scout | Mon–Fri | 09:00 | `scripts/run-reply-scout.sh` |

On boot: `scripts/boot-catchup.sh` runs after 90 s and starts any agent whose
scheduled slot has passed but hasn't run today.

## API keys

The content-scout Python script needs `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY`
at runtime. Cron does not source `~/.bashrc`, so put them in `~/.env.secrets`:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

`chmod 600 ~/.env.secrets` after creating it.

The reply-scout uses the `claude` CLI directly, which uses its own stored auth.

## State tracking

Each agent writes today's date to `.agent-state/<name>.last-run` after a
successful run. Boot-catchup reads this to decide whether to run.

To force a re-run today: `rm .agent-state/<name>.last-run`

## Logs

Shell-level logs land in `scripts/logs/` (gitignored).
Agent output logs go to `agent-logs/<agent>/` as usual and are committed.

## Changing the schedule

Edit the crontab (`crontab -e`) and the matching lines in `scripts/boot-catchup.sh`.
The two must agree on days and times.
