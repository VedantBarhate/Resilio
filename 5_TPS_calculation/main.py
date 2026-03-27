import json
import re
import sys
from pathlib import Path

# Category weights
WEIGHTS = {
    'reasoning': {'FC': 0.30, 'SC': 0.05, 'LC': 0.25, 'RC': 0.30, 'ML': 0.10},
    'logical':   {'FC': 0.25, 'SC': 0.05, 'LC': 0.35, 'RC': 0.25, 'ML': 0.10},
    'qna':       {'FC': 0.45, 'SC': 0.05, 'LC': 0.15, 'RC': 0.20, 'ML': 0.15},
    'classification': {'FC': 0.10, 'SC': 0.50, 'LC': 0.15, 'RC': 0.10, 'ML': 0.15}
}

def get_numerical_priority(key):
    """Helper to sort 'Prompt 2 (qna)' before 'Prompt 10 (classification)'."""
    numbers = re.findall(r'\d+', key)
    return (int(numbers[0]), key) if numbers else (0, key)

def calculate_tps(scores, category):
    """Calculate TPS from factor scores."""
    try:
        weights = WEIGHTS[category]
        tps = (
            weights['FC'] * scores['factual_correctness'] +
            weights['SC'] * scores['sentiment_label_correctness'] +
            weights['LC'] * scores['logical_correctness'] +
            weights['RC'] * scores['reasoning_coherence'] +
            weights['ML'] * scores['manner_of_language']
        )
        return tps
    except KeyError as e:
        print(f"      [ERROR] Missing expected score key or unknown category '{category}': {e}")
        raise

def process_all_scores(base_dir):
    """Process files, add error handling, and save to PWD mirroring structure."""
    
    base_path = Path(base_dir)
    pwd_path = Path.cwd()
    
    print(f"\n🚀 Starting execution...")
    print(f"📂 Input Base Directory: {base_path}")
    print(f"💾 Output Base Directory (PWD): {pwd_path}\n")

    if not base_path.exists():
        print(f"[FATAL ERROR] The input directory '{base_dir}' does not exist.")
        sys.exit(1)
    
    # Iterate through organizations
    for org_dir in base_path.iterdir():
        if not org_dir.is_dir():
            continue
            
        print(f"▶ Entering organization folder: {org_dir.name}")
            
        # Iterate through model-quantization combinations
        for model_quant_dir in org_dir.iterdir():
            if not model_quant_dir.is_dir():
                continue
            
            model_name = model_quant_dir.name
            print(f"  ▶ Processing Model/Quant: {model_name}")
            
            all_tps = {}
            
            # Iterate through categories
            for category_dir in model_quant_dir.iterdir():
                if not category_dir.is_dir():
                    continue
                
                category = category_dir.name
                score_file = category_dir / 'judge_scores.json'
                
                if not score_file.exists():
                    print(f"    [SKIP] No judge_scores.json found in {category}")
                    continue
                
                print(f"    📄 Reading scores from category: {category}")
                
                # Try loading the JSON
                try:
                    with open(score_file, 'r') as f:
                        data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"    [ERROR] Corrupted JSON in {score_file.name}: {e}")
                    continue
                except Exception as e:
                    print(f"    [ERROR] Could not read {score_file.name}: {e}")
                    continue
                
                # Calculate TPS for each prompt
                print(f"      ⚙️ Calculating TPS for prompts in {category}...")
                for item in data:
                    try:
                        prompt_id = item['id']  
                        scores = item['scores']
                        
                        tps = round(calculate_tps(scores, category), 2)
                        
                        # Parse prompt_id
                        parts = prompt_id.split('_')
                        base_num = parts[1]  
                        level = parts[2]     
                        variant = parts[3] if len(parts) > 3 else "V0"  
                        
                        lvl_num = level.replace('L', '') 
                        prompt_key = f"Prompt {base_num} ({category})" 
                        
                        # Build dictionary structure
                        if lvl_num not in all_tps:
                            all_tps[lvl_num] = {}
                        if prompt_key not in all_tps[lvl_num]:
                            all_tps[lvl_num][prompt_key] = {}
                            
                        all_tps[lvl_num][prompt_key][variant] = tps
                    
                    except Exception as e:
                        # 1. Fetch the correct 'id' instead of the old 'prompt_id'
                        actual_id = item.get('id', 'UNKNOWN_ID')
                        
                        # 2. Grab the actual keys present in the JSON to see what's wrong
                        available_keys = list(item.get('scores', {}).keys())
                        
                        print(f"      [ERROR] Failed processing prompt ID: '{actual_id}'")
                        print(f"        -> Missing Key: {e}")
                        print(f"        -> Keys actually found in your JSON: {available_keys}")
                        continue
            
            # Format into an array of row objects
            print(f"  🏗️ Structuring final JSON array for {model_name}...")
            json_output = []
            level_order = ['0', '1', '2', '3', '4', '5']
            
            for lvl in level_order:
                if lvl in all_tps:
                    row_data = {"Drift_Level": int(lvl)}
                    
                    sorted_keys = sorted(all_tps[lvl].keys(), key=get_numerical_priority)
                    
                    for prompt_key in sorted_keys:
                        variants_dict = all_tps[lvl][prompt_key]
                        
                        # Level 0 handling (Merged cell equivalent)
                        if lvl == '0':
                            try:
                                # Ensure we actually have variants to pull from
                                if variants_dict:
                                    # We expect V0 or V1 to be the only/first key for level 0
                                    first_key = list(variants_dict.keys())[0]
                                    single_val = variants_dict[first_key]
                                else:
                                    single_val = None
                                row_data[prompt_key] = single_val
                            except Exception as e:
                                print(f"      [ERROR] Structuring Level 0 for {prompt_key}: {e}")
                                row_data[prompt_key] = None
                                
                        # Levels 1-5 handling (Sub-columns)
                        else:
                            sorted_variants = {k: variants_dict[k] for k in sorted(variants_dict.keys())}
                            row_data[prompt_key] = sorted_variants
                            
                    json_output.append(row_data)
            
            # Save the structured JSON to PWD mirroring the structure
            if json_output:
                try:
                    # Create the mirrored directory path in PWD: ./org_name/model_name/
                    output_dir = pwd_path / "TPS" / org_dir.name / model_name
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    output_file = output_dir / 'tps_scores_structured.json'
                    with open(output_file, 'w') as f:
                        json.dump(json_output, f, indent=4)
                    print(f"  ✅ Saved output to: {output_file}")
                except Exception as e:
                    print(f"  [ERROR] Failed to save output file for {model_name}: {e}")
            else:
                print(f"  [WARNING] No valid data extracted for {model_name}. Skipping save.")

# Run
if __name__ == "__main__":
    base_dir = r"..\4_response_eval\judge_scores"
    
    try:
        process_all_scores(base_dir)
        print("\n🎉 Execution completed successfully!")
    except KeyboardInterrupt:
        print("\n🛑 Execution manually interrupted by user.")
    except Exception as e:
        print(f"\n💥 An unexpected fatal error occurred: {e}")