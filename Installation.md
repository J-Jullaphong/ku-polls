## KU Polls: Installation

### Automated Installation

1. Clone the repository from GitHub.
   ``` 
   git clone https://github.com/J-Jullaphong/ku-polls.git
   ```
   
2. Change directory to KU Polls.
   ``` 
   cd ku-polls 
   ```
   
3. Run Automated installation script.
   - Linux and macOS
   ```
   chmod +x auto-setup.sh
   ./auto-setup.sh 
   ```
   - Windows
   ```
   auto-setup.bat
   ``` 
   
4. (Optional) If you want to see the previous votes, enter this command.
   ```
   python manage.py loaddata data/votes.json
   ```
   
> **NOTE:** Once the script is completed, please follow how to run instruction in [README](README.md).

### Manual Installation

> **NOTE:** For the commands below, if you have the "**zsh: command not found: python**" problem on **macOS**, please change "**python**" to "**python3**".

1. Clone the repository from GitHub.
   ``` 
   git clone https://github.com/J-Jullaphong/ku-polls.git
   ```
   
2. Change directory to KU Polls.
   ``` 
   cd ku-polls 
   ```
   
3. Create a virtual environment.
   ```
   python -m venv venv
   ```
   
4. Activate the virtual environment.
   - Linux and macOS
   ``` 
   source venv/bin/activate 
   ```
   - Windows
   ```  
   .\venv\Scripts\activate
   ```

5. Install Dependencies for required python modules.
   ```
   pip install -r requirements.txt
   ```
   
6. Create a .env file for externalized variables.
   - Linux and macOS
   ``` 
   cp sample.env .env 
   ```
   - Windows
   ```  
   copy sample.env .env
   ``` 
   
7. Use a text editor to edit the .env file according to your needs.

8. Run migrations to apply database migrations.
   ```
   python manage.py migrate
   ```
   
9. Run tests to verify the correctness of the above installations.
   ```
   python manage.py test
   ```

10. Install data from the data fixtures.
   ```
   python manage.py loaddata data/users.json data/polls.json
   ```
    
11. (Optional) If you want to see the previous votes, enter this command.
   ```
   python manage.py loaddata data/votes.json
   ```

> **NOTE:** Once the steps are completed, please follow how to run instruction in [README](README.md).