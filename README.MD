# pi-cctv

A simple cctv built with PiCamera & Flask, on Python.

You will need to first install all dependencies first:

    $ sudo apt-get install python-picamera
    $ sudo pip install Flask

## Running pi-cctv

Then you can run the following to boot the server:

    $ python app.py

You can run the server in background using `screen`:

    $ screen -dm python app.py

## Troubleshooting

If you experience the following error:

    * failed to open vchiq instance

You might want try to fix it by execute this:

    sudo chmod a+rw /dev/vchiq

I am not sure why I need to do this everytime after boot.

## Nginx back-end

You can also run this using nginx:

    upstream pi_cam {
      server 127.0.0.1:5000;
      keepalive 4;
    }

    server {
      root /path/to/project/static;
      autoindex off;
      
      server_name camera.1.armv5.pi;

      location / {
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_pass http://pi_cam;
        proxy_redirect      off;
        proxy_buffering     off;
        proxy_set_header    Host            $host;
        proxy_set_header    X-Real-IP       $remote_addr;
      }

      location /static {
        alias /path/to/project/static;
      }
    }


