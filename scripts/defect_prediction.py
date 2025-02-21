import os
import random
import subprocess
from collections import defaultdict
from git import Repo

# --- Approach 1: Predicting Faults from Cached History (BugCache/FixCache) ---

def clone_repository(repo_url, local_path):
    """
    Clone a GitHub repository to a local directory.
    If the repository exists, simply use it.
    """
    if not os.path.exists(local_path):
        print(f"Cloning repository from {repo_url}...")
        Repo.clone_from(repo_url, local_path)
    else:
        print(f"Repository already exists at {local_path}.")

def extract_file_change_history(repo_path):
    """
    Extract commit history and count how many times each file was changed.
    Uses the BugCache/FixCache algorithm to predict defect-prone files.
    """
    file_change_count = defaultdict(int)
    repo = Repo(os.path.abspath(repo_path))

    # Iterate through all commits in all branches
    for commit in repo.iter_commits('--all'):
        changed_files = commit.stats.files.keys()
        for file in changed_files:
            file_change_count[file] += 1

    return file_change_count

def calculate_bug_scores(file_change_count):
    """
    Calculate defect likelihood scores for each file.
    The score is normalized by the total number of changes.
    """
    total_changes = sum(file_change_count.values())
    bug_scores = {}

    if total_changes == 0:
        return bug_scores  # Avoid division by zero

    for file, changes in file_change_count.items():
        bug_scores[file] = changes / total_changes

    return bug_scores

def generate_report(bug_scores, top_n=10):
    """
    Generate a report of the top N files most likely to contain defects.
    This report can be used for test prioritization or code review focus.
    """
    sorted_files = sorted(bug_scores.items(), key=lambda x: x[1], reverse=True)
    print(f"Top {top_n} files most likely to contain defects:")
    for i, (file, score) in enumerate(sorted_files[:top_n], 1):
        print(f"{i}. {file} (Score: {score:.4f})")

# --- Approach 2: REPD Model for Defect Prediction ---

def repd_defect_prediction(repo_path):
    """
    Simulated implementation of the Reconstruction Error Probability Distribution (REPD) model.
    In a real scenario, this function would load a trained model (or train one using historical
    datasets such as those from NASA ESDS Data Metrics) and apply it to extract features from the source code.
    
    Here, we simulate predictions by assigning a random defect score to each file.
    """
    repd_scores = {}
    repo = Repo(os.path.abspath(repo_path))
    
    # Gather list of files in the repository by scanning the file tree
    repo_files = []
    for root, _, files in os.walk(repo.working_tree_dir):
        for file in files:
            # Optionally filter out non-code files (e.g., images, binaries)
            if file.endswith(('.py', '.c', '.cpp', '.h', '.java', '.js', '.go')):
                repo_files.append(os.path.relpath(os.path.join(root, file), repo.working_tree_dir))
    
    # Simulate a prediction: assign a random score between 0 and 1 to each file
    for file in repo_files:
        repd_scores[file] = random.random()
    
    # Normalize scores to sum to 1 (optional)
    total_score = sum(repd_scores.values())
    if total_score > 0:
        repd_scores = {file: score / total_score for file, score in repd_scores.items()}
    
    return repd_scores

# --- New Function: Static Code Analysis for Multi-Language Support ---

def run_static_analysis(repo_path):
    """
    Run static code analysis on the repository to identify bugs/defects.
    This example supports Java, C++, and C using appropriate tools.
    """
    print("\n=== Running Static Code Analysis to Identify Bugs/Defects ===")
    repo = Repo(os.path.abspath(repo_path))
    working_dir = repo.working_tree_dir

    # Define static analysis tools for each language
    tools = {
        "java": "spotbugs",  # Use SpotBugs for Java
        "cpp": "cppcheck",   # Use cppcheck for C++
        "c": "cppcheck",     # Use cppcheck for C
    }

    # Scan the repository for files and run appropriate tools
    for root, _, files in os.walk(working_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".java") and not file.endswith("module-info.java"):  # Skip module-info.java
                print(f"Running SpotBugs on {file_path}...")
                try:
                    result = subprocess.run(
                        ["spotbugs", file_path],
                        capture_output=True,
                        text=True,
                        check=False,  # Do not raise an exception if the command fails
                    )
                    if result.returncode != 0:
                        print(f"SpotBugs failed for {file_path}: {result.stderr}")
                    elif result.stdout:
                        print(result.stdout)
                except Exception as e:
                    print(f"Error running SpotBugs on {file_path}: {e}")
            elif file.endswith((".cpp", ".h")):
                print(f"Running cppcheck on {file_path}...")
                try:
                    result = subprocess.run(
                        ["cppcheck", file_path],
                        capture_output=True,
                        text=True,
                        check=False,  # Do not raise an exception if the command fails
                    )
                    if result.returncode != 0:
                        print(f"cppcheck failed for {file_path}: {result.stderr}")
                    elif result.stdout:
                        print(result.stdout)
                except Exception as e:
                    print(f"Error running cppcheck on {file_path}: {e}")
            elif file.endswith(".c"):
                print(f"Running cppcheck on {file_path}...")
                try:
                    result = subprocess.run(
                        ["cppcheck", file_path],
                        capture_output=True,
                        text=True,
                        check=False,  # Do not raise an exception if the command fails
                    )
                    if result.returncode != 0:
                        print(f"cppcheck failed for {file_path}: {result.stderr}")
                    elif result.stdout:
                        print(result.stdout)
                except Exception as e:
                    print(f"Error running cppcheck on {file_path}: {e}")
            else:
                continue  # Skip non-code files

# --- Main Analysis Function integrating both approaches --- 

def main():
    # Configuration: update these values as needed or pass via environment variables/CI/CD
    repo_url = "https://github.com/eclipse-openj9/openj9"  # Example repository; can be parameterized.
    local_path = "./openj9_repo"  # Local clone directory

    # Step 1: Clone the repository
    clone_repository(repo_url, local_path)

    # --- Approach 1 Execution ---
    print("\n=== Running BugCache/FixCache defect prediction (Approach 1) ===")
    file_change_count = extract_file_change_history(local_path)
    bug_scores = calculate_bug_scores(file_change_count)
    generate_report(bug_scores)

    # --- Approach 2 Execution ---
    print("\n=== Running REPD defect prediction (Approach 2) ===")
    print("Running REPD defect prediction model...")
    repd_scores = repd_defect_prediction(local_path)
    if repd_scores:
        generate_report(repd_scores)
    else:
        print("REPD model not implemented yet.")

    # --- New Function Execution ---
    run_static_analysis(local_path)

    # Future integration:
    # - Compare results between the two approaches.
    # - Integrate with a CI/CD pipeline (e.g., GitHub Actions, Jenkins) to run this analysis on new tags or pull requests.
    # - Optionally, store results in a database (MongoDB, PostgreSQL, etc.) for historical analysis.
    
if __name__ == "__main__":
    main()
  