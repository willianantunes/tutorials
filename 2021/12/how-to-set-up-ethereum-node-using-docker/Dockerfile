ARG CUSTOM_USER=aladdin

FROM ethereum/client-go:stable

ARG CUSTOM_USER

RUN addgroup -S "$CUSTOM_USER"

RUN adduser \
    --disabled-password \
    --gecos "" \
    --ingroup "$CUSTOM_USER" \
    "$CUSTOM_USER"

WORKDIR /home/$CUSTOM_USER

USER "$CUSTOM_USER"
