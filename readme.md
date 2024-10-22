# Peer-to-peer evaluation module 

Code:
1. `generate_submissions.py`: For test purposes only. Generates mock submission files (for each of *N* students) and saves them as `#.txt` in the `submissions` folder.
2. `p2p_engine.py`: Allocates papers to students using a cyclical round-robin assignment, balancing workload and the number of times each paper is reviewed. 
    * Each student gets a zip file with their assigned submissions for review, in the `assignments` folder.
    * The assignment distribution is also saved as an Excel file for easy retrieval.


## Roadmap

1. Make the code work with arbitrary file extensions (or at least `*.pdf` and `*.docx` files)
2. Create function to anonymize submissions and save them in a format compatible to `p2p_engine`.
3. Code to load grades and summarize grades for each student.