#!/usr/bin/env bash

set -e

python -m unittest test_publisher.TestPublisher.test_publish_messages_indefinitely_until_keyboard_interrupt
