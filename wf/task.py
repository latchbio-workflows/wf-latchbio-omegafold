import subprocess
import sys
from pathlib import Path
from typing import Optional

from latch.executions import rename_current_execution
from latch.functions.messages import message
from latch.resources.tasks import small_gpu_task, v100_x1_task
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile

sys.stdout.reconfigure(line_buffering=True)


@v100_x1_task
def omegafold_task(
    run_name: str,
    input_fasta: LatchFile,
    output_directory: LatchOutputDir,
    num_cycle: int = 10,
    subbatch_size: Optional[int] = None,
    weights_file: Optional[str] = None,
    weights: Optional[str] = None,
    model: int = 1,
    pseudo_msa_mask_rate: float = 0.15,
    num_pseudo_msa: int = 15,
    allow_tf32: bool = True,
) -> LatchOutputDir:
    rename_current_execution(str(run_name))

    print("-" * 60)
    print("Creating local directories")
    local_output_dir = Path(f"/root/outputs/{run_name}")
    local_output_dir.mkdir(parents=True, exist_ok=True)

    print("-" * 60)
    subprocess.run(["nvidia-smi"], check=True)
    subprocess.run(["nvcc", "--version"], check=True)

    print("-" * 60)
    print("Running OmegaFold")
    command = [
        "python3.9",
        "/tmp/docker-build/work/OmegaFold/main.py",
        str(input_fasta.local_path),
        str(local_output_dir),
    ]

    if weights_file is not None:
        command.extend(["--weights_file", weights_file])
    elif weights is not None:
        command.extend(["--weights", weights])
    else:
        print("-" * 60)
        print("Downloading model")
        model_path = Path(
            LatchFile(
                f"s3://latch-public/proteinengineering/omegafold/model{'' if model == 1 else '2'}.pt"
            ).local_path
        )
        root_model_path = Path("/root") / model_path.name
        model_path.rename(root_model_path)
        command.extend(["--weights_file", str(root_model_path)])

    if num_cycle != 10:
        command.extend(["--num_cycle", str(num_cycle)])
    if subbatch_size is not None:
        command.extend(["--subbatch_size", str(subbatch_size)])

    if pseudo_msa_mask_rate != 0.15:
        command.extend(["--pseudo_msa_mask_rate", str(pseudo_msa_mask_rate)])
    if num_pseudo_msa != 15:
        command.extend(["--num_pseudo_msa", str(num_pseudo_msa)])
    if not allow_tf32:
        command.append("--no_tf32")

    print(f"Running command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print("FAILED")
        message("error", {"title": "OmegaFold failed", "body": f"{e}"})

    print("-" * 60)
    print("Returning results")
    return LatchOutputDir(str("/root/outputs"), output_directory.remote_path)
