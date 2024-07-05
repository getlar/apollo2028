usage() { echo "Usage: $0 [-o <win|mac>] [-d <cpu|gpu>] [-v <version|latest>]" 1>&2; exit 1; }

while getopts "o:d:v:" opt; do
    case $opt in
        o)
            os=${OPTARG}
            ;;
        d)
            device=${OPTARG}
            ;;
        v)
            version=${OPTARG}
            ;;
        :) 
            echo "Option -$OPTARG requires an argument." >&2;;
        *)
            usage
            ;;
    esac
done

if [ -z "$os" ] || [ -z "$device" ] || [ -z "$version" ]; then
    usage
fi

if [ "$os" = "mac" ]; then
    docker run -it --gpus all --env DISPLAY=host.docker.internal:0 --env QT_X11_NO_MITSHM=1 --volume /tmp/.X11-unix:/tmp/.X11-unix --volume /etc/machine-id:/etc/machine-id:ro --device /dev/dri -p 8888:8888 -p 8521:8521 -v $(pwd):/usr/src/apollo2028 ranuon98/apollo:latest /bin/bash
else
    docker run -it --gpus all --env DISPLAY=$DISPLAY --env QT_X11_NO_MITSHM=1 --volume /tmp/.X11-unix:/tmp/.X11-unix --volume /etc/machine-id:/etc/machine-id:ro --device /dev/dri -p 8888:8888 -p 8521:8521 -v $(pwd):/usr/src/apollo2028 ranuon98/apollo:latest /bin/bash
fi