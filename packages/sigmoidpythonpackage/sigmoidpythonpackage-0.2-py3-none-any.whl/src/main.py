from my_package.logic import load_file_to_dataframe

if __name__ == "__main__":
    # Load a CSV file
    csv_df = load_file_to_dataframe("your_data.csv", file_format="csv")
    print("Loaded CSV file:")
    print(csv_df)

    # Load an Excel file
    excel_df = load_file_to_dataframe("your_data.xlsx", file_format="excel")
    print("Loaded Excel file:")
    print(excel_df)
