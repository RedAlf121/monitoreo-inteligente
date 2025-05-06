def file_content_validate(file, file_path):
    import os
    from services.file_comparator import compare_files

    if os.path.exists(file_path):
        with open(file_path, "rb") as existing_file:
            file_comparison = compare_files(existing_file.read(), file.file.read())
            if not file_comparison.is_correct():
                return False, file_comparison.show_status_error()
    return True, "Correct"