#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import frontmatter


def in_out_dirs():
    """
    Get the posts directory and the metadata directory as absolute paths.

    :return: the absolute paths to the posts and metadata directories
    """
    curr_file = Path(__file__).resolve()
    curr_dir = curr_file.parent

    # Posts are present in '../posts'
    posts_dir = curr_dir.parent.joinpath('posts')

    # Metadata must be written in '../dist/metadata'
    metadata_dir = curr_dir.parent.joinpath('dist', 'metadata')
    metadata_dir.mkdir(parents=True, exist_ok=True)

    return posts_dir, metadata_dir


def export_metadata(post_filename, metadata_dir):
    """
    Read YAML front matter from the post and export as a JSON file.

    :param post_filename: the post file to read YAML front matter from
    :param metadata_dir: the directory in which to write the exported metadata
    :return: True if the export succeeds, False otherwise
    """

    print(f'  Generating metadata for file {post_filename}...', end='')

    try:
        metadata = frontmatter.load(post_filename).metadata

        index = metadata['index']
        meta_filename = metadata_dir.joinpath(f'{index:05}.json')

        with open(meta_filename, 'w') as meta_file:
            json.dump(metadata, meta_file, indent=2)

        print('done!')
        return True
    except Exception as e:
        print('failed!')
        print(e)
        return False


def generate_metadata():
    """
    Read all posts from the post directory and export their metadata as JSON
    files in the metadata directory.
    """

    print('Generating metadata...')

    posts_dir, metadata_dir = in_out_dirs()

    outcomes = []
    for post_file in os.listdir(posts_dir):
        post_filename = posts_dir.joinpath(post_file)
        outcomes.append(export_metadata(post_filename, metadata_dir))

    if all(outcomes):
        print('...done!')
    else:
        print('...failed!')
        sys.exit(1)  # Exit with a non-zero exit code


if __name__ == '__main__':
    generate_metadata()
