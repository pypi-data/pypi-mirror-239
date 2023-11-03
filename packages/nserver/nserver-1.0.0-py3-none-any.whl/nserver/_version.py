"""Version information for this package."""
### IMPORTS
### ============================================================================
## Standard Library

## Installed

## Application

### CONSTANTS
### ============================================================================
## Version Information - DO NOT EDIT
## -----------------------------------------------------------------------------
# These variables will be set during the build process. Do not attempt to edit.
PACKAGE_VERSION = "1.0.0"
BUILD_VERSION = "1.0.0"
BUILD_GIT_HASH = "628db055848c6543641d514b4186f8d953b6af7d"
BUILD_GIT_HASH_SHORT = "628db05"
BUILD_GIT_BRANCH = "main"
BUILD_TIMESTAMP = 1698994950
BUILD_DATETIME = datetime.datetime.utcfromtimestamp(1698994950)

## Version Information Strings
## -----------------------------------------------------------------------------
VERSION_INFO_SHORT = f"{BUILD_VERSION}"
VERSION_INFO = f"{PACKAGE_VERSION} ({BUILD_VERSION})"
VERSION_INFO_LONG = (
    f"{PACKAGE_VERSION} ({BUILD_VERSION}) ({BUILD_GIT_BRANCH}@{BUILD_GIT_HASH_SHORT})"
)
VERSION_INFO_FULL = (
    f"{PACKAGE_VERSION} ({BUILD_VERSION})\n"
    f"{BUILD_GIT_BRANCH}@{BUILD_GIT_HASH}\n"
    f"Built: {BUILD_DATETIME}"
)
