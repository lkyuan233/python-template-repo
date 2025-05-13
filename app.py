import argparse
import os
import subprocess
import json
import re
from tempfile import TemporaryDirectory

def run(cmd, cwd=None, env=None, allow_failure=False):
    print(f"> {cmd}")
    try:
        return subprocess.run(
            cmd, shell=True, check=True,
            capture_output=True, text=True,
            cwd=cwd, env=env
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(e.stdout)
        print(e.stderr)
        if not allow_failure:
            raise
        return ""

def parse_pr_url(url):
    match = re.match(r"https://github.com/([^/]+)/([^/]+)/pull/(\d+)", url)
    if not match:
        raise ValueError("Invalid GitHub PR URL")
    return match.groups()  # user, repo, pr_number

def get_pr_metadata(repo_dir, pr_number):
    head = run(f"gh pr view {pr_number} --json headRefName --jq .headRefName", cwd=repo_dir)
    base = run(f"gh pr view {pr_number} --json baseRefName --jq .baseRefName", cwd=repo_dir)
    return head.strip(), base.strip()

def get_merge_base(repo_dir, base, head):
    return run(f"git merge-base origin/{base} origin/{head}", cwd=repo_dir)

def checkout(repo_dir, ref):
    run(f"git checkout {ref}", cwd=repo_dir)
    
def run_coverage(repo_dir, output_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = repo_dir

    # Run pytest with coverage
    run("coverage erase", cwd=repo_dir, env=env, allow_failure=True)
    run("coverage run -m pytest", cwd=repo_dir, env=env, allow_failure=True)

    # Check if .coverage file exists before converting to JSON
    coverage_data_path = os.path.join(repo_dir, ".coverage")
    json_output_path = os.path.join(repo_dir, output_path)

    if os.path.exists(coverage_data_path):
        try:
            run(f"coverage json -o {output_path}", cwd=repo_dir, env=env)
        except subprocess.CalledProcessError:
            print("⚠️ Failed to generate coverage JSON — coverage data likely empty.")
            with open(json_output_path, "w") as f:
                json.dump({"files": {}}, f)
    else:
        print("⚠️ No .coverage data found. Writing empty coverage JSON.")
        with open(json_output_path, "w") as f:
            json.dump({"files": {}}, f)

def get_diff_lines(repo_dir, base, head):
    diff = run(f"git diff -U0 {base} {head}", cwd=repo_dir)
    return parse_diff(diff)

def parse_diff(diff_text):
    from collections import defaultdict
    modified = defaultdict(set)
    current_file = None
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            if match:
                start = int(match.group(1))
                count = int(match.group(2) or 1)
                for i in range(start, start + count):
                    modified[current_file].add(i)
    return modified

def load_coverage(path):
    with open(path) as f:
        return json.load(f)["files"]

def compare_line_coverage(modified, base_cov, pr_cov):
    print("\n📄 Modified Line Coverage Changes:")
    for file, lines in modified.items():
        base_exec = set(base_cov.get(file, {}).get("executed_lines", []))
        pr_exec = set(pr_cov.get(file, {}).get("executed_lines", []))
        for line in sorted(lines):
            b = "✅" if line in base_exec else "❌"
            p = "✅" if line in pr_exec else "❌"
            if b != p:
                print(f"{file}: Line {line}: {b} → {p}")

def coverage_summary(cov_data):
    if not cov_data:
        return 0, 0
    total = covered = 0
    for file_data in cov_data.values():
        statements = file_data.get("executed_lines", []) + file_data.get("missing_lines", [])
        total += len(statements)
        covered += len(file_data.get("executed_lines", []))
    return covered, total
    
def compare_overall_coverage(base_cov, pr_cov):
    def percentage(c, t):
        return (c / t * 100) if t else 0

    b_cov, b_total = coverage_summary(base_cov)
    p_cov, p_total = coverage_summary(pr_cov)

    b_pct = percentage(b_cov, b_total)
    p_pct = percentage(p_cov, p_total)
    delta = p_pct - b_pct

    print("\n📊 Overall Coverage Summary:")
    print(f"   🔹 Covered lines: {b_cov}/{b_total} ({b_pct:.2f}%) → {p_cov}/{p_total} ({p_pct:.2f}%)")
    print(f"   🔺 Change: {delta:+.2f}%")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="GitHub PR URL")
    args = parser.parse_args()

    user, repo, pr_number = parse_pr_url(args.url)
    repo_url = f"https://github.com/{user}/{repo}.git"

    with TemporaryDirectory() as tmp:
        repo_dir = os.path.join(tmp, repo)

        print(f"\n📦 Cloning {repo_url}...")
        run(f"git clone {repo_url}", cwd=tmp)
        run("gh auth status", cwd=repo_dir)  # sanity check

        run("git fetch origin", cwd=repo_dir)
        head, base = get_pr_metadata(repo_dir, pr_number)
        merge_base = get_merge_base(repo_dir, base, head)

        print(f"\n🔁 Merge base: {merge_base}")
        print(f"🔀 Head: origin/{head}")
        print(f"🌱 Base: origin/{base}")

        # 1. Merge base coverage
        checkout(repo_dir, merge_base)
        run_coverage(repo_dir, "coverage-base.json")
        base_cov = load_coverage(os.path.join(repo_dir, "coverage-base.json"))

        # 2. PR head coverage
        checkout(repo_dir, f"origin/{head}")
        run_coverage(repo_dir, "coverage-pr.json")
        pr_cov = load_coverage(os.path.join(repo_dir, "coverage-pr.json"))

        # 3. Compare
        modified = get_diff_lines(repo_dir, merge_base, f"origin/{head}")
        compare_line_coverage(modified, base_cov, pr_cov)
        compare_overall_coverage(base_cov, pr_cov)

if __name__ == "__main__":
    main()
