import pandas as pd
from typing import List, Tuple, Optional
from pathlib import Path


class ExcelParser:
    """Parser for Excel files using pandas"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None
        self.sheet_names: List[str] = []
        self._load_file()
    
    def _load_file(self):
        """Load Excel file"""
        try:
            # Get all sheet names
            excel_file = pd.ExcelFile(self.file_path)
            self.sheet_names = excel_file.sheet_names
            
            # Load first sheet by default
            if self.sheet_names:
                self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_names[0])
        except Exception as e:
            raise ValueError(f"Failed to load Excel file: {str(e)}")
    
    def get_sheet_names(self) -> List[str]:
        """Get list of sheet names"""
        return self.sheet_names
    
    def load_sheet(self, sheet_name: str):
        """Load a specific sheet"""
        try:
            self.df = pd.read_excel(self.file_path, sheet_name=sheet_name)
        except Exception as e:
            raise ValueError(f"Failed to load sheet '{sheet_name}': {str(e)}")
    
    def get_dimensions(self) -> Tuple[int, int]:
        """Get row and column count"""
        if self.df is None:
            return 0, 0
        return len(self.df), len(self.df.columns)
    
    def get_column_data(self, column_index: int) -> List[str]:
        """Get data from a specific column"""
        if self.df is None:
            raise ValueError("No data loaded")
        
        if column_index < 0 or column_index >= len(self.df.columns):
            raise ValueError(f"Column index {column_index} out of range")
        
        # Get column data and convert to strings
        column = self.df.iloc[:, column_index]
        
        # Convert to string, handling NaN values
        data = []
        for value in column:
            if pd.isna(value):
                data.append("")
            else:
                data.append(str(value))
        
        return data
    
    def get_column_by_name(self, column_name: str) -> List[str]:
        """Get data from a column by name"""
        if self.df is None:
            raise ValueError("No data loaded")
        
        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        
        column = self.df[column_name]
        
        data = []
        for value in column:
            if pd.isna(value):
                data.append("")
            else:
                data.append(str(value))
        
        return data
    
    def get_all_data(self) -> List[List[str]]:
        """Get all data as list of rows"""
        if self.df is None:
            raise ValueError("No data loaded")
        
        data = []
        for _, row in self.df.iterrows():
            row_data = []
            for value in row:
                if pd.isna(value):
                    row_data.append("")
                else:
                    row_data.append(str(value))
            data.append(row_data)
        
        return data
    
    def get_column_names(self) -> List[str]:
        """Get column names"""
        if self.df is None:
            return []
        return list(self.df.columns)
