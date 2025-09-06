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

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd Agentless-universe

# Create conda environment
conda create -n agentless python=3.10
conda activate agentless

# Install dependencies
pip install -r Agentless/requirements.txt
pip install -r multi-swe-bench/requirements.txt
```

## 🎯 Quick Start

### 1. Agentless Bug Repair

#### Localization
```bash
cd Agentless
python agentless/fl/localize.py \
  --output_folder results/localization \
  --model your-model-name \
  --backend openai \
  --local_dataset path/to/dataset.jsonl
```

#### Retrieval
```bash
python agentless/fl/retrieve.py \
  --output_folder results/retrieval \
  --model your-model-name \
  --backend openai \
  --local_dataset path/to/dataset.jsonl
```

#### Repair
```bash
python agentless/repair/repair.py \
  --loc_file results/localization/loc_outputs.jsonl \
  --output_folder results/repair \
  --model your-model-name \
  --backend openai \
  --local_dataset path/to/dataset.jsonl \
  --target_id your-target-id
```

### 2. MultiSWE-Bench Evaluation

#### Convert Predictions
```bash
python convert_preds.py input_predictions.jsonl output_patches.jsonl
```

#### Run Evaluation
```bash
cd multi-swe-bench
python -m multi_swe_bench.harness.run_evaluation \
  --config config_example.json
```

## 🔧 Configuration

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
