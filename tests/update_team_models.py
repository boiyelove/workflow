#!/usr/bin/env python
import os
import re

def update_team_create_statements(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Pattern to match Team.objects.create without teamAuthor
    pattern = r'(self\.team = Team\.objects\.create\(\s*name=[\'"].*?[\'"],\s*url=[\'"].*?[\'"],\s*description=[\'"].*?[\'"])'
    
    # Replace with teamAuthor added
    if 'self.user' in content and not 'self.user1' in content:
        replacement = r'\1,\n            teamAuthor=self.user'
    else:
        replacement = r'\1,\n            teamAuthor=self.user1'
    
    updated_content = re.sub(pattern, replacement, content)
    
    # Handle the case without self.team assignment
    pattern2 = r'(Team\.objects\.create\(\s*name=[\'"].*?[\'"],\s*url=[\'"].*?[\'"],\s*description=[\'"].*?[\'"])'
    if 'self.user' in content and not 'self.user1' in content:
        replacement2 = r'\1,\n            teamAuthor=self.user'
    else:
        replacement2 = r'\1,\n            teamAuthor=self.user1'
    
    updated_content = re.sub(pattern2, replacement2, updated_content)
    
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    return "Updated: " + file_path

# Update all test files
test_files = [
    'test_edge_cases.py',
    'test_forms.py',
    'test_integration.py',
    'test_links.py',
    'test_models.py',
    'test_views.py'
]

for file_name in test_files:
    file_path = os.path.join('tests', file_name)
    if os.path.exists(file_path):
        print(update_team_create_statements(file_path))
    else:
        print(f"File not found: {file_path}")
