# Import the ansible and json modules
import json

import ansible

import ansible_runner


# Define a function to run an Ansible playbook
def run_playbook(playbook, inventory):
    # Create an Ansible runner object
    r = ansible_runner.run(private_data_dir="./.tmp", playbook=playbook)

    # playbook=playbook, inventory=inventory, remote_user="nzeer", become=True)
    # Run the playbook and get the results
    results = r.stats
    # Return the results
    return results


# Define a function to parse the results and get the OS information
def get_os_info(results={"ip": 1}):
    # Initialize an empty dictionary to store the OS information
    os_info = {}
    if results == None:
        print("results empty")
        quit()
    print(results)
    # Loop through the results
    for host, data in results.items():
        # Check if the data has ansible_facts key
        if "ansible_facts" in data:
            # Get the ansible_facts value
            facts = data["ansible_facts"]
            # Get the OS name, version, and family from the facts
            os_name = facts.get("ansible_distribution", "Unknown")
            os_version = facts.get("ansible_distribution_version", "Unknown")
            os_family = facts.get("ansible_os_family", "Unknown")
            # Add the OS information to the dictionary with the host as the key
            os_info[host] = {
                "name": os_name,
                "version": os_version,
                "family": os_family,
            }
    # Return the OS information
    return os_info


# Define a function to write the OS information to a JSON file
def write_json(data, file):
    # Open the file in write mode
    with open(file, "w") as f:
        # Write the JSON data to the file
        json.dump(data, f, indent=4)


# Define a main function
def main():
    # Get the playbook name from the user input or use the default
    playbook = "./gather_facts.yml"
    # Get the inventory name from the user input or use the default
    inventory = "./inventory"
    # Get the output file name from the user input or use the default
    output_file = "./os_info.json"
    # Call the run_playbook function and get the results
    results = run_playbook(playbook, inventory)
    # Call the get_os_info function and get the OS information
    os_info = get_os_info(results)
    # Call the write_json function and write the OS information to the file
    write_json(os_info, output_file)
    # Print a success message
    print(
        f"Successfully gathered OS information for {inventory} and wrote to {output_file}"
    )


# Check if the script is run as the main module
if __name__ == "__main__":
    # Call the main function
    main()
