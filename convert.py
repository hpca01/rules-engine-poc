import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    f = Path('log.txt')
    df = pd.read_csv(f)
    columns = ['log_time', 'millisec', 'type', 'ct_deque', 'time_due', 'insert_time', 'simul_tasks']
    df.columns = columns
    print(df[df.ct_deque - df.time_due > 0])
    df.sort_values(['ct_deque', 'time_due'], ascending=True,inplace=True)
    df.to_csv('test.csv', index=False)
    print(df.shape)