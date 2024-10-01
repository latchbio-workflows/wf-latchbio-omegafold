import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from latch.executions import rename_current_execution
from latch.resources.tasks import small_gpu_task, v100_x1_task
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)


@v100_x1_task
def task(
    run_name: str, input_file: LatchFile, output_directory: LatchOutputDir
) -> LatchOutputDir:
    rename_current_execution(str(run_name))

    print("-" * 60)
    print("Creating local directories")
    local_output_dir = Path(f"/root/outputs/{run_name}")
    local_output_dir.mkdir(parents=True, exist_ok=True)

    print("-" * 60)
    subprocess.run(["nvidia-smi"], check=True)
    subprocess.run(["nvcc", "--version"], check=True)

    # python3.9 -c "import torch; torch.cuda.empty_cache()"

    print("Running OmegaFold")
    # Download precompiled references here in advance

    command_second = [
        "python3.9",
        "/tmp/docker-build/work/OmegaFold/main.py",
        str(input_file.local_path),
        str(local_output_dir),
        # "--model",
        # "2",
    ]

    try:
        subprocess.run(command_second, check=True)
    except Exception as e:
        print("FAILED")
        print(e)
        time.sleep(6000)

    print("Returning results")
    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
