#!/bin/bash
# chmod +x matplotlib_ja.sh
# sh ./matplotlib_ja.sh
# Download Japanese fonts and  for matplotlib.

function logging() {
  echo -e "\033[0;32m$1\033[0m"
}

FONT_PATH="https://ipafont.ipa.go.jp/IPAfont/IPAfont00303.zip"
TMP_NAME="font.zip"
FONT_DIR="IPAfont00303"
FONT_FILENAME="ipam.ttf"
FONT_NAME="IPAMincho"
MATPLOTLIBPATH=$(python3 -c "import matplotlib; print(matplotlib.__path__[0])")
CASH_DIR="$(python3 -c 'import matplotlib; print(matplotlib.get_cachedir())')/fontList.cache"

echo "[Download and set up Japanese fonts for 'matplotlib']"
echo -n "1. Download font from "; logging $FONT_PATH
echo -n "2. Then, set it to "; logging ${MATPLOTLIBPATH}/mpl-data/fonts/ttf/${FONT_FILENAME}
echo -n "3. Add 'font.family : IPAMincho' to "; logging ${MATPLOTLIBPATH}/mpl-data/matplotlibrc

wget ${FONT_PATH} -O ${TMP_NAME} && \
    unzip ${TMP_NAME} && \
    cp ${FONT_DIR}/${FONT_FILENAME} ${MATPLOTLIBPATH}/mpl-data/fonts/ttf/${FONT_FILENAME} && \
    echo "font.family : ${FONT_NAME}" >> ${MATPLOTLIBPATH}/mpl-data/matplotlibrc && \

# Rebuild the font cache.
if [ -e $CASH_DIR ]; then
  rm ${CASH_DIR}
fi

if [ -e ${TMP_NAME} ]; then
  rm ${TMP_NAME}
fi

if [ -e ${FONT_DIR} ]; then
  rm -r ${FONT_DIR}
fi