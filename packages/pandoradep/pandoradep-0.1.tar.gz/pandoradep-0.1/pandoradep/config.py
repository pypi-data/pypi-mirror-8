
''' Configuration file '''

# Repo to upload the updated dependencies
PANDORA_REPO = 'https://raw.github.com/pandora-auth-ros-pkg/ci-scripts/master/pandoradep/repos.yml'

# ROSinstall templates
INSTALL_TEMPLATE_SSH = "- git: {local-name: $repo_name, uri: 'git@github.com:pandora-auth-ros-pkg/$repo_name.git', version: hydro-devel}"
INSTALL_TEMPLATE_HTTPS = "- git: {local-name: $repo_name, uri: 'https://github.com/pandora-auth-ros-pkg/$repo_name.git', version: hydro-devel}"

# Git templates
GIT_TEMPLATE_SSH = 'git@github.com:pandora-auth-ros-pkg/$repo_name.git'
GIT_TEMPLATE_HTTPS = 'https://github.com/pandora-auth-ros-pkg/$repo_name.git'

# Colorscheme
colors = {'error': 'red',
          'success': 'green',
          'info': 'magenta',
          'debug': 'blue',
          'data': 'white'
          }
