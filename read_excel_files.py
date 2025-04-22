import pandas as pd
import os

def read_excel_file(file_path, output_dir):
    # Get the file name without extension
    file_name = os.path.basename(file_path).split('.')[0]
    output_file = os.path.join(output_dir, f"{file_name}_analysis.txt")
    
    # Open a file to write the output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Reading: {file_path}\n")
        f.write("-" * 80 + "\n")
        
        # Read all sheets in the Excel file
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        f.write(f"The file contains {len(sheet_names)} sheet(s): {sheet_names}\n\n")
        
        # Read each sheet and display its content
        for sheet_name in sheet_names:
            f.write(f"Sheet: {sheet_name}\n")
            f.write("-" * 40 + "\n")
            
            # Read the sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Display basic info
            f.write(f"Dimensions: {df.shape[0]} rows × {df.shape[1]} columns\n")
            f.write(f"Column names: {list(df.columns)}\n\n")
            
            # Save the data to a CSV file for easier viewing
            csv_file = os.path.join(output_dir, f"{file_name}_{sheet_name}.csv")
            df.to_csv(csv_file, index=False)
            f.write(f"Saved sheet data to: {csv_file}\n")
            
            # Display first 5 rows of data
            f.write("First 5 rows:\n")
            f.write(df.head().to_string() + "\n\n")
            
            # Display basic statistics for numeric columns
            if len(df.select_dtypes(include=['number']).columns) > 0:
                f.write("Basic statistics for numeric columns:\n")
                f.write(df.describe().to_string() + "\n\n")
            
            f.write("-" * 40 + "\n\n")
    
    print(f"Analysis for {file_name} saved to {output_file}")
    print(f"CSV files for each sheet saved in {output_dir}")

# Main execution
if __name__ == "__main__":
    files = [
        r"f:\Projects\Excel Automation\Cycle 1 LNC Implementation  Analysis January 25.xlsx",
        r"f:\Projects\Excel Automation\LNC Implementation Comparison Graph January 25.xlsx"
    ]
    
    # Create output directory
    output_dir = r"f:\Projects\Excel Automation\excel_analysis_output"
    os.makedirs(output_dir, exist_ok=True)
    
    for file_path in files:
        try:
            read_excel_file(file_path, output_dir)
            print("-" * 50)
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
