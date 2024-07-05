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

if [ "$device" = "gpu" ]; then
    image="apollo_gpu"
    gpu="--gpus all"
else
    image="apollo_cpu"
    gpu=""
fi

docker run -it $gpu --env DISPLAY=$DISPLAY --env QT_X11_NO_MITSHM=1 --volume /tmp/.X11-unix:/tmp/.X11-unix --volume /etc/machine-id:/etc/machine-id:ro -p 8888:8888 -p 8521:8521 -v $(pwd):/usr/src/apollo2028 ranuon98/$image:latest /bin/bash