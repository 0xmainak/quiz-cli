import json
import os
from typing import Dict, List, Any, Optional, Union
from functools import lru_cache
from pathlib import Path

class DataLoader:
    """Advanced data loader class for managing quiz content with caching and validation"""

    def __init__(self, data_dir: Union[str, Path] = "./data", config_dir: Union[str, Path] = "./config"):
        """
        Initialize the DataLoader with configurable paths and caching
        
        Args:
            data_dir: Directory containing quiz data files
            config_dir: Directory containing configuration files
        """
        self.data_dir = Path(data_dir)
        self.config_dir = Path(config_dir)
        self._cache = {}
        self._validate_paths()

    def _validate_paths(self) -> None:
        """Validate that required directories and files exist"""
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")

    @lru_cache(maxsize=32)
    def _load_json(self, filepath: Union[str, Path]) -> Dict:
        """
        Load and cache JSON file with error handling
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Dict containing parsed JSON data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If invalid JSON
        """
        filepath = Path(filepath)
        if filepath not in self._cache:
            if not filepath.exists():
                raise FileNotFoundError(f"File not found: {filepath}")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    self._cache[filepath] = json.load(f)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Invalid JSON in {filepath}: {str(e)}", e.doc, e.pos)
        return self._cache[filepath]

    def get_question(self, json_name: str, index: int) -> Dict[str, Any]:
        """
        Get question data by topic and index with validation
        
        Args:
            json_name: Topic identifier
            index: Question index
            
        Returns:
            Question data dictionary
            
        Raises:
            IndexError: If index out of range
        """
        data = self._load_json(self.data_dir / f"{json_name}.json")
        if not 0 <= index < len(data):
            raise IndexError(f"Question index {index} out of range for topic {json_name}")
        return data[index]

    def get_answer(self, question: Dict[str, Any]) -> str:
        """
        Get correct answer from question data
        
        Args:
            question: Question dictionary containing answer
            
        Returns:
            Correct answer string
            
        Raises:
            KeyError: If answer field missing
        """
        if "answer" not in question:
            raise KeyError("Question dictionary missing required 'answer' field")
        return question["answer"]

    def get_topic(self, index: Union[str, int]) -> str:
        """
        Get topic identifier by index
        
        Args:
            index: Topic index
            
        Returns:
            Topic identifier string
            
        Raises:
            KeyError: If invalid topic index
        """
        topics = self._load_json(self.config_dir / "topics.json")["topics"]
        if not topics:  # Check if topics list is empty
            raise KeyError("No topics found in topics.json")
        if not 0 <= index < len(topics):
            raise KeyError(f"Invalid topic index: {index}. Valid indices are 0-{len(topics)-1}")
        return topics[index]["file_name"]

    def get_length(self, json_name: str) -> int:
        """
        Get number of questions for topic
        
        Args:
            json_name: Topic identifier
            
        Returns:
            Number of questions
        """
        data = self._load_json(self.data_dir / f"{json_name}.json")
        return len(data)
    
    def get_topics(self) -> List[str]:
        """
        Get list of all available topics
        
        Returns:
            List of topic display names
        """
        topics = self._load_json(self.config_dir / "topics.json")["topics"]
        return [topic["display_name"] for topic in topics]
