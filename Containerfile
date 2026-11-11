FROM scratch

# fs-icons — SVG icon artifact
# This is a pure data artifact; no runtime process.
# The icon directories are copied into the image for distribution.

COPY homarrlabs/ /usr/share/freeSynergy/icons/homarrlabs/

LABEL org.opencontainers.image.title="fs-icons"
LABEL org.opencontainers.image.description="FreeSynergy curated SVG icon sets"
LABEL org.opencontainers.image.vendor="FreeSynergy"
