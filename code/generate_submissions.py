import os
import random
import string
from hydra import compose, initialize
from omegaconf import OmegaConf

def generate_random_text_files(num_files, folder_path):
    # Ensure the target folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Generate the files with random text content
    for i in range(0, num_files):
        file_path = os.path.join(folder_path, f"{i}.txt")
        random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=100))  # 100 random characters
        with open(file_path, 'w') as f:
            f.write(random_text)

    return folder_path

if __name__ == "__main__":
    with initialize(version_base=None, config_path="../conf"):
        cfg = compose(config_name="config")
    # Run the function to generate 52 text files
    generated_folder = generate_random_text_files(cfg.num_students, cfg.folder_submissions)
