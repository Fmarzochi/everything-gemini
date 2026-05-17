import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from execution.tool_runner import run_command

async def test_tool_runner():
    print("--- Running Tests ---")
    
    # 1. Valid command
    res1 = await run_command(["python3", "--version"])
    print(f"Test 1 (Valid): {'PASS' if res1.returncode == 0 else 'FAIL'} (stdout: {res1.stdout[:10]}...)")
    
    # 2. Blocked command
    res2 = await run_command(["rm", "-rf", "/"])
    print(f"Test 2 (Blocked): {'PASS' if res2.returncode == 1 else 'FAIL'} (stderr: {res2.stderr})")
    
    # 3. Timeout
    res3 = await run_command(["python3", "-c", "import time; time.sleep(2)"], timeout=1)
    print(f"Test 3 (Timeout): {'PASS' if res3.timed_out else 'FAIL'}")

if __name__ == "__main__":
    asyncio.run(test_tool_runner())
