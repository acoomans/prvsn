from .command import (
    command,
    bash,
    ruby,
)

from .file import (
    chown,
    file,
    file_contains,
    mkdir,
)

from .filetype import (
    file_handler
)

from .hostname import (
    hostname,
)

from .kernel import (
    module,
)

from .package import (
    apt_package,
    cask_package,
    homebrew_install,
    homebrew_package,
    mac_app_store,
    mac_app_store_signin,
    package,
    yum_package,
)

from .unarchive import (
    unarchive,
    untar,
    unzip,
)

from .user import (
    real_user,
    real_home,
)