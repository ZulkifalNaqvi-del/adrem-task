"""
CSV Reporter Utility
Generates CSV reports for test execution steps with success/failure status
"""
import csv
import os
from datetime import datetime
from typing import List, Dict
from utils.logger import logger


class CSVReporter:
    """
    CSV Reporter for test execution
    Creates detailed CSV reports for each test step with success/failure status
    """
    
    def __init__(self, report_name: str = "test_execution_report"):
        """
        Initialize CSV Reporter
        
        Args:
            report_name: Name of the CSV report file (without extension)
        """
        self.report_name = report_name
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        
        # Create reports directory if it doesn't exist
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.csv_file = os.path.join(self.reports_dir, f"{report_name}_{timestamp}.csv")
        
        # CSV header
        self.headers = [
            'Step Number',
            'Step Name',
            'Status',
            'Duration (seconds)',
            'Details',
            'Error Message'
        ]
        
        # Test steps data
        self.steps: List[Dict] = []
        
        logger.info(f"CSV Reporter initialized: {self.csv_file}")
    
    def add_step(self, step_number: int, step_name: str, status: str, 
                 duration: float, details: str = "", error_message: str = ""):
        """
        Add a test step to the report
        
        Args:
            step_number: Step number in the test
            step_name: Name/description of the step
            status: SUCCESS or FAILED
            duration: Duration in seconds
            details: Additional details about the step
            error_message: Error message if step failed
        """
        step = {
            'Step Number': step_number,
            'Step Name': step_name,
            'Status': status,
            'Duration (seconds)': round(duration, 2),
            'Details': details,
            'Error Message': error_message
        }
        
        self.steps.append(step)
        logger.debug(f"Added step to CSV report: {step_name} - {status}")
    
    def generate_report(self):
        """Generate the CSV report file"""
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(self.steps)
            
            logger.info(f"CSV report generated successfully: {self.csv_file}")
            return self.csv_file
        except Exception as e:
            logger.error(f"Failed to generate CSV report: {e}")
            raise
    
    def add_summary(self):
        """Add a summary row to the report"""
        total_steps = len(self.steps)
        passed_steps = sum(1 for step in self.steps if step['Status'] == 'SUCCESS')
        failed_steps = total_steps - passed_steps
        total_duration = sum(step['Duration (seconds)'] for step in self.steps)
        
        summary = {
            'Step Number': '',
            'Step Name': 'SUMMARY',
            'Status': 'PASSED' if failed_steps == 0 else 'FAILED',
            'Duration (seconds)': round(total_duration, 2),
            'Details': f"Total: {total_steps}, Passed: {passed_steps}, Failed: {failed_steps}",
            'Error Message': ''
        }
        
        self.steps.append(summary)
        logger.info(f"Summary added - Total: {total_steps}, Passed: {passed_steps}, Failed: {failed_steps}")
    
    def get_report_path(self) -> str:
        """Get the path to the generated CSV report"""
        return self.csv_file


class StepTimer:
    """Helper class to track step timing"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer"""
        self.start_time = datetime.now()
        return self.start_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def stop(self):
        """Stop the timer"""
        self.end_time = datetime.now()
        return self.end_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_duration(self) -> float:
        """Get the duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

