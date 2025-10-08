#!/usr/bin/env bash
# create_antique_copy.sh
# Usage: ./create_antique_copy.sh /path/to/repo /path/to/outputdir
set -euo pipefail

REPO_PATH="${1:-.}"
OUTDIR="${2:-./antique_archive}"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
BUNDLE_NAME="edward_${TIMESTAMP}.bundle"
TARBALL_NAME="edward_${TIMESTAMP}.tar.gz"
SIGNED_TARBALL="${TARBALL_NAME}.asc"

mkdir -p "$OUTDIR"
pushd "$REPO_PATH" >/dev/null

# Create a bundle of everything
git bundle create "$OUTDIR/$BUNDLE_NAME" --all

# Create a source tarball (clean, no .git)
TMPDIR=$(mktemp -d)
git archive --format=tar --prefix="edward_${TIMESTAMP}/" HEAD > "$TMPDIR/$TARBALL_NAME"
gzip -f "$TMPDIR/$TARBALL_NAME"
mv "$TMPDIR/$TARBALL_NAME.gz" "$OUTDIR/$TARBALL_NAME"
rmdir "$TMPDIR"

# GPG-sign the tarball (requires GPG configured)
if command -v gpg >/dev/null 2>&1; then
  gpg --armor --detach-sign --output "$OUTDIR/$SIGNED_TARBALL" "$OUTDIR/$TARBALL_NAME"
  echo "Signed tarball created: $OUTDIR/$SIGNED_TARBALL"
else
  echo "gpg not found; skipping signature. Install gpg and re-run to sign."
fi

echo "Bundle created: $OUTDIR/$BUNDLE_NAME"
echo "Tarball created: $OUTDIR/$TARBALL_NAME"
popd >/dev/null
