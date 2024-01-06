
$version = '3.11.5'
$download_url = "https://www.python.org/ftp/python/${version}/Python-${version}.tgz"

package { ['gcc', 'make', 'pkg-config', 'build-essential', 'libreadline-dev', 'libncursesw5-dev', 'libssl-dev',  'libsqlite3-dev', 'tk-dev', 'libgdbm-dev', 'libc6-dev', 'libbz2-dev', 'libffi-dev', 'zlib1g-dev']:
    ensure => installed,
}

exec { 'download_python_source':
    command => "/usr/bin/curl -o /tmp/pythony.tgz ${download_url}",
    creates => "/tmp/pythony.tgz",
}

exec { 'extract_python_source':
    command => "/bin/tar -xzf /tmp/pythony.tgz -C /tmp",
    creates => "/tmp/Python-${version}",
    require => Exec['download_python_source'],
}

exec { 'compile_and_create_python_make_file':
    command => "/tmp/Python-${version}/configure --enable-optimizations",
    cwd     => "/tmp/Python-${version}",
    require => Exec['extract_python_source'],
}
# exec {'compile_python':
#     command => "/usr/bin/make altinstall",
#     cwd     => "/tmp/Python-${version}",
#     creates => "/usr/local/bin/python3.11",
#     require => [Exec['compile_and_create_python_make_file'], Package['gcc'], Package['make']]
# }
# exec { 'create_python_symlink':
#     command => "/bin/ln -s /usr/local/bin/python3.11 /usr/local/bin/python"
#     creates => "/usr/local/bin/python",
#     require => Exec['compile_python'],
# }
