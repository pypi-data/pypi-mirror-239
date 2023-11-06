import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from textfsm import clitable


def get_template_dir(_skip_ntc_package: bool = False) -> str:
    """
    Find and return the directory containing the TextFSM index file.

    Order of preference is:
    1) Find directory in `NET_TEXTFSM` Environment Variable.
    2) Check for pip installed `ntc-templates` location in this environment.
    3) ~/ntc-templates/ntc_templates/templates.

    If `index` file is not found in any of these locations, raise ValueError

    :return: directory containing the TextFSM index file

    """

    msg = """
Directory containing TextFSM index file not found.

Please set the NET_TEXTFSM environment variable to point at the directory containing your TextFSM
index file.

Alternatively, `pip install ntc-templates` (if using ntc-templates).

"""

    # Try NET_TEXTFSM environment variable
    template_dir = os.environ.get("NET_TEXTFSM")
    if template_dir is not None:
        template_dir = os.path.expanduser(template_dir)
        index = os.path.join(template_dir, "index")
        if not os.path.isfile(index):
            # Assume only base ./ntc-templates specified
            template_dir = os.path.join(template_dir, "templates")

    index = os.path.join(template_dir, "index")
    if not os.path.isdir(template_dir) or not os.path.isfile(index):
        raise ValueError(msg)
    return os.path.abspath(template_dir)


def clitable_to_dict(cli_table: clitable.CliTable) -> List[Dict[str, str]]:
    """Converts TextFSM cli_table object to list of dictionaries."""
    return_list = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        return_list.append(temp_dict)
    return return_list


def _textfsm_parse(
    textfsm_obj: clitable.CliTable,
    raw_output: str,
    attrs: Dict[str, str],
    template_file: Optional[str] = None,
) -> Union[str, List[Dict[str, str]]]:
    """Perform the actual TextFSM parsing using the CliTable object."""
    tfsm_parse: Callable[..., Any] = textfsm_obj.ParseCmd
    try:
        # Parse output through template
        if template_file is not None:
            tfsm_parse(raw_output, templates=template_file)
        else:
            tfsm_parse(raw_output, attrs)

        structured_data = clitable_to_dict(textfsm_obj)
        if structured_data == []:
            return raw_output
        else:
            return structured_data
    except (FileNotFoundError, clitable.CliTableError):
        return raw_output


def get_structured_data_textfsm(
    raw_output: str,
    platform: Optional[str] = None,
    command: Optional[str] = None,
    template: Optional[str] = None,
) -> Union[str, List[Dict[str, str]]]:
    """
    Convert raw CLI output to structured data using TextFSM template.

    You can use a straight TextFSM file i.e. specify "template". If no template is specified,
    then you must use an CliTable index file.
    """
    if platform is None or command is None:
        attrs = {}
    else:
        attrs = {"Command": command, "Platform": platform}

    if template is None:
        if attrs == {}:
            raise ValueError(
                "Either 'platform/command' or 'template' must be specified."
            )
        template_dir = get_template_dir()
        index_file = os.path.join(template_dir, "index")
        textfsm_obj = clitable.CliTable(index_file, template_dir)
        output = _textfsm_parse(textfsm_obj, raw_output, attrs)

        return output
    else:
        template_path = Path(os.path.expanduser(template))
        template_file = template_path.name
        template_dir_alt = template_path.parents[0]
        # CliTable with no index will fall-back to a TextFSM parsing behavior
        textfsm_obj = clitable.CliTable(template_dir=template_dir_alt)
        return _textfsm_parse(
            textfsm_obj, raw_output, attrs, template_file=template_file
        )


# For compatibility
get_structured_data = get_structured_data_textfsm


def structured_data_converter(
    raw_data: str,
    command: str,
    platform: str,
    use_textfsm: bool = False,
    textfsm_template: Optional[str] = None,
) -> Union[str, List[Any], Dict[str, Any]]:
    """
    Try structured data converters in the following order: TextFSM, TTP, Genie.

    Return the first structured data found, else return the raw_data as-is.
    """
    command = command.strip()
    if use_textfsm:
        structured_output_tfsm = get_structured_data_textfsm(
            raw_data, platform=platform, command=command, template=textfsm_template
        )
        if not isinstance(structured_output_tfsm, str):
            return structured_output_tfsm

    return raw_data
