# KB-07 GitHub sync

On Pro and Team you can connect a project to a GitHub repository (Settings > GitHub > Connect).
Buildbox asks for access to one repository you choose, not your whole account.

- Sync is two-way on the `main` branch. Each AI generation is pushed as a commit. Commits you push
  to `main` on GitHub are pulled into Buildbox within about a minute.
- Other branches are ignored by sync. Work on a branch and merge to `main` when ready.
- If you edit the same file in Buildbox and on GitHub at the same time, Buildbox does not overwrite
  your GitHub commit. It stops syncing, shows **Conflict**, and asks you to pick which version to
  keep.
- Disconnecting keeps the repository and its history on GitHub. Nothing is deleted.
- If sync shows **Unauthorized**, the GitHub app lost access (often after a GitHub organization
  changed its settings). Reconnect from Settings > GitHub.
