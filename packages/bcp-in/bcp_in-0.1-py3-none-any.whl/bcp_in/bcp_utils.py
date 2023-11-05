import subprocess
import logging

logger = logging.getLogger(__name__)

def is_bcp_available():
    """Check if bcp is available."""
    try:
        result = subprocess.run(['bcp', '-v'], capture_output=True, text=True)
        if 'SQL Server' in result.stdout:
            return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking bcp availability: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False

def run_bcp_command(bcp_command):
    """Run a bcp command and return the output or error message."""
    logger.info(f"Running bcp command: {' '.join(bcp_command)}")
    try:
        result = subprocess.run(bcp_command, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running bcp: {e}")
        return e.stderr
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return str(e)

def truncate_table(server, database, schema, table):
    """Truncate a table using a bcp command."""
    query = f"TRUNCATE TABLE {schema}.{table}"
    bcp_command = [
        'bcp',
        query,
        'queryout',
        '/dev/null',
        '-S', server,
        '-d', database,
        '-T',
        '-c'
    ]
    return run_bcp_command(bcp_command)

def load_data_using_bcp(filename, server, database, schema, table, delimiter, truncate=False):
    """Load data into a table using a bcp command."""
    if truncate:
        truncate_table(server, database, schema, table)
    
    query = f"{schema}.{table}"
    bcp_command = [
        'bcp',
        query,
        'in',
        filename,
        '-S', server,
        '-d', database,
        '-T',
        '-c',
        '-t', delimiter
    ]
    return run_bcp_command(bcp_command)