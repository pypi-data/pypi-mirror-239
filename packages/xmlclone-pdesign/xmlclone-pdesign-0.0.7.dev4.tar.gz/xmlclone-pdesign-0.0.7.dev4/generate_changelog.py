import subprocess
import sys


if len(sys.argv) < 2:
    raise Exception("Provide a version number.")

version = sys.argv[1]

cmd = [
    "github_changelog_generator",
    "-u",
    "xmlclone",
    "-p",
    "pdemo",
    "--exclude-labels",
    "duplicate,question,invalid,wontfix,cantfix,stale,no-changelog",
    "--future-release",
    version,
]

print(f"Running command: {' '.join(cmd)}\n")
subprocess.run(cmd)
