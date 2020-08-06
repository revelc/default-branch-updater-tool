# Default Branch Updater Tool

A basic tool to update your GitHub default branch to a different one, using
pygithub.

This tool requires your branch to exist already. If you already have a clone,
you can do something like the following to create it:

```bash
# to create 'main' from 'master', if your remote is named 'origin'
git remote update origin && git push origin origin/master:refs/heads/main
```

Other useful commands:
```bash
# To update your local branch's HEAD ref for the origin remote
git remote set-head origin -a
```
