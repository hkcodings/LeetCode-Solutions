from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parent.parent

PATTERN_FOLDERS = {
    "01-Arrays-Hashing",
    "02-Strings",
    "03-Two-Pointers-Sliding-Window",
    "04-Binary-Search",
    "05-Stack-Queue",
    "06-Linked-List",
    "07-Trees-BST",
    "08-Heap-Priority-Queue",
    "09-Graphs",
    "10-Recursion-Backtracking",
    "11-Dynamic-Programming",
    "12-Greedy",
    "13-Intervals",
    "14-Bit-Manipulation",
    "15-Math",
    "16-Mixed-OA-Problems",
}

SOLUTION_EXTENSIONS = {
    ".java",
    ".py",
    ".cpp",
    ".c",
    ".js",
    ".ts",
    ".go",
    ".rs",
    ".kt",
    ".cs",
    ".swift",
    ".php",
    ".rb",
}


def clean_problem_title(folder_name: str) -> str:
    """
    Converts:
        1-two-sum          -> Two Sum
        125-valid-palindrome -> Valid Palindrome
        217-contains-duplicate -> Contains Duplicate
    """

    # Remove LeetCode problem number
    name = re.sub(r"^\d+-", "", folder_name)

    # Replace separators with spaces
    name = re.sub(r"[-_]+", " ", name)

    # Normalize whitespace
    name = re.sub(r"\s+", " ", name).strip()

    # Title case
    return name.title()


def find_solution_file(problem_dir: Path):
    solutions = [
        file
        for file in problem_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in SOLUTION_EXTENSIONS
    ]

    if len(solutions) == 1:
        return solutions[0]

    if len(solutions) == 0:
        print(f"⚠️  No solution file found: {problem_dir}")
        return None

    print(f"⚠️  Multiple solution files found: {problem_dir}")
    for solution in solutions:
        print(f"    - {solution.name}")

    return None


def organize_pattern_folder(pattern_dir: Path):
    """
    Flattens:

        pattern/
            1-two-sum/
                README.md
                two-sum.java

    into:

        pattern/
            Two Sum.java
    """

    for problem_dir in sorted(pattern_dir.iterdir()):

        if not problem_dir.is_dir():
            continue

        # Ignore hidden directories
        if problem_dir.name.startswith("."):
            continue

        solution = find_solution_file(problem_dir)

        if solution is None:
            continue

        title = clean_problem_title(problem_dir.name)
        destination = pattern_dir / f"{title}{solution.suffix}"

        # Avoid accidentally overwriting an existing solution
        if destination.exists():
            existing_content = destination.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            new_content = solution.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if existing_content == new_content:
                print(f"✓ Already exists: {destination}")
                shutil.rmtree(problem_dir)
                continue

            print(f"⚠️  Conflict detected: {destination}")
            print(f"    Keeping original problem folder: {problem_dir}")
            continue

        print(f"→ {problem_dir} -> {destination}")

        shutil.move(str(solution), str(destination))

        # Remove README and any remaining LeetSync files
        shutil.rmtree(problem_dir)

        print(f"✓ Organized: {destination}")


def main():
    print("======================================")
    print("     LeetCode Repository Organizer")
    print("======================================")
    print()

    for pattern in sorted(PATTERN_FOLDERS):
        pattern_dir = ROOT / pattern

        if not pattern_dir.exists():
            print(f"⚠️  Missing pattern folder: {pattern}")
            continue

        print(f"\n📁 {pattern}")
        organize_pattern_folder(pattern_dir)

    print("\n======================================")
    print("Organization complete.")
    print("======================================")


if __name__ == "__main__":
    main()
