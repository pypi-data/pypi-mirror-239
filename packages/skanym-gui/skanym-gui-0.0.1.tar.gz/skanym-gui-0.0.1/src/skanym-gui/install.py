import os

if __name__ == "__main__":
    # Check if the GeeXLab executable is in the current directory
    if not os.path.exists("geexlab.exe"):
        print("Error: cannot find GeeXLab executable!")
        exit(1)
    
    # Copy the content from this package to the current directory (except the GeeXLab executable)
    # Use powershell on Windows and bash on Linux
    
    # TODO

    

    