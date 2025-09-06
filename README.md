# Agentless Universe

A comprehensive toolkit for automated bug localization and repair, featuring enhanced MultiSWE-Bench evaluation capabilities.

## 🚀 Features

### Agentless - Automated Bug Repair
- **Localization**: Automatically identify bug locations in code
- **Retrieval**: Find relevant code context for bug repair
- **Repair**: Generate patches to fix identified bugs
- **Flexible Model Support**: Use any LLM model via custom API endpoints
- **Local Dataset Support**: Work with local SWE-bench datasets

### MultiSWE-Bench - Enhanced Evaluation
- **Prediction Format Converter**: Convert model predictions to evaluation format
- **Comprehensive Testing**: Support for multiple programming languages
- **Flexible Configuration**: Easy-to-use configuration system

## 📁 Project Structure

```
Agentless universe/
├── Agentless/                    # Main Agentless framework
│   ├── agentless/
│   │   ├── fl/                   # Fault localization
│   │   ├── repair/               # Bug repair
│   │   ├── test/                 # Testing utilities
│   │   └── util/                 # Utilities
│   └── classification/           # Classification tools
├── multi-swe-bench/              # MultiSWE-Bench evaluation
│   ├── multi_swe_bench/
│   │   ├── harness/              # Evaluation harness
│   │   ├── collect/              # Data collection
│   │   └── utils/                # Utilities
│   └── docs/                     # Documentation
└── convert_preds.py             # Prediction format converter
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git
- Conda (recommended)

### Environment Setup

This project uses two separate environments for different purposes:

#### 1. Agentless Environment (for bug repair)
```bash
# Create conda environment for Agentless
conda create -n agentless python=3.10
conda activate agentless

# Install Agentless dependencies
pip install -r Agentless/requirements.txt
```

#### 2. MultiSWE-Bench Environment (for evaluation)
```bash
# Create conda environment for MultiSWE-Bench
conda create -n multiswebench python=3.10
conda activate multiswebench

# Install MultiSWE-Bench dependencies
pip install -r multi-swe-bench/requirements.txt
```

## 🎯 Quick Start

### 1. Agentless Bug Repair

**Environment**: Use the `agentless` environment

```bash
# Activate Agentless environment
conda activate agentless
cd Agentless

# Set up environment
export PYTHONPATH=$PYTHONPATH:$(pwd)
export OPENAI_API_KEY="your-api-key-here"

# Create results directory
mkdir -p results
```

#### Complete Agentless Pipeline

The Agentless framework follows a 3-stage localization process followed by repair and validation:

##### Stage 1: Localize to Suspicious Files

**Step 1.1: LLM-based File Localization**
```bash
python agentless/fl/localize.py --file_level \
                                --output_folder results/file_level \
                                --local_dataset /path/to/local_dataset.jsonl \
                                --model your-model-name \
                                --backend openai \
                                --num_threads 10 \
                                --skip_existing
```

**Step 1.2: Identify Irrelevant Folders**
```bash
python agentless/fl/localize.py --file_level \
                                --irrelevant \
                                --output_folder results/file_level_irrelevant \
                                --local_dataset /path/to/local_dataset.jsonl \
                                --model your-model-name \
                                --backend openai \
                                --num_threads 10 \
                                --skip_existing
```

**Step 1.3: Embedding-based Retrieval**
```bash
python agentless/fl/retrieve.py --index_type simple \
                                --filter_type given_files \
                                --filter_file results/file_level_irrelevant/loc_outputs.jsonl \
                                --output_folder results/retrieval_embedding \
                                --persist_dir embedding/swe-bench_simple \
                                --local_dataset /path/to/local_dataset.jsonl \
                                --model your-model-name \
                                --backend openai \
                                --num_threads 10
```

**Step 1.4: Combine LLM and Retrieval Results**
```bash
python agentless/fl/combine.py --retrieval_loc_file results/retrieval_embedding/retrieve_locs.jsonl \
                               --model_loc_file results/file_level/loc_outputs.jsonl \
                               --top_n 3 \
                               --output_folder results/file_level_combined
```

##### Stage 2: Localize to Related Elements

```bash
python agentless/fl/localize.py --related_level \
                                --output_folder results/related_elements \
                                --top_n 3 \
                                --compress_assign \
                                --compress \
                                --start_file results/file_level_combined/combined_locs.jsonl \
                                --local_dataset /path/to/local_dataset.jsonl \
                                --model your-model-name \
                                --backend openai \
                                --num_threads 10 \
                                --skip_existing
```

##### Stage 3: Localize to Edit Locations

**Step 3.1: Generate Edit Location Samples**
```bash
python agentless/fl/localize.py --fine_grain_line_level \
                                --output_folder results/edit_location_samples \
                                --top_n 3 \
                                --compress \
                                --temperature 0.8 \
                                --num_samples 4 \
                                --start_file results/related_elements/loc_outputs.jsonl \
                                --local_dataset /path/to/local_dataset.jsonl \
                                --model your-model-name \
                                --backend openai \
                                --num_threads 10 \
                                --skip_existing
```

**Step 3.2: Separate Individual Edit Location Sets**
```bash
python agentless/fl/localize.py --merge \
                                --output_folder results/edit_location_individual \
                                --top_n 3 \
                                --num_samples 4 \
                                --start_file results/edit_location_samples/loc_outputs.jsonl
```

##### Stage 4: Repair

Generate patches using the edit locations:

```bash
python agentless/repair/repair.py --loc_file results/edit_location_individual/loc_merged_0-0_outputs.jsonl \
                                  --output_folder results/repair_sample_1 \
                                  --local_dataset /path/to/local_dataset.jsonl \
                                  --model your-model-name \
                                  --backend openai \
                                  --loc_interval \
                                  --top_n=3 \
                                  --context_window=10 \
                                  --max_samples 10 \
                                  --cot \
                                  --diff_format \
                                  --gen_and_process \
                                  --num_threads 2
```

**Repeat for all 4 edit location sets:**
```bash
# For samples 1-4
for i in {1..4}; do
    python agentless/repair/repair.py --loc_file results/edit_location_individual/loc_merged_$((i-1))-$((i-1))_outputs.jsonl \
                                      --output_folder results/repair_sample_$i \
                                      --local_dataset /path/to/local_dataset.jsonl \
                                      --model your-model-name \
                                      --backend openai \
                                      --loc_interval \
                                      --top_n=3 \
                                      --context_window=10 \
                                      --max_samples 10 \
                                      --cot \
                                      --diff_format \
                                      --gen_and_process \
                                      --num_threads 2
done
```

##### Stage 5: Patch Validation and Selection

**Step 5.1: Generate Regression Tests**
```bash
python agentless/test/run_regression_tests.py --run_id generate_regression_tests \
                                              --output_file results/passing_tests.jsonl
```

**Step 5.2: Select Regression Tests**
```bash
python agentless/test/select_regression_tests.py --passing_tests results/passing_tests.jsonl \
                                                 --output_folder results/select_regression
```

**Step 5.3: Run Regression Tests on Patches**
```bash
folder=results/repair_sample_1
for num in {0..9..1}; do
    run_id_prefix=$(basename $folder)
    python agentless/test/run_regression_tests.py --regression_tests results/select_regression/output.jsonl \
                                                  --predictions_path="${folder}/output_${num}_processed.jsonl" \
                                                  --run_id="${run_id_prefix}_regression_${num}" \
                                                  --num_workers 10
done
```

**Step 5.4: Generate Reproduction Tests**
```bash
python agentless/test/generate_reproduction_tests.py --max_samples 40 \
                                                     --output_folder results/reproduction_test_samples \
                                                     --local_dataset /path/to/local_dataset.jsonl \
                                                     --model your-model-name \
                                                     --backend openai \
                                                     --num_threads 10
```

**Step 5.5: Execute Reproduction Tests**
```bash
for st in {0..36..4}; do
    en=$((st + 3))
    echo "Processing ${st} to ${en}"
    for num in $(seq $st $en); do
        echo "Processing ${num}"
        python agentless/test/run_reproduction_tests.py --run_id="reproduction_test_generation_filter_sample_${num}" \
                                                        --test_jsonl="results/reproduction_test_samples/output_${num}_processed_reproduction_test.jsonl" \
                                                        --num_workers 6 \
                                                        --testing
    done &
done
```

**Step 5.6: Select Final Reproduction Tests**
```bash
python agentless/test/generate_reproduction_tests.py --max_samples 40 \
                                                     --output_folder results/reproduction_test_samples \
                                                     --output_file reproduction_tests.jsonl \
                                                     --select
```

**Step 5.7: Evaluate Patches on Reproduction Tests**
```bash
folder=results/repair_sample_1
for num in {0..9..1}; do
    run_id_prefix=$(basename $folder)
    python agentless/test/run_reproduction_tests.py --test_jsonl results/reproduction_test_samples/reproduction_tests.jsonl \
                                                    --predictions_path="${folder}/output_${num}_processed.jsonl" \
                                                    --run_id="${run_id_prefix}_reproduction_${num}" \
                                                    --num_workers 10
done
```

**Step 5.8: Final Patch Selection**
```bash
python agentless/repair/rerank.py --patch_folder results/repair_sample_1/,results/repair_sample_2/,results/repair_sample_3/,results/repair_sample_4/ \
                                  --num_samples 40 \
                                  --deduplicate \
                                  --regression \
                                  --reproduction
```

#### Simplified Usage (Single Target)

For testing with a single target:

```bash
# Localization
python agentless/fl/localize.py --output_folder results/localization \
                                --local_dataset /path/to/local_dataset.jsonl \
                                --model your-model-name \
                                --backend openai \
                                --target_id your-target-id

# Retrieval
python agentless/fl/retrieve.py --output_folder results/retrieval \
                                --local_dataset /path/to/local_dataset.jsonl \
                                --model your-model-name \
                                --backend openai

# Repair
python agentless/repair/repair.py --loc_file results/localization/loc_outputs.jsonl \
                                  --output_folder results/repair \
                                  --local_dataset /path/to/local_dataset.jsonl \
                                  --model your-model-name \
                                  --backend openai \
                                  --target_id your-target-id
```

### 2. MultiSWE-Bench Evaluation

**Environment**: Use the `multiswebench` environment

```bash
# Activate MultiSWE-Bench environment
conda activate multiswebench
```

#### Convert Predictions
```bash
# This can be run in either environment
python convert_preds.py input_predictions.jsonl output_patches.jsonl
```

#### Run Evaluation
```bash
cd multi-swe-bench
python -m multi_swe_bench.harness.run_evaluation \
  --config config_example.json
```

## 🔧 Configuration

### Environment Management

This project uses two separate conda environments to avoid dependency conflicts:

- **`agentless`**: For running Agentless bug repair tasks
- **`multiswebench`**: For running MultiSWE-Bench evaluation tasks

#### Switching Between Environments
```bash
# For Agentless tasks
conda activate agentless

# For MultiSWE-Bench evaluation
conda activate multiswebench
```

### Model Configuration
All scripts now support flexible model configuration:

- **Model**: Any model name supported by your backend
- **Backend**: `openai`, `deepseek`, `anthropic`, or custom endpoints
- **API Endpoints**: Custom base URLs and API keys

### Environment Variables
```bash
export OPENAI_API_BASE="https://your-api-endpoint.com/v1"
export OPENAI_API_KEY="your-api-key"
```

## 📊 Supported Formats

### Input Data Formats
- **SWE-bench**: Standard SWE-bench dataset format
- **Predictions**: Model prediction format with `instance_id` and `model_patch`
- **Local Datasets**: JSONL format for local dataset files

### Output Formats
- **Patches**: Git diff format patches
- **Evaluations**: JSON reports with success/failure metrics
- **Logs**: Detailed execution logs

## 🌟 Key Improvements

### Enhanced Flexibility
- ✅ **No Model Restrictions**: Use any LLM model
- ✅ **Custom API Support**: Support for custom API endpoints
- ✅ **Local Dataset Support**: Work with local datasets
- ✅ **Flexible Backend**: Support for multiple API providers

### Improved Usability
- ✅ **Standalone Converter**: Independent prediction format converter
- ✅ **Comprehensive Documentation**: Clear usage instructions
- ✅ **Example Configurations**: Ready-to-use configuration files

## 💰 Cost Analysis

To measure the cost of running Agentless, use the provided cost analysis utility:

```bash
# Calculate cost for any step's output
python dev/util/cost.py --output_file results/step_name/output.jsonl

# Include embedding costs
python dev/util/cost.py --output_file results/step_name/output.jsonl --embedding_cost
```

This will output the dollar cost and token usage for each step.

## 📊 Output Structure

### Key Output Files

- **`loc_outputs.jsonl`**: Contains localization results with file paths and edit locations
- **`output.jsonl`**: Contains generated patches and repair trajectories
- **`all_preds.jsonl`**: Final selected patches ready for evaluation
- **`*_test_results.jsonl`**: Test execution results for validation

### Results Directory Structure
```
results/
├── file_level/                    # Stage 1.1: LLM file localization
├── file_level_irrelevant/         # Stage 1.2: Irrelevant folder identification
├── retrieval_embedding/           # Stage 1.3: Embedding-based retrieval
├── file_level_combined/           # Stage 1.4: Combined file locations
├── related_elements/              # Stage 2: Related element localization
├── edit_location_samples/         # Stage 3.1: Edit location samples
├── edit_location_individual/      # Stage 3.2: Individual edit location sets
├── repair_sample_1-4/            # Stage 4: Repair results (4 samples)
├── passing_tests.jsonl           # Stage 5.1: Generated regression tests
├── select_regression/            # Stage 5.2: Selected regression tests
├── reproduction_test_samples/     # Stage 5.4-5.6: Reproduction test generation
└── all_preds.jsonl               # Final output: Selected patches
```

## 📚 Documentation

- [Agentless Usage Guide](Agentless/README.md)
- [MultiSWE-Bench Documentation](multi-swe-bench/README.md)
- [Configuration Examples](multi-swe-bench/config_example.json)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original Agentless framework
- MultiSWE-Bench evaluation framework
- SWE-bench dataset contributors
