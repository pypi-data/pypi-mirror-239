from prisma import Prisma
import time
from .supabase_module import *


async def insertCalculation(name: str, description='', status='finished', bucketDir='Calculations/') -> None:
    """
    Insert a calculation record into a database using Prisma and upload related files to a specified bucket directory.

    Args:
        name (str): The name of the calculation.
        description (str, optional): A description of the calculation (default is an empty string).
        status (str, optional): The status of the calculation (default is 'finished').
        bucketDir (str, optional): The directory in the storage bucket where related files will be stored (default is 'Calculations/').

    Returns:
        None

    Note:
    - This function is designed to work with the Prisma ORM for database interactions.
    - You should have a Prisma instance set up with appropriate models and a connection to the database.
    - The function uses an asynchronous design ('async') and should be awaited when called.
    - The 'uploadFile' function is assumed to be defined elsewhere in your code.

    Example Usage:
    await insertCalculation('Calculation 1', 'Description of calculation', 'in progress', 'CustomDir/')

    Details:
    - This function inserts a calculation record into a database using Prisma, a popular ORM (Object-Relational Mapping) tool.
    - The calculation's 'name', 'description', 'status', and 'bucketDir' are specified as function arguments.
    - By default, the 'description' is an empty string, 'status' is set to 'finished', and 'bucketDir' is 'Calculations/'.
    - The 'await' keyword is used since this function likely involves asynchronous database operations.
    - The 'uploadFile' function is expected to be defined elsewhere in your code for handling file uploads.
    - The function creates a Prisma instance, connects to the database, inserts a calculation record, and uploads related files.
    - It then disconnects from the database using Prisma to complete the database operation.
    """
    # Create a Prisma instance for database interactions
    prisma = Prisma()

    # Establish a database connection using Prisma
    await prisma.connect()

    # Create a new calculation record in the database
    calc = await prisma.calculations.create(
        data={
            "name": name,
            "description": description,
            "status": status,
            "bucketPath": bucketDir
        },
    )

    # Update the 'bucketPath' with the calculation's ID as part of the path
    calc = await prisma.calculations.update(
        where={
            'id': calc.id,
        },
        data={
            "bucketPath": bucketDir + calc.id
        },
    )

    # Upload related files to the specified bucket directory using 'uploadFile'
    uploadFile(name, calc.id, bucketDir)

    # Disconnect from the database using Prisma
    await prisma.disconnect()


async def insertJob(name: str, description='', status='pending', user='guest', bucketDir='JobQueue/') -> None:
    """
    Insert a job record into a database using Prisma and upload related files to a specified bucket directory.

    Args:
        name (str): The name of the job.
        description (str, optional): A description of the job (default is an empty string).
        status (str, optional): The status of the job (default is 'pending').
        user (str, optional): The user associated with the job (default is 'guest').
        bucketDir (str, optional): The directory in the storage bucket where related files will be stored (default is 'JobQueue/').

    Returns:
        None

    Note:
    - This function is designed to work with the Prisma ORM for database interactions.
    - You should have a Prisma instance set up with appropriate models and a connection to the database.
    - The function uses an asynchronous design ('async') and should be awaited when called.
    - The 'uploadFile' function is assumed to be defined elsewhere in your code.

    Example Usage:
    await insertJob('Job 1', 'Description of the job', 'in progress', 'john_doe', 'CustomJobDir/')

    Details:
    - This function inserts a job record into a database using Prisma, a popular ORM (Object-Relational Mapping) tool.
    - The job's 'name', 'description', 'status', 'user', and 'bucketDir' are specified as function arguments.
    - By default, the 'description' is an empty string, 'status' is set to 'pending', 'user' is 'guest', and 'bucketDir' is 'JobQueue/'.
    - The 'await' keyword is used since this function likely involves asynchronous database operations.
    - The 'uploadFile' function is expected to be defined elsewhere in your code for handling file uploads.
    - The function creates a Prisma instance, connects to the database, inserts a job record, and uploads related files.
    - It then disconnects from the database using Prisma to complete the database operation.
    """
    # Documentation update due
    prisma = Prisma()

    # Establish a database connection using Prisma
    await prisma.connect()

    # Create a new job record in the database
    job = await prisma.jobqueue.create(
        data={
            "name": name,
            "description": description,
            "status": status,
            "user": user,
            "inputPath": bucketDir + name
        },
    )

    # Upload related files to the specified bucket directory using 'uploadFile'
    uploadFile(name, job.id, bucketDir)

    # Disconnect from the database using Prisma
    await prisma.disconnect()


async def retrieveQID():
    """
    Retrieve the ID of the next pending job in the job queue from the database using Prisma.

    Returns:
        int: The ID of the next pending job.

    Raises:
        SystemExit: Raised when there are no pending jobs in the queue.

    Note:
    - This function is designed to work with the Prisma ORM for database interactions.
    - You should have a Prisma instance set up with appropriate models and a connection to the database.
    - The function uses an asynchronous design ('async') and should be awaited when called.

    Example Usage:
    qid = await retrieveQID()

    Details:
    - This function retrieves the ID of the next pending job in the job queue from the database using Prisma, an ORM
      (Object-Relational Mapping) tool.
    - The function creates a Prisma instance, connects to the database, queries the database for the next pending job,
      and disconnects from the database after the query is executed.
    - If there are no pending jobs in the queue, the function raises a 'SystemExit' exception with an informative
      error message.
    - The retrieved job ID is returned for further processing.
    """
    # Documentation update required
    try:
        while True:
            # Your code here
            prisma = Prisma()

            # Establish a database connection using Prisma
            await prisma.connect()

            # Query the database to find the next pending job
            job = await prisma.jobqueue.find_first(
                where={
                    'status': {
                        'in': ['pending', 'interrupted'],
                    }
                },
            )

            # Disconnect from the database using Prisma
            await prisma.disconnect()

            # Check if a pending job was found or not
            if job is None:
                interval = 30  # Set the countdown interval to 5 seconds
                print("\nCurrently all jobs are finished/running. Checking up the queue again when the timer is over.")
                print("Press Ctrl+C to interrupt the loop.")
                for remaining in range(interval, 0, -1):
                    print(f"{remaining} seconds", end='\r')
                    time.sleep(1)
                print(" " * 30, end='\r')  # Clear the countdown timer
            else:
                return job.id
    except KeyboardInterrupt:
        print("Loop interrupted by the user.")


async def upsertQState(id: str, status='done'):
    """
    Update or insert the status of a job in the job queue within the database using Prisma.

    Args:
        id (str): The unique identifier of the job.
        status (str, optional): The status to set for the job (default is 'done').

    Returns:
        None

    Note:
    - This function is designed to work with the Prisma ORM for database interactions.
    - You should have a Prisma instance set up with appropriate models and a connection to the database.
    - The function uses an asynchronous design ('async') and should be awaited when called.

    Example Usage:
    await upsertQState('12345', 'in progress')

    Details:
    - This function updates or inserts the status of a job in the job queue within the database using Prisma, an ORM
      (Object-Relational Mapping) tool.
    - The 'id' argument specifies the unique identifier of the job to be updated.
    - The 'status' argument (defaulting to 'done') is used to set the new status for the job.
    - The function creates a Prisma instance, connects to the database, updates the job's status, and disconnects
      from the database after the operation is completed.
    - The function can be used to both update an existing job's status or insert a new job with the specified status.
    """
    prisma = Prisma()

    # Establish a database connection using Prisma
    await prisma.connect()

    # Update or insert the job's status in the database
    job = await prisma.jobqueue.update(
        where={
            'id': id,
        },
        data={
            'status': status
        },
    )

    # Disconnect from the database using Prisma
    await prisma.disconnect()
