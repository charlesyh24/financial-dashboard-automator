import argparse
import pandas as pd
from postman_crawler import wholeState


def get_parser():
    """Get arguments from users"""
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--industry', required=True)
    parser.add_argument('-c', '--company', required=True, type=int, nargs='+')
    parser.add_argument('-y', '--year', required=True, type=int, help='2017~2021')
    parser.add_argument('-q', '--quarter', required=True)
    parser.add_argument('-e', '--email', required=True)
    
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    industry = args.industry
    companies = args.company
    year = args.year
    quarter = args.quarter
    email = args.email

    df_IS = wholeState(companies, 'IS_M_QUAR')
    df_BS = wholeState(companies, 'BS_M_QUAR')
#    df_IS.to_excel('df_IS.xlsx')
#    df_BS.to_excel('df_BS.xlsx')