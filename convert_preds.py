#!/usr/bin/env python3
"""
Standalone converter script for all_preds.jsonl to multiswebench format
Usage: python convert_preds.py <input_file> <output_file>
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


class PredsConverter:
    """
    Convert all_preds.jsonl format to multiswebench test script compatible Patch format
    
    Input format (all_preds.jsonl):
    {
        "model_name_or_path": "agentless",
        "instance_id": "org__repo-PR_number", 
        "model_patch": "diff --git ..."
    }
    
    Output format (multiswebench):
    {
        "org": "org_name",
        "repo": "repo_name", 
        "number": PR_number,
        "fix_patch": "diff --git ..."
    }
    """
    
    def __init__(self):
        pass
    
    def parse_instance_id(self, instance_id: str) -> tuple[str, str, int]:
        """
        Parse instance_id format: org__repo-PR_number
        Example: zeromicro__go-zero-2787 -> ('zeromicro', 'go-zero', 2787)
        """
        # Match format: org__repo-PR_number
        # Use more flexible regex to handle repository names with hyphens
        pattern = r'^([^_]+)__(.+)-(\d+)$'
        match = re.match(pattern, instance_id)
        
        if not match:
            raise ValueError(f"Invalid instance_id format: {instance_id}")
        
        org, repo, number = match.groups()
        return org, repo, int(number)
    
    def convert_pred_to_patch(self, pred_data: dict) -> dict:
        """
        Convert single prediction data to patch dictionary
        
        Args:
            pred_data: Dictionary containing model_name_or_path, instance_id, model_patch
            
        Returns:
            Dictionary containing org, repo, number, fix_patch
        """
        instance_id = pred_data["instance_id"]
        model_patch = pred_data["model_patch"]
        
        # Parse instance_id
        org, repo, number = self.parse_instance_id(instance_id)
        
        # Create patch dictionary
        patch = {
            "org": org,
            "repo": repo,
            "number": number,
            "fix_patch": model_patch
        }
        
        return patch
    
    def convert_preds_file(self, preds_file_path: str | Path) -> List[dict]:
        """
        Convert entire preds file to patch list
        
        Args:
            preds_file_path: all_preds.jsonl file path
            
        Returns:
            List of patch dictionaries
        """
        patches = []
        
        with open(preds_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    pred_data = json.loads(line)
                    patch = self.convert_pred_to_patch(pred_data)
                    patches.append(patch)
                except Exception as e:
                    print(f"Error parsing line {line_num}: {e}")
                    continue
        
        return patches
    
    def save_patches_to_file(self, patches: List[dict], output_file_path: str | Path):
        """
        Save patch list to JSONL file
        
        Args:
            patches: List of patch dictionaries
            output_file_path: Output file path
        """
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for patch in patches:
                f.write(json.dumps(patch) + '\n')
    
    def convert_and_save(self, preds_file_path: str | Path, output_file_path: str | Path):
        """
        Convert preds file and save to test script compatible format
        
        Args:
            preds_file_path: Input all_preds.jsonl file path
            output_file_path: Output patch file path
        """
        patches = self.convert_preds_file(preds_file_path)
        self.save_patches_to_file(patches, output_file_path)
        print(f"Converted {len(patches)} patches from {preds_file_path} to {output_file_path}")


def main():
    """
    Command line tool entry point
    """
    if len(sys.argv) != 3:
        print("Usage: python convert_preds.py <input_file> <output_file>")
        print("Example: python convert_preds.py all_preds.jsonl converted_patches.jsonl")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert the file
    converter = PredsConverter()
    try:
        converter.convert_and_save(input_file, output_file)
        print("✅ Conversion completed successfully!")
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
