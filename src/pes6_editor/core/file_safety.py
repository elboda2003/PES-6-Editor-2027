"""Non-destructive file-copy helpers.

These functions only read source files and create separate, exclusive
destination files. They never write to or replace the source.
"""

import os
import stat
import uuid

COPY_CHUNK_SIZE = 1024 * 1024


def _copy_to_new_path(source_path, destination_path):
    """Copy a regular file to a new path, refusing to overwrite anything."""
    source_path = os.path.abspath(source_path)
    destination_path = os.path.abspath(destination_path)

    source_stat = os.stat(source_path, follow_symlinks=False)
    if not stat.S_ISREG(source_stat.st_mode):
        raise ValueError("Source must be a regular file.")

    destination_directory = os.path.dirname(destination_path)
    if not destination_directory:
        raise ValueError("Destination must include a directory.")

    os.makedirs(destination_directory, exist_ok=True)
    created_destination = False

    try:
        with open(source_path, "rb") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise ValueError("Opened source is not a regular file.")

            # Exclusive create guarantees this operation cannot overwrite a file.
            with open(destination_path, "xb") as destination:
                created_destination = True
                while True:
                    chunk = source.read(COPY_CHUNK_SIZE)
                    if not chunk:
                        break
                    destination.write(chunk)
    except Exception:
        # Only clean up a partial destination created by this call.
        if created_destination:
            try:
                os.remove(destination_path)
            except OSError:
                pass
        raise

    return destination_path


def _unique_destination(directory, filename, purpose):
    """Return a destination path with a random suffix."""
    token = uuid.uuid4().hex
    return os.path.join(
        os.path.abspath(directory),
        "{}.{}.{}".format(filename, purpose, token),
    )


def create_backup(source_path, backup_directory):
    """Create a new backup file without changing the source."""
    filename = os.path.basename(os.path.abspath(source_path))
    destination = _unique_destination(backup_directory, filename, "backup")
    return _copy_to_new_path(source_path, destination)


def create_working_copy(source_path, workspace_directory):
    """Create a separate work copy; never edit the original."""
    filename = os.path.basename(os.path.abspath(source_path))
    destination = _unique_destination(workspace_directory, filename, "work")
    return _copy_to_new_path(source_path, destination)


def restore_to_new_file(backup_path, output_directory):
    """Copy a backup to a new output file, without replacing the original."""
    filename = os.path.basename(os.path.abspath(backup_path))
    destination = _unique_destination(output_directory, filename, "restored")
    return _copy_to_new_path(backup_path, destination)
