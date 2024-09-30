import csv
import time
import keyboard
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    time_counter = 0
    neo = 0
    tags = 0
    filename = 'neo_tracking.csv'
    space_pressed = False
    times, neos = [], []

    # Time acceleration factor (10x faster)
    time_acceleration = 1

    # Set up the plot
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot(times, neos)
    ax.set_ylim(-1, 1)
    ax.set_xlim(0, 60)  # Start with 60 seconds visible
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Neophilia')
    ax.set_title('Neophilia over Time')
    ax.grid(True)
    plt.draw()

    # Create and open the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'neo', 'tags'])  # Write header

        print(f"Time is accelerated by a factor of {time_acceleration}.")
        print("Press and hold spacebar to increase neo. Release to decrease.")
        print("Press 'q' to quit.")

        start_time = time.time()

        while True:
            current_time = time.time()
            elapsed_time = (current_time - start_time) * time_acceleration

            if elapsed_time >= 1:
                time_counter += 1
                start_time = current_time

                # Decrease neo by 0.01 if spacebar is not pressed
                if not keyboard.is_pressed('space'):
                    neo = max(-1, neo - 0.01 * time_acceleration)
                    space_pressed = False
                else:
                    neo = min(1, neo + 0.01 * time_acceleration)
                    if not space_pressed:
                        tags += 1
                        space_pressed = True

                # Write to CSV
                writer.writerow([time_counter, f"{neo:.2f}", tags])
                file.flush()  # Ensure data is written to file

                # Update plot data
                times.append(time_counter)
                neos.append(neo)
                line.set_data(times, neos)
                ax.set_xlim(max(0, time_counter - 60), max(60, time_counter))
                plt.draw()
                plt.pause(0.01)

                # Display current time, neo value, and tags
                sys.stdout.write(f"\rTime: {time_counter}s, Neo: {neo:.2f}, Tags: {tags}")
                sys.stdout.flush()

            # Check for quit command
            if keyboard.is_pressed('q'):
                print("\nQuitting...")
                break

            # Small sleep to reduce CPU usage
            time.sleep(0.01 / time_acceleration)

if __name__ == "__main__":
    main()