from os import linesep
import subprocess
import re


def get_diff() -> list[str]:
    print("Building diff list")
    modified_pattern = re.compile("images/(.*?)/.*")
    status = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "HEAD~1"],
        capture_output=True,
        text=True,
    )
    return list(
        {
            modified_pattern.search(line).group(1)
            for line in status.stdout.split(linesep)
            if modified_pattern.match(line)
        }
    )


def write_manifest(diff: list[str]):
    print("Building manifest file")
    with open("./manifest.txt", "w") as file:
        if not diff:
            return
        for folder in diff:
            file.write(f"{folder}\n")

def commit():
    print("Committing manifest file")
    empty_commit_pattern = re.compile("nothing to commit, working tree clean")
    subprocess.run(["git", "add", "."])
    commit_status = subprocess.run(
        ["git", "commit", "-m", "ACTION: Build image manifest"],
        capture_output=True,
        text=True,
    )
    should_push = not any([empty_commit_pattern.match(line) for line in commit_status.stdout.split(linesep)])
    print(f"Needs to push: {should_push}")

    if should_push:
        subprocess.run(["git", "push"])


def main():
    diff = get_diff()
    print(f"Diff is: {diff}")
    write_manifest(diff)
    commit()

if __name__ == "__main__":
    main()
