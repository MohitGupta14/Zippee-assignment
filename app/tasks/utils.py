def validate_task_data(data):
    errors = []
    if not data.get('title'):
        errors.append('Title is required')
    if len(data.get('title', '')) > 200:
        errors.append('Title must be less than 200 characters')
    return errors
