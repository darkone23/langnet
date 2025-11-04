#!/usr/bin/env python3

import asyncio
import os
import sys

from sh import bash

# --- Configuration ---
SLEEP_DURATION = 3600  # 1 hour (3600 seconds)
# --- End Configuration ---


def find_zombie_ppid() -> int | None:
    """
    Finds the Parent PID (PPID) of the first 'perl <defunct>' process.
    """
    # This command finds the PPID, STAT, and COMMAND
    # Then awk filters for lines where STAT is 'Z' (Zombie)
    # and COMMAND is 'perl', printing the PPID and exiting.
    cmd = 'ps -eo ppid,stat,comm | awk \'$2=="Z" && $3=="perl" {print $1; exit}\''
    ppid_str = bash("-c", cmd).strip()

    if ppid_str.isdigit():
        return int(ppid_str)

    return None


def kill_process(pid: int):
    """
    Sends a SIGTERM signal to the given PID.
    """
    try:
        # os.kill is a simple, direct system call.
        # It's synchronous, but so fast it doesn't matter.
        os.kill(pid, 15)  # 15 = SIGTERM
        print(f"Zombie Killer: Sent KILL signal to parent process {pid}.")
    except ProcessLookupError:
        print(f"Zombie Killer: Process {pid} no longer exists.", file=sys.stderr)
    except PermissionError:
        print(f"Zombie Killer: Permission denied to kill {pid}.", file=sys.stderr)
    except Exception as e:
        print(f"Zombie Killer: Failed to kill {pid}: {e}", file=sys.stderr)


async def main_loop():
    """
    Main service loop.
    """
    print(f"Zombie Killer: Service started. Will check every {SLEEP_DURATION}s.")
    while True:
        ppid = find_zombie_ppid()

        if ppid:
            print(f"Zombie Killer: Found perl zombie parent at PID {ppid}.")
            kill_process(ppid)
        else:
            print("Zombie Killer: No perl zombies found.")

        print(f"Zombie Killer: Sleeping for {SLEEP_DURATION} seconds...")
        await asyncio.sleep(SLEEP_DURATION)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nZombie Killer: Shutting down...")
