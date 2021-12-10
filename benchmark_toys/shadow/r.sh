#!/usr/bin/env bash

set -o nounset

rm a.out source.txt shadow.txt &> /dev/null

if command -v gcc-7.1.0 ; then
  GCC="gcc-7.1.0"
else
  GCC="gcc"
fi

if command -v clang-7.1.0 ; then
  CLANG="clang-7.1.0"
else
  CLANG="clang"
fi

# Check the source program does not have cerntain errors.
if ! "${GCC}" -Wall -Wextra source.c &> source.txt ; then
  exit 1
fi

if ! "${CLANG}" -Weverything source.c >> source.txt 2>&1 ; then
  exit 1
fi

if grep -q "Wimplicit-int" source.txt || \
   grep -q "defaulting to type" source.txt || \
   grep -q "Wmain-return-type" source.txt || \
   grep -q "Wimplicit-function-declaration" source.txt || \
   grep -q "Wincompatible-library-redeclaration" source.txt || \
   grep -q "too few arguments" source.txt ; then
  exit 1
fi
# End of the check.

./a.out > source.txt
if ! grep -q "world" source.txt ; then
  exit 1
fi


# Check the shadow program does not have cerntain errors.
"${GCC}" -Wall -Wextra shadow.c &> shadow.txt
"${CLANG}" -Weverything shadow.c >> shadow.txt 2>&1

if grep -q "Wimplicit-int" shadow.txt || \
   grep -q "defaulting to type" shadow.txt || \
   grep -q "Wmain-return-type" shadow.txt || \
   grep -q "Wimplicit-function-declaration" shadow.txt || \
   grep -q "Wincompatible-library-redeclaration" shadow.txt || \
   grep -q "too few arguments" shadow.txt ; then
  exit 1
fi
# End of the check.

if ! grep -q "expected '}'" shadow.txt ; then
  exit 1
fi

exit 0
