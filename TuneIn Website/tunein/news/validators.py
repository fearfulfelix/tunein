def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.wav', '.mp3', '.mov', '.flac', '.mkv', '.m4v', '.avi', '.m4a', '.aac']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')