import json
import os

def split_prompts(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    prompts = data.get('prompts', [])
    metadata = data.get('metadata', {})

    categories = ['reasoning', 'logical', 'classification', 'qna']
    
    for category in categories:
        filtered_prompts = [p for p in prompts if p['category'] == category]
        
        output_data = {
            "metadata": {
                "category": category,
                "total_prompts": len(filtered_prompts),
                "parent_project": metadata.get("project", "Resolio")
            },
            "prompts": filtered_prompts
        }
        
        file_name = f"drifted_prompts/{category}_prompts.json"
        
        with open(file_name, 'w') as out_file:
            json.dump(output_data, out_file, indent=2)
        
        print(f"Created {file_name} with {len(filtered_prompts)} prompts.")

if __name__ == "__main__":
    input_filename = 'drifted_prompts.json'
    
    if os.path.exists(input_filename):
        split_prompts(input_filename)
    else:
        print(f"Error: {input_filename} not found.")