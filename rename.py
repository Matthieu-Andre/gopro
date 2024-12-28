import os
import argparse
import exiftool
from tqdm import tqdm


def rename_files(directory, prefix):
    files = os.listdir(directory)

    for file in tqdm(files):
        if file.startswith(prefix):
            file_path = os.path.join(directory, file)
            file_dir = os.path.dirname(file_path)
            with exiftool.ExifToolHelper() as et:
                metadata = et.get_metadata(file_path)
                created_datetime = metadata[0]["EXIF:CreateDate"]
                date, time = created_datetime.split(" ")
                time = time.replace(":", "")
                date = date.replace(":", "")
                datetime = date + "_" + time
                new_file_name = f"{datetime}_{file}"
                new_file_path = os.path.join(file_dir, new_file_name)
                os.rename(file_path, new_file_path)


def main():
    argparser = argparse.ArgumentParser(description="Rename files in a directory")
    argparser.add_argument(
        "--directory", help="Directory containing files to rename", default="./footage"
    )
    argparser.add_argument("--prefix", help="Prefix to add to the files", default="GO")

    args = argparser.parse_args()

    rename_files(args.directory, args.prefix)


if __name__ == "__main__":
    main()
