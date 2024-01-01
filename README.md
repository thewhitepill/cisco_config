<div align="center">
  <h1><code>cisco_config</code></h1>
  <p>A toolbelt for reading, parsing and analyzing Cisco configuration files</p>
</div>

## Contents

 - [Configuration Format](#configuration-format)

## Configuration Format

Cisco uses a proprieta text-based file format for configuring its various
software appliances. The configuration files consist of the following
features:
 - **Commands** - the basic building blocks of the configuration. Commands are
 defined by a name and a set of arguments. Commands are hierarchical.
 - **Commentaries** - comments are used to annotate the configuration files. A
 commentary is a line that starts with either `!`, `#` or `:` character.
 - **Metadata** - metadata are special lines that look like commands but carry
 additional information about the configuration.

### Commands

Commands carry the actual configuration information. A command must be fully
specified by its name and all of its required arguments until the end of the
line. If the parser can not fully identify a command before the end of the
line, it will raise an error. When a command is entered properly, the
configuration processor enters a new context. Within this context, the user
can enter additional commands that are related to the parent command and
further modify the parent's properties. The context is exited when the user
enters a command that is not related to the parent command. A commentary or a
new line cannot be used to exit the context; however, special commands may be
used to achieve this. A configuration file may visually group commands by
using indentation; however, this is merely a visual aid and does not affect
the parsing of the configuration file; therefore, it should not be relied
upon.
