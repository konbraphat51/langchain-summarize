"""
Test script to validate the summarizer structure without calling OpenAI
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from summarize import PDFSummarizer


def test_prompt_loading():
    """Test that prompts can be loaded"""
    print("Testing prompt loading...")
    
    # Create a dummy API key for testing
    os.environ["OPENAI_API_KEY"] = "test-key-for-validation"
    
    try:
        summarizer = PDFSummarizer()
        
        # Test loading base prompts
        map_base = summarizer.load_prompt("map_base.txt")
        reduce_base = summarizer.load_prompt("reduce_base.txt")
        map_custom = summarizer.load_prompt("map_custom.txt")
        reduce_custom = summarizer.load_prompt("reduce_custom.txt")
        
        print("✓ All prompts loaded successfully")
        
        # Test creating prompt templates
        map_prompt = summarizer.create_map_prompt()
        reduce_prompt = summarizer.create_reduce_prompt()
        
        print("✓ Prompt templates created successfully")
        
        # Display prompt structure
        print("\n--- Map Prompt Template ---")
        print(f"Input variables: {map_prompt.input_variables}")
        print(f"Template type: {type(map_prompt).__name__}")
        
        print("\n--- Reduce Prompt Template ---")
        print(f"Input variables: {reduce_prompt.input_variables}")
        print(f"Template type: {type(reduce_prompt).__name__}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_initialization():
    """Test that the summarizer initializes correctly"""
    print("\nTesting initialization...")
    
    os.environ["OPENAI_API_KEY"] = "test-key-for-validation"
    
    try:
        summarizer = PDFSummarizer(model_name="gpt-3.5-turbo", temperature=0.3)
        print(f"✓ Summarizer initialized with model: {summarizer.llm.model_name}")
        print(f"✓ Temperature: {summarizer.llm.temperature}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 80)
    print("LangChain PDF Summarizer - Structure Validation")
    print("=" * 80)
    
    results = []
    
    results.append(("Initialization", test_initialization()))
    results.append(("Prompt Loading", test_prompt_loading()))
    
    print("\n" + "=" * 80)
    print("Test Results Summary")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ All tests passed! The structure is correct.")
        print("\nTo use the summarizer:")
        print("1. Set your OpenAI API key in .env file")
        print("2. Run: uv run python summarize.py your_document.pdf")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
