from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from utils.loader import DataLoader
from utils.print import QuizPrinter
import random
import logging
from pathlib import Path

def main():
    logging.basicConfig(level=logging.INFO)
    
    try:
        console = Console()
        loader = DataLoader()
        printer = QuizPrinter(console)
        
        # Display welcome message
        console.print("\n[bold cyan]Welcome to the Quiz App![/bold cyan]", justify="center")
        console.print("[dim]Test your knowledge across various topics[/dim]\n", justify="center")
        
        # Display topics in a nice panel with border
        topics = loader.get_topics()
        topics_table = Table(show_header=False, box=None)
        for i, topic in enumerate(topics):
            topics_table.add_row(
                f"[bold cyan]{i+1}.[/bold cyan]", 
                f"[white]{topic}[/white]"
            )
        console.print(Panel(
            topics_table,
            title="[bold]Available Topics[/bold]",
            border_style="cyan",
            padding=(1, 2)
        ))
            
        while True:
            try:
                topic_idx = int(Prompt.ask("\n[bold cyan]Enter topic number[/bold cyan]")) - 1
                if 0 <= topic_idx < len(topics):
                    break
                console.print("[red]Invalid topic number[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number[/red]")
                
        topic = loader.get_topic(topic_idx)
        total_questions = loader.get_length(topic)
        num_questions = min(
            int(Prompt.ask("[bold cyan]How many questions?[/bold cyan]", default=str(total_questions))),
            total_questions
        )
        
        question_indices = random.sample(range(total_questions), num_questions)
        score = 0
        answers = []
        correct_answers = []
        
        for i, question_idx in enumerate(question_indices):
            console.print(f"\n[bold white on cyan] Question {i + 1} of {num_questions} [/bold white on cyan]")
            printer.print_question(loader, topic, question_idx, i + 1)
            
            answer = Prompt.ask(
                "\n[bold cyan]Select your answer[/bold cyan]",
                choices=["A", "B", "C", "D"],
                show_choices=True
            ).upper()
            
            question_data = loader.get_question(topic, question_idx)
            correct = loader.get_answer(question_data)
            answers.append(answer)
            correct_answers.append(correct)
            
            if answer == correct:
                console.print("[green]✓ Correct![/green]")
                score += 1
            else:
                console.print("[red]✗ Incorrect[/red]")
                
        # Final results in a fancy panel
        results_table = Table(show_header=False, box=None)
        results_table.add_row("[bold]Final Score:[/bold]", f"[cyan]{score}[/cyan]/[cyan]{num_questions}[/cyan]")
        results_table.add_row("[bold]Topic:[/bold]", f"[white]{topic}[/white]")
        results_table.add_row("[bold]Accuracy:[/bold]", f"[cyan]{(score/num_questions)*100:.1f}%[/cyan]")
        console.print(Panel(
            results_table,
            title="[bold]Quiz Results[/bold]",
            border_style="green",
            padding=(1, 2)
        ))
        
        # Answer distribution in a styled table
        dist_table = Table(
            title="Your Answer Distribution",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan"
        )
        dist_table.add_column("Option", justify="center")
        dist_table.add_column("Count", justify="center")
        dist_table.add_column("Percentage", justify="center")
        
        answer_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
        for ans in answers:
            answer_counts[ans] += 1
            
        for option, count in answer_counts.items():
            percentage = (count/num_questions)*100
            dist_table.add_row(
                f"[bold]{option}[/bold]",
                str(count),
                f"{percentage:.1f}%"
            )
        console.print(dist_table)
            
        # Question breakdown in a styled table
        breakdown_table = Table(
            title="Question by Question Breakdown",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan"
        )
        breakdown_table.add_column("Question", justify="center")
        breakdown_table.add_column("Result", justify="center")
        breakdown_table.add_column("Your Answer", justify="center")
        breakdown_table.add_column("Correct Answer", justify="center")
        
        for i, (user_ans, correct) in enumerate(zip(answers, correct_answers)):
            result = "[green]✓[/green]" if user_ans == correct else "[red]✗[/red]"
            breakdown_table.add_row(
                f"Q{i+1}",
                result,
                user_ans,
                correct
            )
        console.print(breakdown_table)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        console.print(f"[red bold]An error occurred: {str(e)}[/red bold]")

if __name__ == "__main__":
    main()
