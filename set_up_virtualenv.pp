exec { 'create virtualenv':
  command => '/usr/bin/python -m venv ilens',
  creates => '/home/ubuntu/projects/components/ilens',
  
}

exec { 'install requirements':
  command => '/home/ubuntu/projects/components/ilens/bin/pip install -r requirements.txt',
  require => Exec['create virtualenv'],
  onlyif  => '/usr/bin/test -f /home/ubuntu/projects/components/requirements.txt',
}
