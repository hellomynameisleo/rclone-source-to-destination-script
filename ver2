import os
import subprocess
import datetime
import shutil

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
              "2. Copyto (Append (#) at end of copied files if exist at destination)\n"
              "3. Moveto (Append (#) at end of copied files if exist at destination)\n"
              "4. Copy (Skip all copied files that exist on destination with same name)\n"
              "5. Move (Skip all copied files that exist on destination with same name)")
        move_operation = input("Enter the move operation option (1, 2, 3 etc.): ")
        if move_operation == "1":
            move_operation = "sync"
            break
        elif move_operation == "2":
            move_operation = "copyto"
            break
        elif move_operation == "3":
            move_operation = "moveto"
            break
        elif move_operation == "4":
            move_operation = "copy"
            ignore = "--ignore-existing"
            break
        elif move_operation == "2":
            move_operation = "move"
            ignore = "--ignore-existing"
            break
        else:
            printRed("Invalid input, try again")
    printCyan(f"Selected move operation: {move_operation}")

    while True:
        if move_operation == "copyto" or move_operation == "moveto":
            checksum = None
            break
        checksum = input("Enabled checksum checks? (Y/N): ")
        checksum = checksum.upper()
        if checksum == "Y":
            checksum = "--checksum"
            printCyan("Checksum checks enabled")
            break
        elif checksum == "N":
            printCyan("Checksum checks disabled")
            checksum = None
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

    if move_operation == "copyto" or move_operation == "moveto":
        # Iterate over files in the source directory
        for root, subdirs, files in os.walk(source_path):
            for file in files:
                source_file = os.path.join(root, file)

                # Construct the destination file path
                relative_path = os.path.relpath(root, source_path)
                destination_file = os.path.join(destination_path, relative_path, file)

                # Check if the file already exists in the destination
                counter = 0
                base, ext = os.path.splitext(file)
                while os.path.exists(destination_file):
                    new_filename = f"{base} ({counter}){ext}"
                    destination_file = os.path.join(destination_path, relative_path, new_filename)
                    counter += 1
                printCyan(f"{move_operation} '{source_file}' to '{destination_file}'")
                cmd_args = ["rclone", move_operation, source_file, destination_file, "--metadata", "--progress", "--log-file=" + logPath + f"{move_operation} source to destination - Date=" + formatted_date + " & Time=" + formatted_time + ".log", "--log-level=INFO"]
                try:
                    subprocess.run(cmd_args, check=True)
                except subprocess.CalledProcessError as e:
                    # Check if the error message indicates "directory not found"
                    error_output = str(e.output.decode('utf-8')) if isinstance(e.output, bytes) else str(e)
                    if "returned non-zero exit status" in error_output:
                        printRed(f"Error: {error_output}")
                        if move_operation == "copyto":
                            printYellow(f"Attempting copy fallback with shutil.copy2, can't preserve file creation date.")
                            shutil.copy2(source_file, destination_file)

                            # Check if the file in the destination exists and has the same size as the source file
                            if os.path.exists(destination_file) and os.path.getsize(source_file) == os.path.getsize(destination_file):
                                printGreen(f"File successfully copied and verified in destination.")
                            else:
                                printRed(f"Error: File copy failed or verification failed in destination.")
                                input("Press enter to continue.")
                        if move_operation == "moveto":
                            printYellow(f"Attempting move fallback with shutil.move, can't preserve file date created metadata if moving to different disk.")
                            try:
                                destination_dir = os.path.dirname(destination_file)
                                os.makedirs(destination_dir, exist_ok=True)
                                shutil.move(source_file, destination_file)
                            except Exception as e:
                                printRed(f"Error occured with moving file with shutil.move: {e}")
                                input("Press enter to continue.")
                    else:
                        printRed(f"An error occurred with copying/moving '{source_file}': {error_output}")
                    print("")
    else:
        cmd_args = ["rclone", move_operation, source_path, destination_path, "--metadata", "--progress", "--check-first", "--create-empty-src-dirs", "--transfers=20", "--checkers=20", "--log-file=" + logPath + f"{move_operation} source to destination - Date=" + formatted_date + " & Time=" + formatted_time + ".log", "--log-level=INFO"]
        if checksum:
            cmd_args.append(checksum)
        subprocess.run(cmd_args)

    current_datetime2 = datetime.datetime.now()
    timeTaken = current_datetime2 - current_datetime

    # Get the total seconds elapsed
    total_seconds = timeTaken.total_seconds()

    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Format as HH.MM.SS
    formatted_time = f"Total elapsed time: {int(hours):d}h {int(minutes):d}min {int(seconds):d}s"
    printCyan(formatted_time)
    print("-"*100)
