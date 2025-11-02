import re

# Map class names to IDs
class_map = {
    'bird': 0,
    'drone': 1,
    'balloon': 2,
    'kite': 3
}

files = ['test_priority_agent.py', 'test_action_agent.py', 'test_complete_workflow.py']

for filename in files:
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find all Detection( patterns and add class_id
    def replace_detection(match):
        full_match = match.group(0)
        class_name_match = re.search(r'class_name="(\w+)"', full_match)
        if class_name_match:
            class_name = class_name_match.group(1)
            class_id = class_map.get(class_name, 0)
            # Insert class_id after class_name
            new_content = full_match.replace(
                f'class_name="{class_name}",',
                f'class_name="{class_name}",\n        class_id={class_id},'
            )
            return new_content
        return full_match
    
    # Pattern to match Detection objects
    pattern = r'Detection\([^)]+\)'
    content = re.sub(pattern, replace_detection, content)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f'Fixed {filename}')

print('All test files fixed!')
