# script that sets up your web servers for the deployment of web_static.

class nginx_config {
  package { 'nginx':
    ensure => 'installed',
  }

  file { '/data/web_static/releases/test':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0755',
    recurse => true,
  }

  file { '/data/web_static/shared':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0755',
  }

  file { '/data/web_static/releases/test/index.html':
    ensure  => 'file',
    content => 'Holberton School',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
  }

  file { '/data/web_static/current':
    ensure  => 'link',
    target  => '/data/web_static/releases/test',
  }

  file { '/etc/nginx/sites-available/default':
    ensure  => 'file',
    content => template('nginx/default-site.erb'),
  }

  service { 'nginx':
    ensure    => 'running',
    enable    => true,
    subscribe => File['/etc/nginx/sites-available/default'],
  }
}
