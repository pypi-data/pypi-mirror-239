# AUTO GENERATED FILE - DO NOT EDIT

export ''_readlocalfile

"""
    ''_readlocalfile(;kwargs...)

A ReadLocalFile component.
Read a local file

State
- file (string): Base64 string representation of the content
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `filePath` (String; required): Full path or relative path where the file is
"""
function ''_readlocalfile(; kwargs...)
        available_props = Symbol[:id, :filePath]
        wild_props = Symbol[]
        return Component("''_readlocalfile", "ReadLocalFile", "pollination_dash_io", available_props, wild_props; kwargs...)
end

