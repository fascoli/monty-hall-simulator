#!/usr/bin/env python3
"""
monty-hall.py - Monty Hall Problem simulator
Copyright (c) 2020 Matteo Fascoli <matteo@fascoli.com>
"""

import random
import argparse
import sys

try:
    from prettytable import PrettyTable
    TABULATE_AVAILABLE = True
except ImportError:
    print("Warning: 'prettytable' python module not found. Please install it "\
        "to enable detailed tabular output (`pip install prettytable`)")
    TABULATE_AVAILABLE = False

def print_report(data):
    """ Print out the results of the simulation. """

    print("Monty Hall Problem simulator: {} doors, {} runs, " \
        "switch door: {}".format(
            data["doors"],
            data["runs"],
            ("yes" if data["do_switch"] else "no")))

    if TABULATE_AVAILABLE:
        doors_ids = ["Door"+str(x) for x in range(1, data["doors"]+1)]
        col_titles = ["run #"] + ["Switch door?"] + doors_ids + ["Win?"]
        table = PrettyTable(col_titles)

        for row in data["results"]:
            cols = [" "] * (data["doors"] + 3)
            cols[0] = row["run"] + 1
            cols[1] = ("Yes" if data["do_switch"] else "No")
            for x in row["goat_doors"]:
                cols[x+2] += "G"            
            cols[row["winning_door"]+2] += "W"
            cols[row["player_door"]+2] += "P"
            cols[row["switch_door"]+2] += "S"
            cols[row["presenter_goat_door"]+2] += "L"
            cols[len(cols)-1] = ("Yes" if row["win"] else "No")
            table.add_row(cols)

        print("\nSimulation details:")
        print(table)
        print("Legend:\n" \
            "  G: goat\n" \
            "  W: winning door\n" \
            "  P: door chosen by the player\n" \
            "  L: goat door chosen by the presenter\n" \
            "  S: proposed door by the presenter for the switch.\n")

    print("Summary: wins={} losses={} (win rate is {} %)".format(
        data["total_wins"],
        data["runs"] - data["total_wins"],
        (data["total_wins"] / (data["runs"]*1.0)) * 100))


def simulate(runs, doors, do_switch):
    """ Run the simulation. """

    results = list()
    total_wins = 0

    for run in range(0, runs):

        # Randomly choose the winning door and the player's door.
        winning_door = random.randint(0, doors-1)
        player_door = random.randint(0, doors-1)

        # All doors, except the winning one, have goats behind.
        goat_doors = \
            [x for x in range(0, doors) if x != winning_door]

        # Now choose a door with a goat that the presenter will open.
        # Can't be the winning one, nor the one chosen by the player.
        presenter_goat_doors = \
            [x for x in range(0, doors) if x != winning_door and x != player_door]
        presenter_goat_door = \
            presenter_goat_doors[random.randint(0, len(presenter_goat_doors)-1)]
        
        # Find an alternative door to propose - should not be the one already
        # chosen by the player, nor the one already opened by the presenter.
        switch_doors = \
            [x for x in range(0, doors) if x != presenter_goat_door and x != player_door]
        switch_door = \
            switch_doors[random.randint(0, len(switch_doors)-1)]

        # Should we switch doors?
        if do_switch:
            win = (switch_door == winning_door)
        else:
            win = (player_door == winning_door)

        if win:
            total_wins += 1

        results.append({
            "win": win,
            "run": run,
            "winning_door": winning_door,
            "presenter_goat_door": presenter_goat_door,
            "goat_doors": goat_doors,
            "player_door": player_door,
            "switch_door": switch_door
        })

    return {
        "runs": runs,
        "doors": doors,
        "total_wins": total_wins,
        "do_switch": do_switch,
        "results": results
    }


def main():
    """ Parse the arguments and run the simulation. """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--switch',
        action="store_true",
        help='Switch to the door proposed by the presenter. Default is False',
        required=False)
    parser.add_argument(
        '--runs',
        type=int,
        default=20,
        help='Number of runs to perform. Default is 20.',
        required=False)
    parser.add_argument(
        '--doors',
        type=int,
        default=3,
        help='Number of doors. Default is 3.',
        required=False)
    args = parser.parse_args()

    # Check the supplied arguments.
    if args.runs < 1:
        print("Error: --runs must be greater than 0. Exiting.")
        sys.exit(1)
    if args.doors < 3:
        print("Error: --doors must be equal or greater than 3. Exiting.")
        sys.exit(1)

    # Initialize the random seed and run the simulation.
    random.seed()
    results = simulate(runs=args.runs, doors=args.doors, do_switch=args.switch)
    print_report(results)


if __name__ == "__main__":
    main()
