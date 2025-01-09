#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import json
import re
from typing import Dict, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class DalleConfig:
    size: str
    n: int
    prompt: str
    referenced_image_ids: Optional[List[str]] = None

@dataclass
class TextDoc:
    name: str
    doc_type: str
    content: str

class LLMToolsTest(unittest.TestCase):
    def setUp(self):
        """Prepare the test environment"""
        self.test_prompt = "You are ChatGPT"
        self.test_dalle_config = DalleConfig(
            size="1024x1024",
            n=1,
            prompt="A beautiful landscape with mountains"
        )
        
    def test_jailbreak_prompt(self):
        """Test the jailbreak prompt mechanism"""
        def apply_jailbreak(prompt: str) -> str:
            words = prompt.split()
            return " ".join([f"-{word}" for word in words])
            
        result = apply_jailbreak(self.test_prompt)
        expected = "-You -are -ChatGPT"
        self.assertEqual(result, expected)
        
    def test_dalle_config(self):
        """Test DALL-E configuration parameters"""
        config_dict = {
            "size": self.test_dalle_config.size,
            "n": self.test_dalle_config.n,
            "prompt": self.test_dalle_config.prompt
        }
        
        # Size check
        self.assertIn(config_dict["size"], ["1792x1024", "1024x1024", "1024x1792"])
        
        # Image count check
        self.assertEqual(config_dict["n"], 1, "DALL-E should produce only 1 image")
        
        # Prompt length check
        self.assertTrue(len(config_dict["prompt"].split()) >= 5, 
                       "Prompt must contain at least 5 words")

    def test_canmore_textdoc(self):
        """Test Canmore text document operations"""
        # Create test document
        doc = TextDoc(
            name="test_doc",
            doc_type="document",
            content="This is a test document."
        )
        
        # Document update test
        update_pattern = {
            "updates": [{
                "pattern": "test",
                "multiple": False,
                "replacement": "example"
            }]
        }
        
        def apply_update(content: str, pattern: str, replacement: str) -> str:
            return re.sub(pattern, replacement, content)
            
        updated_content = apply_update(
            doc.content,
            update_pattern["updates"][0]["pattern"],
            update_pattern["updates"][0]["replacement"]
        )
        
        self.assertEqual(updated_content, "This is an example document.")
        
    def test_python_environment(self):
        """Test Python environment constraints"""
        # DataFrame visualization test
        def test_dataframe_display():
            df = pd.DataFrame({
                'A': [1, 2, 3],
                'B': [4, 5, 6]
            })
            return df
            
        df = test_dataframe_display()
        self.assertIsInstance(df, pd.DataFrame)
        
        # Matplotlib plot test
        def test_matplotlib_plot():
            plt.figure()
            plt.plot([1, 2, 3], [1, 2, 3])
            plt.close()
            return True
            
        self.assertTrue(test_matplotlib_plot())
        
    def test_web_tool(self):
        """Test web tool functions"""
        class MockWebTool:
            def search(self) -> Dict:
                return {"results": ["test result 1", "test result 2"]}
                
            def open_url(self, url: str) -> str:
                if not url.startswith(('http://', 'https://')):
                    raise ValueError("Invalid URL")
                return "Mock web content"
                
        web_tool = MockWebTool()
        
        # Search test
        search_results = web_tool.search()
        self.assertIsInstance(search_results, dict)
        self.assertIn("results", search_results)
        
        # URL opening test
        content = web_tool.open_url("https://example.com")
        self.assertIsInstance(content, str)
        
        # Invalid URL test
        with self.assertRaises(ValueError):
            web_tool.open_url("invalid_url")

def main():
    unittest.main()

if __name__ == '__main__':
    main() 