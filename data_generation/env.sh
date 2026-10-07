# Paths to the local DLPGenerator and edep-sim builds.
# Source it after activating the pixi env (source env.sh)
if [ -n "$BASH_VERSION" ]; then
  LARTPC_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
elif [ -n "$ZSH_VERSION" ]; then
  LARTPC_DIR=$(cd "$(dirname "${(%):-%x}")" && pwd)
fi
export LARTPC_DIR
export DLPGENERATOR_DIR=$LARTPC_DIR/DLPGenerator
export DLPGENERATOR_LIBDIR=$DLPGENERATOR_DIR/build/lib
export DLPGENERATOR_INCDIR=$DLPGENERATOR_DIR/build/include
export LD_LIBRARY_PATH=$DLPGENERATOR_LIBDIR:$LARTPC_DIR/edep-sim-install/lib:$LD_LIBRARY_PATH
export PATH=$LARTPC_DIR/edep-sim-install/bin:$PATH
