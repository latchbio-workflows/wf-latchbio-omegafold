from latch.resources.workflow import workflow
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter

from wf.task import task

metadata = LatchMetadata(
    display_name="OmegaFold",
    author=LatchAuthor(
        name="LatchBio",
    ),
    parameters={
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
def template_workflow(
    input_file: LatchFile, output_directory: LatchOutputDir
) -> LatchFile:
    return task(input_file=input_file, output_directory=output_directory)