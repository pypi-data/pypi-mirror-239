from os import path
import pkg_resources

# List of compatible firmware builds
MIN_COMPAT_FW = 576
COMPAT_FW = 587

# Official release name
distribution = pkg_resources.get_distribution("moku")
release = distribution.version
location = path.join(distribution.location, "moku")
