import argparse
import asyncio
import logging
import subprocess
import threading
import time

from package.IO_module import setCPU, setUp, cleanUp
from package.prisma_module import *

def main():
    parser = argparse.ArgumentParser(description="Python client for Ivette Computational chemistry and Bioinformatics project")
    parser.add_argument("username", help="username", nargs='?', default='guest')

    args = parser.parse_args() # Theses args can be used anywhere

    # Info disabling
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    logging.getLogger("aiohttp").setLevel(logging.CRITICAL)

    validated_input = setCPU()

    # Loop over to run the queue
    while True:
        # Download the job
        id = asyncio.run(retrieveQID())
        setUp()
        downloadApi(id)

        # Define the command as a list of arguments
        # Use the relative or absolute path to the input file in the subdirectory
        # Replace "subdirectory" and "input" with the actual subdirectory and file names
        command = ["rungms tmp/" + id + " 00 " +
                str(validated_input)]  # The last one is ncores

        # Create a flag to signal when the job is done
        job_done = False

        # Function to run the 'rungms' command and update the job_done flag

        def run_rungms():
            global job_done
            with open("tmp/output.log", "w") as output_file:
                try:
                    # Run the 'rungms' command and wait for it to complete
                    subprocess.run(
                        command,
                        stdout=output_file,
                        stderr=subprocess.STDOUT,
                        shell=True,
                        check=True  # This will raise an error if the command returns a non-zero exit code
                    )
                    asyncio.run(upsertQState(id))
                    asyncio.run(insertCalculation('output.log'))
                    job_done = True
                except subprocess.CalledProcessError as e:
                    if not e.returncode == -2:
                        asyncio.run(upsertQState(id, 'failed'))
                        asyncio.run(insertCalculation('output.log'))
                    cleanUp(id)
                    print(f"\n Command failed with exit code {e.returncode}.")
                    job_done = True

        # Create a thread to run the 'rungms' command
        rungms_thread = threading.Thread(target=run_rungms)

        # Create an animated "Waiting" message using Braille characters
        waiting_message = "⣾⣷⣯⣟⡿⢿⣻⣽"  # Customize this as needed

        try:
            asyncio.run(upsertQState(id, 'in progress'))
            print('Running Gamess Job')
            rungms_thread.start()  # Start the 'rungms' command thread
            while not job_done:
                for braille_char in waiting_message:
                    print(braille_char, end='\r', flush=True)
                    time.sleep(0.1)
            print("\nWaiting for 'rungms' job to complete...")
            rungms_thread.join()  # Wait for the 'rungms' command thread to finish
            cleanUp(id)
            print("Job completed successfully.")
        except KeyboardInterrupt:
            if __name__ == '__main__':
                asyncio.run(upsertQState(id, 'interrupted'))
            cleanUp(id)
            print("Job interrupted.")
            raise SystemExit


if __name__ == "__main__":
    main()
