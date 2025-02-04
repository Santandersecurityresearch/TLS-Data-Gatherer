import csv
import re
import utils

# Stage 1: .csv fix

# All rows captured by the csv_reader will be analysed
# row[0] = "Host IP"
# row[1] = "DNS Hostname"
# row[2] = "NetBIOS Hostname"
# row[3] = "Tracking Method"
# row[4] = "Operating System"
# row[5] = "OS CPE"
# row[6] = "NETWORK"
# row[7] = "Last Scan Date"
# row[8] = "Evaluation Date"
# row[9] = "Control ID"
# row[10] =  "Technology"
# row[11] = "Control"
# row[12] = "Criticality Label"
# row[13] = "Criticality Value"
# row[14] = "Instance"
# row[15] = "Rationale"
# row[16] = "Status"
# row[17] = "Remediation"
# row[18] = "Deprecated"
# row[19] = "Evidence"

# The following rows are removed:
# row[20] = "Exception Assignee"
# row[21] = "Exception Status"
# row[22] = "Exception End Date"
# row[23] = "Exception Creator"
# row[24] = "Exception Created Date"
# row[25] = "Exception Modifier"
# row[26] = "Exception Modified Date"
# row[27] = "Exception Comments History"
# row[28] = "Qualys Host ID"

# And the following are added:
# row[20]="Expected Value(s)"
# row[21]="Current Value(s)"
# row[22]="Extended Evidence(s)"
# row[23] = "Qualys Host ID"

# 1. Find the header for the DataFrame
# 2. Column headers are redistributed to accomodate change
# 3. Split data on the Evidence column (three new categories needed)
#    Split: [x[0], None, x[2]] = y[0]; [y[0], None, y[2]] = z[0]; [z[0], None, z[2]] = row[19]
#    Information: row[19] = [[[ x[0], None, x[2] ], None, y[2] ], None, z[2] ]
#    We extract x[2], y[2], z[2] - which correspond to "Expected Value(s)", "Current Value(s)" & "Extended Evidence(s)", respectively.
def process_row(row, dataframe_start_check):
    if row[0] == "Host IP": # bypass first rows (headers)
        row[20] = "Expected Value(s)"
        row[21] = "Current Value(s)"
        row[22] = "Extended Evidence(s)"
        dataframe_start_check = True
    elif dataframe_start_check:
        z = re.split(r'======Extended Evidence(\(s\))*======:', row[19])
        y = re.split(r'======Current Value\(s\) - Last updated:(.)*======', z[0])
        x = re.split(r'======Expected Value(\(s\))*======', y[0])
        # Separations are concatenated onto their proper columns
        row[19] = x[0]
        row[20] = x[2]
        # Replacement of ";" for ":" in columns 21 and 22 due to issues with .csv compatibility in Excel
        row[21] = y[2].replace(";", ":")
        if len(z) > 1:
            row[22] = z[2][:(len(z[2]) - 1)].replace(";", ":")
        row[23] = row[28]
        # Preserve only until row[23]
        row_clear = [ele.replace("\n", " ") for ele in row[:24]]
        return row_clear, dataframe_start_check
    return row, dataframe_start_check

# Runs stage 1
# Output: "[original_csv_filename]_Stage1_csvCleanse.csv"
def run_stage1(original_csv_filename:str, tech:str):
    try:
        with open(original_csv_filename, 'r') as csv_file, open(utils.get_filename_stage(1, original_csv_filename), 'w', newline='') as csv_file_new:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(csv_file_new, delimiter=',')
            dataframe_start_check = False
            for row in csv_reader:
                row_clear, dataframe_start_check = process_row(row, dataframe_start_check)
                if dataframe_start_check:
                    csv_writer.writerow(row_clear)
    except Exception as e:
        raise Exception(f"Error on stage 1: {str(e)}")