exec { 'create virtualenv':
  command => '/usr/bin/python3 -m venv env',
  cwd     => '/path/to/your/directory',
  creates => '/path/to/your/directory/env',
  
}

exec { 'install requirements':
  command => '/path/to/your/directory/env/bin/pip install -r requirements.txt',
  cwd     => '/path/to/your/directory',
  require => Exec['create virtualenv'],
  onlyif  => 'test -f /path/to/your/directory/requirements.txt',
}
