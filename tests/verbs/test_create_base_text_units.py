# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from graphrag.index.run.utils import create_run_context
from graphrag.index.workflows.v1.create_base_text_units import (
    build_steps,
    workflow_name,
)

from .util import (
    compare_outputs,
    get_config_for_workflow,
    get_workflow_output,
    load_expected,
    load_input_tables,
)


async def test_create_base_text_units():
    input_tables = load_input_tables(inputs=[])
    expected = load_expected(workflow_name)

    context = create_run_context(None, None, None)

    config = get_config_for_workflow(workflow_name)
    # test data was created with 4o, so we need to match the encoding for chunks to be identical
    config["text_chunk"]["strategy"]["encoding_name"] = "o200k_base"

    steps = build_steps(config)

    await get_workflow_output(
        input_tables,
        {
            "steps": steps,
        },
        context,
    )

    actual = await context.runtime_storage.get("base_text_units")
    compare_outputs(actual, expected)
