import os
import sys
import subprocess


# Define the parent folder's name
def create_folder_structure(parent_folder, *args):

    validation_path = "./file_contents/validations.py"
    router_path = "./file_contents/router.py"
    main_path = "./file_contents/main.py"
    config_path = "./file_contents/config.py"

    # Create service
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    
        #App    
        if not os.path.exists(f"{parent_folder}/app"):
            os.makedirs(f"{parent_folder}/app")
    
            #API
            if not os.path.exists(f"{parent_folder}/app/api"):
                os.makedirs(f"{parent_folder}/app/api")

                module_files = ["schema","service","controller","router","model"]

                if not os.path.exists(f"{parent_folder}/app/api/example"):
                        os.makedirs(f"{parent_folder}/app/api/example")
                        for j in module_files:
                            file_name = os.path.join(f"{parent_folder}/app/api/example", f"example_{j}.py")
                            with open(router_path, 'r') as source_file:
                            # Read the content of the source file
                                router_content = source_file.read()
                            with open(file_name,"w") as file:
                                if j == "router":
                                     file.write(router_content)
                                else:
                                    file.write(f"#You can write your {j}'s here")
                if args:
                    for i in args:
                        if not os.path.exists(f"{parent_folder}/app/api/{i}"):
                            os.makedirs(f"{parent_folder}/app/api/{i}")
                            for j in module_files:
                                file_name = os.path.join(f"{parent_folder}/app/api/{i}", f"{i}_{j}.py")
                                with open(file_name,"w") as file:
                                    file.write(f"#You can write your {j}'s here")

            #Configuration
            if not os.path.exists(f"{parent_folder}/app/configuration"):
                os.makedirs(f"{parent_folder}/app/configuration")

                with open(config_path, 'r') as source_file:
                    # Read the content of the source file
                    config_content = source_file.read()

                config = os.path.join(f"{parent_folder}/app/configuration", "config.py")
                with open(config,"w") as file:
                    file.write(config_content)

            #Utils
            if not os.path.exists(f"{parent_folder}/app/utils"):
                os.makedirs(f"{parent_folder}/app/utils")

                #auth
                
                config = os.path.join(f"{parent_folder}/app/utils", "auth.py")
                with open(config,"w") as file:
                    file.write("#You can write your authentication's here")

                #validations
                with open(validation_path, 'r') as source_file:
                    # Read the content of the source file
                    validation_content = source_file.read()

                validation = os.path.join(f"{parent_folder}/app/utils", "validations.py")
                with open(validation,"w") as file:
                    file.write(validation_content)
            
            #main
            with open(main_path, 'r') as source_file:
                    # Read the content of the source file
                    main_content = source_file.read()

            env = os.path.join(f"{parent_folder}/app", "main.py")
            with open(env,"w") as file:
                file.write(main_content)
    #.env
    env = os.path.join(parent_folder, ".env")
    with open(env,"w") as file:
        file.write("#You can write you environment variable here")

    #configuration.json
    configure = os.path.join(parent_folder, "configurason.json")
    with open(configure,"w") as file:
        file.write("#You can write you environment variable here")

    #.gitignore
    gitignore = os.path.join(parent_folder, ".gitignore")
    with open(gitignore,"w") as file:
        file.write("#You can write you environment variable here")

    # # Installing required library 
    # libraries_to_install = ["Fastapi", "uvicorn"]

    # for library in libraries_to_install:
    #     command = ["pip", "install", library]
    #     try:
    #         subprocess.check_call(command)
    #         print(f"Installed {library} successfully.")
    #     except subprocess.CalledProcessError:
    #         print(f"Failed to install {library}.")


import argparse

def main():
    parser = argparse.ArgumentParser(description='Create folder structure for a service.')
    parser.add_argument('--service_name', help='Name of the service')
    parser.add_argument('--module_names', nargs='*', help='Name of the modules (optional)')
    args = parser.parse_args()

    service_name = args.service_name
    module_names = args.module_names

    create_folder_structure(service_name, *module_names)
    print("Structure created successfully!")

if __name__ == "__main__":
    main()

    
    