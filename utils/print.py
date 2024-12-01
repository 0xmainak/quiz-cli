from utils.loader import DataLoader
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich.layout import Layout
from rich.syntax import Syntax
from typing import List, Dict, Any, Optional
from datetime import datetime

class QuizPrinter:
    """Advanced class to handle all quiz-related printing functionality with enhanced styling"""
    
    def __init__(self, console: Console = None, theme: str = "default"):
        """
        Initialize QuizPrinter with customizable styling options
        
        Args:
            console: Rich Console instance for output. Creates new one if not provided.
            theme: Theme name to use for styling ('default', 'dark', 'light')
        """
        self.console = console or Console()
        self.options = ["A", "B", "C", "D"]
        self.theme = self._get_theme(theme)
        self._init_styles()

    def _get_theme(self, theme_name: str) -> Dict[str, str]:
        """Define color schemes for different themes"""
        themes = {
            "default": {
                "primary": "cyan",
                "secondary": "magenta",
                "accent": "green",
                "error": "red"
            },
            "dark": {
                "primary": "blue",
                "secondary": "purple",
                "accent": "yellow",
                "error": "red"
            },
            "light": {
                "primary": "cyan",
                "secondary": "magenta",
                "accent": "green",
                "error": "red"
            }
        }
        return themes.get(theme_name, themes["default"])

    def _init_styles(self) -> None:
        """Initialize rich styles for consistent formatting"""
        self.styles = {
            "title": Style(color=self.theme["primary"], bold=True),
            "subtitle": Style(color=self.theme["secondary"], italic=True),
            "highlight": Style(color=self.theme["accent"], bold=True),
            "error": Style(color=self.theme["error"], bold=True)
        }

    def print_welcome(self) -> None:
        """Print an enhanced welcome message with dynamic styling"""
        layout = Layout()
        layout.split_column(
            Layout(name="header"),
            Layout(name="content")
        )
        
        current_time = datetime.now().strftime("%H:%M:%S")
        welcome_text = Text.assemble(
            ("Welcome to the ", self.styles["title"]),
            ("Advanced ", self.styles["highlight"]),
            ("Quiz Game!\n", self.styles["title"]),
            (f"Session started at {current_time}", self.styles["subtitle"])
        )
        
        self.console.print(Panel(
            welcome_text,
            title="[bold]Quiz Master[/bold]",
            subtitle="[italic]Test Your Knowledge[/italic]",
            border_style=self.theme["primary"],
            padding=(1, 2)
        ))

    def print_topics(self, loader: DataLoader) -> None:
        """
        Print available quiz topics in an enhanced table format
        
        Args:
            loader: DataLoader instance containing topic data
        """
        table = Table(
            show_header=True,
            header_style=self.styles["title"],
            border_style=self.theme["primary"],
            title="Available Topics"
        )
        
        table.add_column("ID", justify="center", style=self.styles["subtitle"])
        table.add_column("Topic", style=self.styles["highlight"])
        table.add_column("Questions", justify="right", style=self.styles["subtitle"])
        
        topics = loader.get_topics()
        for i, topic in enumerate(topics):
            table.add_row(
                str(i),
                topic,
                str(loader.get_length(loader.get_topic(str(i))))
            )
        
        self.console.print(table)

    def print_question(
        self,
        loader: DataLoader,
        json_name: str,
        index: int,
        question_num: int,
        time_remaining: Optional[int] = None
    ) -> None:
        """
        Print enhanced formatted quiz question with options and metadata
        
        Args:
            loader: DataLoader instance to fetch question data
            json_name: Name of the JSON file containing questions
            index: Index of question to print
            question_num: Question number to display
            time_remaining: Optional time remaining in seconds
        """
        question_data = loader.get_question(json_name, index)
        self._print_question_text(question_data, question_num, time_remaining)
        self._print_options(question_data)

    def _print_question_text(
        self,
        question_data: Dict[str, Any],
        question_num: int,
        time_remaining: Optional[int] = None
    ) -> None:
        """
        Print the question text with enhanced styling and metadata
        
        Args:
            question_data: Dictionary containing question information
            question_num: Question number to display
            time_remaining: Optional time remaining in seconds
        """
        header = f"Question {question_num}"
        if time_remaining is not None:
            header += f" | Time Remaining: {time_remaining}s"
            
        question_panel = Panel(
            Text(question_data['question'], style=self.styles["highlight"]),
            title=header,
            border_style=self.theme["primary"],
            padding=(1, 2)
        )
        
        self.console.print("\n")
        self.console.print(question_panel)

    def _print_options(self, question_data: Dict[str, Any]) -> None:
        """
        Print question options with enhanced formatting
        
        Args:
            question_data: Dictionary containing option information
        """
        options_table = Table(
            show_header=False,
            box=None,
            padding=(0, 4),
            border_style=self.theme["secondary"]
        )
        
        for opt in self.options:
            options_table.add_row(
                Text(f"{opt}.", style=self.styles["subtitle"]),
                Text(question_data[opt], style=self.styles["title"])
            )
            
        self.console.print(options_table)
