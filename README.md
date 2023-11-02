# How to install LINKED: Linker Sequences Database Web App

## Prequisits 

- Docker Desktop
  Use the following link if you don't have docker installed: https://www.docker.com/get-started/
- WSL if you are using windows operating system
  Use the following link if you don't have WSL installed: https://learn.microsoft.com/en-us/windows/wsl/install

## Installation 

### Setting up the web app
1. Download all the files from the repository
2. Open up the directory where the folder is located in terminal
3. Open Docker Desktop
4. In terminal, enter:
   `make compose-start`
5. enter 'localhost:8000' to access the web app

### Import the data to the web app
1. In terminal, enter:
   `make compose-manage-py cmd="createsuperuser"`
2. Input the required field
3. go to 'localhost:8000/admin"
4. Log in with the crenditial that you created in step 2
5. Click "linkers" under "LINKER"
   ![image](https://github.com/becca-pettigrew/Linker/assets/100552559/32743923-b42f-4149-a058-ee4b2d907aee)
7. Select `Import`
8. Upload "linker_data.csv" from ./linkers_website/data from the folder you downloaded
9. Click "Flexibility" under "LINKER"
10. Repeat step 7 to 8 and upload "flexibility.json" file
11. Click "Hydrophobicity" under "LINKER"
12. Select `ADD HYDROPHOBICITY`
13. Enter in the required field, this is used as a placeholder
14. Go back to the "hydrophobivity" page
15. Selected the placeholder entry, go to action and select the "import data from hydrophocity_data.json"
![image](https://github.com/becca-pettigrew/Linker/assets/100552559/884042bf-b932-48b7-9485-c6442b889a86)
16. Go back to "localhost:8000" and start linking :)
  





