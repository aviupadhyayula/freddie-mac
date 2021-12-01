import csv

initials = [["AL", "Alabama"], ["AK", "Alaska"], ["AZ", "Arizona"], ["CA", "California"], 
            ["CO", "Colorado"], ["CT", "Connecticut"], ["DE", "Delaware"], ["D.C", "District of Columnia"],
            ["FL", "Florida"], ["GA", "Georgia"], ["HI", "Hawaii"], ["ID", "Idaho"],
            ["IL", "Illinois"], ["IN", "Indiana"], ["IA", "Iowa"], ["KS", "Kansas"],
            ["KY", "Kentucky"], ["LA", "Louisiana"], ["ME", "Maine"], ["MD", "Maryland"],
            ["MA", "Massachusetts"], ["MI", "Michigan"], ["MN", "Minnesota"], 
            ["MS", "Mississippi"], ["MO", "Missouri"], ["MT", "Montana"], ["NE", "Nebraska"],
            ["NV", "Nevada"], ["NH", "New Hampshire"], ["NJ", "New Jersey"], ["NM", "New Mexico"], 
            ["NY", "New York"], ["NC", "North Carolina"], ["ND", "North Dakota"], ["OH", "Ohio"], 
            ["OK", "Oklahoma"], ["OR", "Oregon"], ["PA", "Pennsylvania"], ["PR", "Puerto Rico"], 
            ["RI", "Rhode Island"], ["SC", "South Carolina"], ["SD", "South Dakota"], 
            ["TN", "Tennessee"], ["TX", "Texas"], ["UT", "Utah"], ["VT", "Vermont"], 
            ["VA", "Virginia"], ["WA", "Washington"], ["WV", "West Virginia"], ["WI", "Wisconsin"],
            ["WY", "Wyoming"]]

def parse(csv_name):
    with open(csv_name, "r") as f:
        entries = f.readlines()
    for i in range(0, len(entries)):
        entries[i] = entries[i].replace("\n", "")
        entries[i] = entries[i].split(",")
    count = 0
    with open(csv_name, "w") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for state in initials:
            collection = []
            for entry in entries:
                if state[0] == entry[0] or state[1] == entry[0]:
                    try:
                        collection.append([state[0], entry[1], entry[2], entry[3]])
                    except IndexError:
                        print(entry)
            sorted(collection, key=lambda x : x[1])
            for entry in collection:
                count += 1
                writer.writerow(entry)
    print(str(count) + '/' + str(len(entries)) + ' entries parsed')

if __name__ == '__main__':
    target = input("File you'd like to parse: ")
    parse(target)