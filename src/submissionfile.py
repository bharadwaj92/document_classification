import csv
import io
with io.open('results.csv', 'w' ,encoding = 'utf-8' , errors = 'ignore' ) as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["id","tags"])
    with open('result_mp1.csv', encoding = 'utf-8') as f:
        reader= csv.reader(f)
        for row in reader:
            if(bool(row)):
                print(row[1])
            
        

    