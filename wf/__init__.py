from latch.resources.workflow import workflow
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    Fork,
    ForkBranch,
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    LatchRule,
    Params,
    Section,
    Spoiler,
)

from wf.task import task

metadata = LatchMetadata(
    display_name="OmegaFold",
    author=LatchAuthor(
        name="LatchBio",
    ),
    parameters={
        "run_name": LatchParameter(
            display_name="Run Name",
            description="Name of run",
            batch_table_column=True,
            rules=[
                LatchRule(
                    regex=r"^[a-zA-Z0-9_-]+$",
                    message="Run name must contain only letters, digits, underscores, and dashes. No spaces are allowed.",
                )
            ],
        ),
        "input_file": LatchParameter(
            display_name="Input File",
            batch_table_column=True,  # Show this parameter in batched mode.
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            batch_table_column=True,  # Show this parameter in batched mode.
        ),
    },
)


@workflow(metadata)
def omegafold_workflow(
    run_name: str, input_file: LatchFile, output_directory: LatchOutputDir
) -> LatchOutputDir:
    return task(
        run_name=run_name, input_file=input_file, output_directory=output_directory
    )
