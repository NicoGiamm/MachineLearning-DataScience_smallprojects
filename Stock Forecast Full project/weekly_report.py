import pandas as pd
import sys
sys.path.insert(1, './utils/')
from Functions import report_stats

def main():
    
    filename = 'weekly_report.csv'
    report = pd.read_csv(filename, parse_dates=True, index_col='date')
    report_stats(report)
    
main()