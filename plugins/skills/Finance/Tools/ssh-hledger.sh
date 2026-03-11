#!/bin/bash
# SSH wrapper for running hledger commands on VPS
# Runs hledger inside the Docker container, file operations directly on host
# Usage: ssh-hledger.sh <hledger-args>
# Example: ssh-hledger.sh bal
#          ssh-hledger.sh is --monthly
#          ssh-hledger.sh accounts
#          ssh-hledger.sh append "ENTRY_TEXT"

VPS_HOST="root@76.13.98.215"
JOURNAL="/data/finance/journal.hledger"
FINANCE_DIR="/data/finance"
CONTAINER="bos8s4kg8gggocock4ss0www-015553219229"

if [ "$1" = "append" ]; then
    # Special case: append a transaction entry to the journal (host filesystem)
    shift
    ENTRY="$1"
    ssh "$VPS_HOST" "echo '' >> $JOURNAL && echo '$ENTRY' >> $JOURNAL && cd $FINANCE_DIR && git add -A && git commit -m 'Add transaction via Ekko'"
else
    # Run hledger command inside the container
    ssh "$VPS_HOST" "docker exec $CONTAINER hledger -f $JOURNAL $*"
fi
