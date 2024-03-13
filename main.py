# python version 3.8.15
import csv
import time
from disklist import DiskList
import statistics

matri_num = "U2121401C" ## Change accordingly
#matri_num = "A1234013B"
def main():

    years = matri_num[-2]

    if years == '4':
        year1= '201' + years
        year2= '202'+ years
        print("Year 1:",year1)
        print("Year 2:",year2)
    elif years == 5 or years == 6 or years == 7 or years == 8 or years == 9:
        year1='201' + years
        year2 = '201' + years
        #year2= '201'+ last_num
        print("Year 1:",year1)
    else:
        year1='202' + years
        year2 = '202' + years  
      
    month=int(matri_num[-3])
    rangeDict = {
        0: [10, 11, 12],  # October, November, December
        1: [1, 2, 3],     # January, February, March
        2: [2, 3, 4],     # February, March, April
        3: [3, 4, 5],     # March, April, May
        4: [4, 5, 6],     # April, May, June
        5: [5, 6, 7],     # May, June, July
        6: [6, 7, 8],     # June, July, August
        7: [7, 8, 9],     # July, August, September
        8: [8, 9, 10],    # August, September, October
        9: [9, 10, 11]    # September, October, November
    }
    
    # Dictionary Encoding (Data Compression Technique)
    town = int(matri_num[-4])
    townDict = {
        0: "ANG MO KIO",
        1: "BEDOK",
        2: "BUKIT BATOK",
        3: "CLEMENTI",
        4: "CHOA CHU KANG",
        5: "HOUGANG",
        6: "JURONG WEST",
        7: "PUNGGOL",
        8: "WOODLANDS",
        9: "YISHUN"
    }
    location = townDict[town]
    # Instead of storing strings, we store a number. Takes less storage space and a more efficient way of storing categorical data that has a small number of distinct values
    # Whenever the data is read, the numerical codes can be replaced back with the corresponding string values using the dictionary.

    dateColumn = DiskList()
    townColumn = DiskList()
    flat_type_Column = DiskList()
    blockColumn = DiskList()
    street_name_Column = DiskList()
    storey_range_Column = DiskList()
    floor_area_Column = DiskList()
    flat_model_Column = DiskList()
    lease_commence_date_column = DiskList()
    resale_price_column = DiskList()

    # Create Column store
    print("initializing column store...")
    start_time = time.time()

    with open("src/main/resources/ResalePricesSingapore.csv", 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        #sorted_data = sorted(data, key=lambda x: x['month'])
        #for row in sorted_data:
        for row in data:
            dateColumn.append(row['month'])
            townColumn.append(row['town'])
            flat_type_Column.append(row['flat_type'])
            blockColumn.append(row['block'])
            street_name_Column.append(row['street_name'])
            storey_range_Column.append(row['storey_range'])
            floor_area_Column.append(row['floor_area_sqm'])
            flat_model_Column.append(row['flat_model'])
            lease_commence_date_column.append(row['lease_commence_date'])
            resale_price_column.append(row['resale_price'])

    end_time = time.time()
    print(f'column store creation complete in {round(end_time-start_time,4)}s')

    # QUERY PROCESSING
    # Assume memory is able to hold positions
    start_time = time.time()
    count = 0
    position_dict = {}
    
    for i in range(len(dateColumn)):

        date = dateColumn[i]
        date_year, date_month = dateColumn[i].split("-")

        #print(date_month in rangeDict[month])
        # print(date_month)
        #if date[:4] in (year1, year2):  # Filter by year(2003,2013) and month in column store
        #if date_year in (year1, year2) and str(date_month) in str(rangeDict[month]):
        if date_year in (year1, year2) and int(date_month) in rangeDict[month]:
            #if str(date_month) in str(rangeDict[month]): 
            #print(rangeDict[month][j])
                # Filter by location in column store
                if townColumn[i] == location:
                    key = date[0:7]
                    count += 1
                    #print("key: ", key)

                    if key not in position_dict:
                        position_dict[key] = []

                    position_dict[key].append(i)

    area_dict = {}
    price_dict = {}

    # declare outside to get indi month
    # single scan to find statistics for both area and price
    min_area = 1000000000
    min_price = 1000000000
    min_area_list =[]
    min_price_list =[]
    std_price = []
    std_area = []
    sum_area = 0
    sum_price = 0
    for key, positions in position_dict.items():  
        for pos in positions:
            #price query
            curr_price_str = resale_price_column[pos]
            if (curr_price_str == 'M'):
                continue
            #floor area query
            curr_area_str = floor_area_Column[pos]
            if (curr_area_str == 'M'):
                continue

            curr_price = int(curr_price_str)
            sum_price = curr_price + sum_price
            std_price.append(curr_price)

            curr_area = int(curr_area_str)
            sum_area = curr_area + sum_area
            std_area.append(curr_area)

            if curr_price <= min_price:
                min_price_list = []
                min_price = curr_price
                min_price_list.append(pos)
            if curr_area <= min_area:
                min_area_list = []
                min_area = curr_area
                min_area_list.append(pos)
            else:
                #min_price = curr_price
                continue
            # for i in range(len(min_price_list)):
            #     price_dict[dateColumn[min_price_list[i]], 'Min Price'] = min_price
            #     price_dict[dateColumn[min_price_list[i]], 'Average Price'] = sum_price/len(position_dict.get(year_month, []))

        # Min area query
        #for pos in positions:
            # curr_area_str = floor_area_Column[pos]
            # if (curr_area_str == 'M'):
            #     continue
            # curr_area = int(curr_area_str)
            # sum_area = curr_area + sum_area
            # std_area.append(curr_area)
            # #print("curr_area: ", curr_area)    
            # if curr_area <= min_area:
            #     min_area_list = []
            #     min_area = curr_area
            #     min_area_list.append(pos)
            # else:
            #     continue
            # for i in range(len(min_area_list)):
            #     area_dict[dateColumn[min_area_list[i]], 'Min Area'] = min_area
            #     area_dict[dateColumn[min_area_list[i]], 'Average Area'] = sum_area/len(position_dict.get(year_month, []))
         
    for i in range(len(min_price_list)):
            price_dict[dateColumn[min_price_list[i]], 'Min Price'] = min_price
            price_dict[dateColumn[min_price_list[i]], 'Average Price'] = sum_price/count
            price_dict[dateColumn[min_price_list[i]], 'Standard Deviation of Price'] = statistics.stdev(std_price)

    for i in range(len(min_area_list)):
            area_dict[dateColumn[min_area_list[i]], 'Min Area'] = min_area
            area_dict[dateColumn[min_area_list[i]], 'Average Area'] = sum_area/count
            area_dict[dateColumn[min_area_list[i]], 'Standard Deviation of Area'] = statistics.stdev(std_area)

    end_time = time.time()    
    print(f'Time taken for query processing: {round(end_time-start_time,4)}s')

    start_time = time.time()

    with open('ScanResult_' + matri_num + ".csv", 'w', newline='') as f:
        header = ['Year', 'Month', 'town', 'Category', 'Value']
        writer = csv.writer(f)
        writer.writerow(header)
        for key, value in price_dict.items():
            year, date_month = key[0].split('-')
            writer.writerow([year,rangeDict[month][0],location,key[1],value])

        for key, value in area_dict.items():
            year, date_month = key[0].split('-')
            writer.writerow([year,rangeDict[month][0],location,key[1],value])

    end_time = time.time()
    print(f'Time taken for result saving: {round(end_time-start_time,4)}s')


if __name__ == "__main__":
    main()
