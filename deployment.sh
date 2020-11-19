#!/bin/bash
if [ "$ABSTRUSE_BRANCH" = "pip-release" ]; then
    # Wheel generation from setup
    python3 learnblock_setup.py sdist bdist_wheel --universal
    # Upload to pip repository
    python3 -m twine upload --skip-existing --repository testpypi dist/*
else
    echo "No deployment for branch $ABSTRUSE_BRANCH"
fi
