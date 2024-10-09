from typing import Optional

from latch.resources.launch_plan import LaunchPlan
from latch.resources.workflow import workflow
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    LatchRule,
    Params,
    Section,
    Spoiler,
    Text,
)

from wf.task import omegafold_task

flow = [
    Section(
        "Input",
        Params("input_fasta"),
    ),
    Section(
        "Output",
        Params("run_name"),
        Text("Directory for outputs"),
        Params("output_directory"),
    ),
    Spoiler(
        "Advanced Parameters",
        Params(
            "num_cycle",
            "subbatch_size",
            "weights_file",
            "model",
            "pseudo_msa_mask_rate",
            "num_pseudo_msa",
            "allow_tf32",
        ),
    ),
]

metadata = LatchMetadata(
    display_name="OmegaFold",
    author=LatchAuthor(
        name="Ruidong Wu et al.",
    ),
    repository="https://github.com/HeliXonProtein/OmegaFold",
    license="Apache-2.0",
    tags=["Protein Engineering"],
    parameters={
        "run_name": LatchParameter(
            display_name="Run Name",
            description="Name of the run",
            batch_table_column=True,
            rules=[
                LatchRule(
                    regex=r"^[a-zA-Z0-9_-]+$",
                    message="Run name must contain only letters, digits, underscores, and dashes. No spaces are allowed.",
                )
            ],
        ),
        "input_fasta": LatchParameter(
            display_name="Input FASTA",
            description="The input fasta file",
            batch_table_column=True,
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            batch_table_column=True,
            description="Directory to write output files",
        ),
        "num_cycle": LatchParameter(
            display_name="Number of Cycles",
            description="The number of cycles for optimization",
            batch_table_column=True,
        ),
        "subbatch_size": LatchParameter(
            display_name="Subbatch Size",
            description="The subbatching number, smaller means slower but less GRAM requirements",
            batch_table_column=True,
        ),
        "weights_file": LatchParameter(
            display_name="Weights File",
            description="The model cache to run",
            batch_table_column=True,
        ),
        "model": LatchParameter(
            display_name="Model Number",
            description="OmegaFold model number to run (1 or 2)",
            batch_table_column=True,
        ),
        "pseudo_msa_mask_rate": LatchParameter(
            display_name="Pseudo MSA Mask Rate",
            description="The masking rate for generating pseudo MSAs",
            batch_table_column=True,
        ),
        "num_pseudo_msa": LatchParameter(
            display_name="Number of Pseudo MSAs",
            description="The number of pseudo MSAs",
            batch_table_column=True,
        ),
        "allow_tf32": LatchParameter(
            display_name="Allow TF32",
            description="Allow tf32 for speed if available",
            batch_table_column=True,
        ),
    },
    flow=flow,
)


@workflow(metadata)
def omegafold_workflow(
    run_name: str,
    input_fasta: LatchFile,
    num_cycle: int = 10,
    subbatch_size: Optional[int] = None,
    weights_file: Optional[str] = None,
    weights: Optional[str] = None,
    model: int = 1,
    pseudo_msa_mask_rate: float = 0.15,
    num_pseudo_msa: int = 15,
    allow_tf32: bool = True,
    output_directory: LatchOutputDir = LatchOutputDir("latch:///OmegaFold"),
) -> LatchOutputDir:
    """
    OmegaFold: High-resolution de novo structure prediction from protein sequences

    <html>
    <p align="center">
    <img src="https://user-images.githubusercontent.com/31255434/182289305-4cc620e3-86ae-480f-9b61-6ca83283caa5.jpg" alt="Latch Verified" width="100">
    </p>

    <p align="center">
    <strong>
    Latch Verified
    </strong>
    </p>

    ## OmegaFold

    OmegaFold is a groundbreaking computational method for high-resolution protein structure prediction from a single primary sequence, without the need for multiple sequence alignments (MSAs) or evolutionary information.

    ### Key Features

    - Predicts high-resolution protein structures from primary sequences alone
    - Combines a protein language model with a geometry-inspired transformer model
    - Effective for orphan proteins and fast-evolving proteins like antibodies
    - Outperforms RoseTTAFold and achieves similar accuracy to AlphaFold2 on recent structures

    ### Applications

    - Accurate predictions for orphan proteins not belonging to characterized protein families
    - Effective structure prediction for antibodies with noisy MSAs due to fast evolution
    - Potential insights into the natural protein folding process

    ### Credits

    High-resolution de novo structure prediction from primary sequence
    Ruidong Wu, Fan Ding, Rui Wang, Rui Shen, Xiwen Zhang, Shitong Luo, Chenpeng Su, Zuofan Wu, Qi Xie, Bonnie Berger, Jianzhu Ma, Jian Peng
    doi: https://doi.org/10.1101/2022.07.21.500999

    """
    return omegafold_task(
        run_name=run_name,
        input_fasta=input_fasta,
        subbatch_size=subbatch_size,
        weights_file=weights_file,
        weights=weights,
        model=model,
        pseudo_msa_mask_rate=pseudo_msa_mask_rate,
        num_cycle=num_cycle,
        num_pseudo_msa=num_pseudo_msa,
        allow_tf32=allow_tf32,
        output_directory=output_directory,
    )


LaunchPlan(
    omegafold_workflow,
    "Folding Test",
    {
        "run_name": "Test_Run",
        "input_fasta": LatchFile(
            "s3://latch-public/proteinengineering/omegafold/omegafold_test.fasta"
        ),
    },
)
