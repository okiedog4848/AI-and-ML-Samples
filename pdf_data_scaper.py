import pdfplumber
import pandas as pd
from typing import Optional


class PDFDataScraper:
    def __init__(self, pdf_path: str):
        """
        Initialize the PDFDataScraper with the path to the PDF file.

        Args:
            pdf_path (str): Path to the PDF file to be scraped.
        """
        self.pdf_path = pdf_path
        self.data = []

    def extract_text(self) -> None:
        """
        Extract text from the PDF file using pdfplumber.
        Stores extracted data in self.data.
        """
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    # Extract text from each page
                    text = page.extract_text()
                    if text:
                        # Split text into lines and store
                        lines = text.split('\n')
                        self.data.extend(lines)
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")

    def extract_tables(self) -> list:
        """
        Extract tables from the PDF file using pdfplumber.

        Returns:
            list: List of tables extracted from the PDF.
        """
        tables = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    # Extract tables from each page
                    page_tables = page.extract_tables()
                    tables.extend(page_tables)
        except Exception as e:
            print(f"Error extracting tables: {str(e)}")
        return tables

    def create_dataframe(self, table_index: Optional[int] = None) -> pd.DataFrame:
        """
        Create a pandas DataFrame from extracted data.
        If table_index is provided, uses the specified table; otherwise, uses text data.

        Args:
            table_index (Optional[int]): Index of the table to convert to DataFrame.
                                        If None, uses text data.

        Returns:
            pd.DataFrame: DataFrame containing the scraped data.
        """
        if table_index is not None:
            # Use specified table
            tables = self.extract_tables()
            if table_index < len(tables) and tables[table_index]:
                try:
                    df = pd.DataFrame(tables[table_index][1:], columns=tables[table_index][0])
                    return df
                except Exception as e:
                    print(f"Error creating DataFrame from table: {str(e)}")
                    return pd.DataFrame()
            else:
                print(f"No table found at index {table_index}")
                return pd.DataFrame()
        else:
            # Use extracted text data
            if not self.data:
                self.extract_text()
            try:
                # Assume data is space-separated or can be split into columns
                processed_data = [line.split() for line in self.data if line.strip()]
                # Filter out empty lists and ensure consistent column length
                max_cols = max(len(row) for row in processed_data) if processed_data else 1
                # Pad rows with fewer columns
                processed_data = [row + [''] * (max_cols - len(row)) for row in processed_data]
                # Create DataFrame with generic column names
                columns = [f"Column_{i + 1}" for i in range(max_cols)]
                df = pd.DataFrame(processed_data, columns=columns)
                return df
            except Exception as e:
                print(f"Error creating DataFrame from text: {str(e)}")
                return pd.DataFrame()

    def save_dataframe(self, df: pd.DataFrame, output_path: str) -> None:
        """
        Save the DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): DataFrame to save.
            output_path (str): Path to save the CSV file.
        """
        try:
            df.to_csv(output_path, index=False)
            print(f"DataFrame saved to {output_path}")
        except Exception as e:
            print(f"Error saving DataFrame: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Replace 'input.pdf' with your PDF file path
    scraper = PDFDataScraper('C:/daddison/pdf/f455213a-e909-4a53-85ca-89d0515a7779.pdf')

    # Extract data and create DataFrame from text
    df_text = scraper.create_dataframe()
    if not df_text.empty:
        scraper.save_dataframe(df_text, 'output_text.csv')

    # Extract data and create DataFrame from the first table (if any)
    df_table = scraper.create_dataframe(table_index=0)
    if not df_table.empty:
        scraper.save_dataframe(df_table, 'output_table.csv')