import csv
import pandas as pd


# with open('../images/images.csv', 'w') as f:
#     writer = csv.writer(f, delimiter=' ')
#     writer.writerow(['id', 'name', 'age'])
    # writer.writerow(['10001', 'Mike', 20])
    # writer.writerow(['10002', 'Bob', 22])
    # writer.writerow(['10003', 'Jordan', 21])

    # writer.writerows([['10001', 'Mike', 20], ['10002', 'Bob', 22], ['10003', 'Jordan', 21]])


# with open('../images/images.csv', 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in f:
#         print(row)

df = pd.read_csv('../images/images.csv')
print(df)





