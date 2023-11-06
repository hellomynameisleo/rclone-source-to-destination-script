import os
import subprocess
import datetime

def printRed(skk):
    print("\033[91m{}\033[00m".format(skk))
def printGreen(skk):
    print("\033[92m{}\033[00m".format(skk))
def printYellow(skk):
    print("\033[93m{}\033[00m".format(skk))
def printCyan(skk):
    print("\033[96m{}\033[00m".format(skk))

logPath = "PathToLogFile/Logs/"

while True:
    # Set move operation
    ignore = None
    while True:
        print("1. Sync\n"
              "2. Copy\n"
              "3. Move")
        move_operation = input("Enter the move operation (1, 2, or 3): ")
        if move_operation == "1":
            move_operation = "sync"
            break
        elif move_operation == "2":
            move_operation = "copy"
            ignore = "--ignore-existing"
            break
        elif move_operation == "3":
            move_operation = "move"
            break
        else:
            printRed("Invalid input, try again")
    printCyan(f"Selected move operation: {move_operation}")

    while True:
        checksum = input("Enabled checksum checks? (Y/N): ")
        checksum = checksum.upper()
        if checksum == "Y":
            checksum = "--checksum"
            printCyan("Checksum checks enabled")
            break
        elif checksum == "N":
            checksum = None
            printCyan("Checksum checks disabled")
            break
        else:
            printRed("Invalid input, try again")

    while True:
        # Set source path
        while True:
            source_path = input("Enter the source directory path: ")
            source_path = source_path.replace('"',"")
            if os.path.isdir(source_path):
                printCyan(f"Selected source path: {source_path}")
                break
            else:
                printRed("Directory path not found, try again")

        # Set destination path
        while True:
            destination_path = input("Enter the destination directory path: ")
            destination_path = destination_path.replace('"',"")
            if os.path.isdir(destination_path):
                printCyan(f"Selected destination path: {destination_path}")
                break
            else:
                printRed("Directory path not found, try again")
        
        if source_path == destination_path:
            printRed(f"Source and destination path cannot be the same")
        else:
            break
    
    input("Press any key to continue move operation")

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date as YYYY-MM-DD
    formatted_date = current_datetime.strftime('%Y-%m-%d')

    # Format the time as HH.mm.ss
    formatted_time = current_datetime.strftime('%H.%M.%S')

    cmd_args = ["rclone", move_operation, source_path, destination_path, "--progress", "--check-first", "--create-empty-src-dirs", "--transfers=20", "--checkers=20", "--log-file=" + logPath + "Copy source to destination - Date=" + formatted_date + " & Time=" + formatted_time + ".log", "--log-level=INFO"]
    if checksum:
        cmd_args.append(checksum)
    if ignore:
        cmd_args.append(ignore)
    subprocess.run(cmd_args)

    print("-"*100)
