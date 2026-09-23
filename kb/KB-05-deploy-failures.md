# KB-05 When a deploy fails

Open **Deploy history**, click the failed deploy and read the last 30 lines of the build log.
Most failures are one of these:

| Log says | What it means | Fix |
|---|---|---|
| `Build exceeded 10 minute limit` | The build took longer than 10 minutes | Remove unused packages, or ask the AI to "reduce build time by removing unused dependencies". Large image assets should be uploaded, not generated at build time |
| `Missing environment variable X` | The app needs a value that is not set for Production | Add it in Settings > Environment (KB-08), then deploy again |
| `Module not found` | A package is imported but not installed | Ask the AI to "add the missing package X", or restore the last working checkpoint |
| `Out of memory` | The build ran out of memory (2 GB limit) | Same as the time limit: fewer or lighter dependencies |

A failed deploy never replaces the live site; the previous deploy keeps running.

If the log shows none of these, or deploys stay in **Queued** for more than 15 minutes, that is on
our side. Contact support with the project name and the deploy id from Deploy history.
