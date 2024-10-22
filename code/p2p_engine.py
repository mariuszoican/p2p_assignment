import os
import zipfile
import pandas as pd
import random
from collections import defaultdict
from hydra import compose, initialize
from omegaconf import OmegaConf

def assign_reviews_and_create_zips(
    num_students,
    reviews_per_student,
    reviews_per_paper,
    folder_path,
    output_zip_folder
):
    os.makedirs(output_zip_folder, exist_ok=True)

    # Initialize assignments: each student reviews 'reviews_per_student' papers
    reviews = {student: [] for student in range(num_students)}
    papers_reviewed_by = {paper: [] for paper in range(num_students)}

    # Step 1: Create a round-robin assignment
    student_list = list(range(num_students))
    paper_list = list(range(num_students))

    shift = 1  # Start with a shift to avoid self-review on the first assignment

    while True:
        # Reset assignments for this round
        valid_assignment = True

        for i, student in enumerate(student_list):
            paper = paper_list[(i + shift) % num_students]
            if paper == student:  # Ensure no self-review
                valid_assignment = False
                break
            reviews[student].append(paper)
            papers_reviewed_by[paper].append(student)

        # Check if we managed a valid assignment
        if valid_assignment and all(len(revs) == reviews_per_student for revs in reviews.values()):
            break  # Valid balanced assignment found

        # Otherwise, increase shift and try again
        shift += 1

    # Step 2: Verify all papers are reviewed exactly the required times
    assert all(len(evals) == reviews_per_paper for evals in papers_reviewed_by.values()), \
        "Each paper must be reviewed exactly 6 times."

    # Convert the assignments to a DataFrame for better visualization
    assignments = [(student, paper) for student, papers in reviews.items() for paper in papers]
    df = pd.DataFrame(assignments, columns=['Student', 'Reviewed_Paper'])

    # Save the DataFrame to Excel
    df.to_excel("peer_review_assignments.xlsx", index=False)

    # Create zip files for each student's assignments
    for student, papers in reviews.items():
        zip_file_path = os.path.join(output_zip_folder, f"Student_{student}_reviews.zip")
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for paper in papers:
                paper_filename = f"{paper}.txt"
                paper_path = os.path.join(folder_path, paper_filename)
                if os.path.exists(paper_path):
                    zipf.write(paper_path, arcname=paper_filename)

    return df, output_zip_folder

if __name__ == "__main__":
    with initialize(version_base=None, config_path="../conf"):
        cfg = compose(config_name="config")
    # Run the function to assign reviews and create zip files
    df, zip_folder = assign_reviews_and_create_zips(cfg.num_students,
                        cfg.reviews_per_student,
                        cfg.reviews_per_paper,
                        cfg.folder_submissions,
                        cfg.folder_assignments)
    df, zip_folder
