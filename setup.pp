
$version = '3.11.5'
$download_url = "https://www.python.org/ftp/python/${version}/Python-${version}.tgz"

package { ['gcc', 'make']:
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

exec { 'compile_and_install_python':
    command => "/tmp/Python-${version}/configure --enable-optimizations && make altinstall",
    cwd     => "/tmp/Python-${version}",
    creates => "/usr/local/bin/python3.11",
    require => [Exec['extract_python_source'], Package['gcc'], Package['make']],
}

file { '/usr/bin/python':
    ensure => link,
    target => '/usr/local/bin/python3.11',
    require => Exec['compile_and_install_python'],
}
