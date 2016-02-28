# OpsComm-cli
##A Cli interface to the OpsComm Middleware

This is the cli client interface to the [OpsComm-server](https://github.com/stonesrose/OpsComm-Server-Core)

Usage:
  opscomm [options] ACTION ITEM [<keyvalues>...]

  opscomm -h|--help
  opscomm --version

Options:
  -h --help                              Show this screen.
  --version                              Show version.
  -s SERVER --server=SERVER              Set Server 
  -p PORT --port=PORT                    Set Port 
  -F --FULL                              Use Full detail listing
  -c COLUMN --columns=COLUMNS            Set Columns [default: 25]
  -L LEVEL --logging=level               Set Debug Level critical, error, warning, info, debug  [default: error]

Examples:
  opscomm search n3b01