import pynetlogo
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
import seaborn as sns
import sys
import logging
import warnings

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[logging.StreamHandler()])

stream_handler = [h for h in logging.root.handlers if isinstance(h , logging.StreamHandler)][0]
stream_handler.setLevel(logging.INFO)
stream_handler.setStream(sys.stderr)
logger = logging.getLogger("netlogo")
LOG = True

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore")

def parse_args():
    parser = argparse.ArgumentParser(description='Run a NetLogo model and visualize the results.')
    parser.add_argument('--num-people', type=int, default=100, help='Number of people in the simulation.')
    parser.add_argument('--max-pop', type=int, default=10, help='Maximum population density.')
    parser.add_argument('--life-expectancy', type=int, default=50, help='Life expectancy of people in the simulation.')
    parser.add_argument('--base-repr-rate', type=int, default=2, help='Base reproduction rate of the population.')
    parser.add_argument('--move-tendency', type=int, default=44, help='Tendency of people to move in the simulation.')
    parser.add_argument('--tick-limit', type=int, default=1000, help='Number of ticks to run the simulation for.')
    
    # NetLogo specific
    parser.add_argument('--gui', type=bool, default=True, help='Whether to show the NetLogo GUI.')
    parser.add_argument('--jvm-path', type=str, default='/usr/lib/jvm/java-21-openjdk-amd64/lib/server/libjvm.so', help='Path to the JVM shared library.')
    parser.add_argument('--netlogo-home', type=str, default='/usr/src/netlogo', help='Path to the NetLogo installation directory.')
    parser.add_argument('--model-path', type=str, default='netlogo/CityModel.nlogo', help='Path to the NetLogo model file.')

    args = parser.parse_args()
    logger.info(args)
    return args

def main():
    args = parse_args()
    # Initialize a NetLogo
    netlogo = pynetlogo.NetLogoLink(gui = args.gui, jvm_path = args.jvm_path, netlogo_home = args.netlogo_home)
    netlogo.load_model(args.model_path)

    netlogo.command(f'set num-people {args.num_people}')
    netlogo.command(f'set max-pop {args.max_pop}')
    netlogo.command(f'set life-expectancy {args.life_expectancy}')
    netlogo.command(f'set repr-rate {args.base_repr_rate}')
    netlogo.command(f'set move-tendency {args.move_tendency}')
    netlogo.command(f'set tick-limit {args.tick_limit}')
    netlogo.command('setup')

    def run_simulation():
        while netlogo.report('ticks') < args.tick_limit:
            netlogo.command('go')
    run_simulation()

    pop_dens = netlogo.patch_report("population-density")

    pop_dens = np.log(pop_dens + 1)

    fig, ax = plt.subplots(1)
    patches = sns.heatmap(
        pop_dens, xticklabels=5, yticklabels=5, cbar_kws={"label": "density"}, ax=ax
    )
    ax.set_xlabel("pxcor")
    ax.set_ylabel("pycor")
    ax.set_aspect("equal")
    fig.set_size_inches(20, 10)

    plt.show()

if __name__ == "__main__":
    main()